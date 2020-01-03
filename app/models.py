from app import db


class Video(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    video_id = db.Column(db.String(11), unique=True, nullable=False)
    title = db.Column(db.String(100), index=True, unique=False, nullable=False)
    upload_date = db.Column(db.DateTime, index=True, unique=False)
    description = db.Column(db.String(1000), index=False, unique=False)
    thumbnail_url = db.Column(db.String(256), index=False, unique=True)
    duration = db.Column(db.Integer, unique=False)
    view_count = db.Column(db.Integer, index=True, unique=False)
    is_downloaded = db.Column(db.Boolean, default=False, index=True, unique=False)
    channel_id = db.Column(db.Integer, db.ForeignKey('channel.id'), nullable=False)

    def __repr__(self):
        return '<Video \'{}\'>'.format(self.title)


class Channel(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    channel_id = db.Column(db.String(50), nullable=False)
    subscriber_count = db.Column(db.Integer, unique=False)
    videos = db.relationship('Video', backref='channel', lazy=True)

    def __repr__(self):
        return '<Channel \'{}\'>'.format(self.name)

    def get_nondownloaded_videos(self):
        return Video.query.with_parent(self) \
                          .filter_by(is_downloaded=False) \
                          .order_by(Video.upload_date.desc()) \
                          .all()

