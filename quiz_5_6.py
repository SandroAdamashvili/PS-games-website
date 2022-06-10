from flask import Flask, render_template, request, flash
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///ps_games.sqlite'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = 'key'
db = SQLAlchemy(app)


class Games(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    game_title = db.Column(db.String(200), nullable=False)
    price = db.Column(db.Float, nullable=False)
    img_source = db.Column(db.String(200), nullable=False)

    def __str__(self):
        return f'game title: {self.game_title}, \nprice: {self.price}'


class MyGames(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    game_title = db.Column(db.String(200), nullable=False)
    price = db.Column(db.Float, nullable=False)


@app.route('/')
def home():
    return render_template('home.html')


@app.route('/games')
def games():
    all_games = Games.query.all()
    return render_template('games.html', games=all_games)


@app.route('/mygames')
def my_games():
    all_my_games = MyGames.query.all()
    return render_template('my_games.html', my_games=all_my_games)


@app.route('/addgame', methods=['GET', 'POST'])
def add_game():

    if request.method == "POST":
        t = request.form['title']
        p = request.form['price']
        if t == '' or p == '':
            flash("შეიყვანეთ მონაცემები!")
        elif not p.isdecimal():
            flash('შეიყვანეთ რიცხვი ფასის ველში!')
        else:
            g1 = MyGames(game_title=t, price=float(p))
            db.session.add(g1)
            db.session.commit()
            flash("თამაში დაემატა!")

    return render_template('add_game.html')


@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html')


if __name__ == '__main__':
    app.run(debug=True)