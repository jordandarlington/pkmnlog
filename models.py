from flask_sqlalchemy import SQLAlchemy
from datetime import date, datetime

db = SQLAlchemy()

class Playthrough(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), nullable=False)
    game = db.Column(db.String(120), nullable=False)
    start_date = db.Column(db.Date, default=date.today)

    entries = db.relationship('Entry', backref='playthrough', lazy=True)

class Entry(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    playthrough_id = db.Column(db.Integer, db.ForeignKey('playthrough.id'), nullable=False)

    title = db.Column(db.String(120), nullable=False)
    content = db.Column(db.Text, nullable=False)
    type = db.Column(db.String(50), nullable=True)
    timestamp = db.Column(db.DateTime, server_default=db.func.now())
