from flask import render_template
from app import app, db
from youtube_dl.utils import DownloadError


@app.errorhandler(DownloadError)
def video_not_found_error(error):
    return render_template('entity_not_found.html', entity={'type':'Video'}, error=error), 404


@app.errorhandler(404)
def not_found_error(error):
    return render_template('entity_not_found.html', entity={}, error=error), 404


@app.errorhandler(500)
def internal_error(error):
    db.session.rollback()
    return render_template('500.html'), 500
