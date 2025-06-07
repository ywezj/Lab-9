#выполнено сразу с допзаданием
from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
import os

app = Flask(__name__)
basedir = os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'games.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

class Game(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    year = db.Column(db.Integer, nullable=False)

    def __repr__(self):
        return f'<Game {self.title} ({self.year})>'

with app.app_context():
    db.create_all()

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        # Обработка очистки списка
        if 'clear' in request.form:
            Game.query.delete()
            db.session.commit()
            return redirect(url_for('index'))
        
        # Обработка добавления игры
        title = request.form['title']
        year = request.form['year']
        
        if not title or not year:
            return "Необходимо заполнить все поля", 400
            
        try:
            year = int(year)
        except ValueError:
            return "Год должен быть числом", 400
            
        new_game = Game(title=title, year=year)
        db.session.add(new_game)
        db.session.commit()
        return redirect(url_for('index'))
    
    games = Game.query.order_by(Game.year.desc()).all()
    return render_template('index.html', games=games)

if __name__ == '__main__':
    app.run(debug=True)