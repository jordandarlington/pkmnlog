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

@app.route('/playthrough/new', methods=['GET', 'POST'])
def new_playthrough():
    if request.method == 'POST':
        name = request.form['name']
        game = request.form['game']
        start_date = request.form.get('start_date', date.today())
        playthrough = Playthrough(name=name, game=game, start_date=start_date)
        db.session.add(playthrough)
        db.session.commit()
        return redirect(url_for('index'))
    return render_template('new_playthrough.html')

@app.route('/playthrough/<int:playthrough_id>')
def view_playthrough(playthrough_id):
    playthrough = Playthrough.query.get_or_404(playthrough_id)
    entries = Entry.query.filter_by(playthrough_id=playthrough.id).order_by(Entry.timestamp.desc()).all()
    return render_template('playthrough.html', playthrough=playthrough, entries=entries)

@app.route('/playthrough/<int:playthrough_id>/entry/new', methods=['GET', 'POST'])
def new_entry(playthrough_id):
    playthrough = Playthrough.query.get_or_404(playthrough_id)
    if request.method == 'POST':
        title = request.form['title']
        content = request.form['content']
        type = request.form.get('type')
        entry = Entry(title=title, content=content, type=type, playthrough_id=playthrough.id)
        db.session.add(entry)
        db.session.commit()
        return redirect(url_for('view_playthrough', playthrough_id=playthrough.id))
    return render_template('new_entry.html', playthrough=playthrough)

if __name__ == '__main__':
    app.run(debug=True)