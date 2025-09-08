from flask import Flask, render_template, request, redirect, url_for
from models import db, Playthrough, Entry
from datetime import date

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///pkmnlog.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db.init_app(app)

with app.app_context():
    db.create_all()

@app.route('/')
def index():
    playthroughs = Playthrough.query.order_by(Playthrough.start_date.desc()).all()
    return render_template('index.html', playthroughs=playthroughs)

