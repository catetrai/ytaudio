import os
from datetime import datetime
#from io import StringIO
#from contextlib import redirect_stdout
from flask import render_template, send_file, abort, redirect, flash
from app import app, db
from app.models import Channel, Video
from app.forms import SubscribeForm, UnsubscribeForm
from app.youtube_extractor import download_mp3, get_channel_videos
from youtube_dl.utils import DownloadError


@app.route('/')
@app.route('/index')
def index():
    channel_videos = []
    for channel in Channel.query.all():
        channel_videos.append({ 'channel': channel, 'videos': channel.get_nondownloaded_videos() })
    return render_template('index.html', channel_videos=channel_videos)


@app.route('/channels')
def channels():
    channels = Channel.query.all()
    form_sub = SubscribeForm()
    form_unsub = UnsubscribeForm()
    return render_template('channels.html', channels=channels, form_sub=form_sub, form_unsub=form_unsub)


@app.route('/info/<videoid>')
def video_info(videoid):
    video = Video.query.filter_by(video_id=videoid).first_or_404()
    return render_template('video_info.html', video=video)


@app.route('/subscribe', methods=['POST'])
def subscribe():
    form = SubscribeForm()
    if form.validate_on_submit():
        videos = get_channel_videos(form.channel.data)

        if not videos:
            return render_template('entity_not_found.html', entity={'type':'Channel','value':form.channel.data}, error=''), 404
        
        channel = Channel(name=videos[0]['uploader_id'], channel_id=videos[0]['channel_id'])
        db.session.add(channel)
        db.session.commit()

        for v in videos:
            if v and 'id' in v:
                video = Video(video_id=v['id'],
                            title=v['title'],
                            channel_id=channel.id,
                            description=v['description'],
                            thumbnail_url=v['thumbnail'],
                            duration=v['duration'],
                            upload_date=datetime.strptime(v['upload_date'], '%Y%m%d'),
                            view_count=v['view_count'])
                db.session.add(video)
        db.session.commit()
        
    return redirect('/channels')


@app.route('/unsubscribe', methods=['POST'])
def unsubscribe():
    form = UnsubscribeForm()
#    if form.validate_on_submit():
    channel = Channel.query.get(form.channel.data)
    if not channel:
        return render_template('entity_not_found.html', entity={'type':'Channel'}, error=''), 404

    for video in Video.query.with_parent(channel).all():
        db.session.delete(video)

    db.session.delete(channel)
    db.session.commit()

    return redirect('/channels')


#@app.route('/audiostdout/<videoid>')
#def serve_mp3_file_stdout(videoid): 
#    f = StringIO()
#    with redirect_stdout(f):
#        download_mp3(videoid, stdout=True)
#        try:
#            return send_file(f, attachment_filename='{}.mp3'.format(videoid))
#        except:
#            abort(404)


@app.route('/audio/<videoid>')
def serve_mp3_file(videoid):
    try:
        if download_mp3(videoid) == 0:
            set_downloaded_flag(videoid)
            return send_file('static/{}.mp3'.format(videoid), attachment_filename='{}.mp3'.format(videoid))
    except:
        abort(404)
    finally:
        os.remove('app/static/{}.mp3'.format(videoid))
        print('Deleted file \'{}.mp3\''.format(videoid))


@app.route('/explore')
def explore():
    return render_template('base.html')



def set_downloaded_flag(videoid):
    video = Video.query.filter_by(video_id=videoid).first_or_404()
    video.is_downloaded = True
    db.session.commit()
    return


