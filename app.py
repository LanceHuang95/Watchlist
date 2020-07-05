import os
import sys
import click
from flask import Flask,url_for,request,render_template
from flask_sqlalchemy import SQLAlchemy

WIN = sys.platform.startswith("win")
prefix = 'sqlite:///' if WIN else 'sqlite:////'

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = prefix + os.path.join(app.root_path,'data.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

@app.cli.command()
@click.option('--drop',is_flag=True, help='Create after drop.')
def initdb(drop):
    if drop:
        db.drop_all()
    db.create_all()
    click.echo('Initialized	database.')

class User(db.Model):
    id = db.Column(db.Integer,primary_key=True)
    name = db.Column(db.String(20))

class Movie(db.Model):
    id = db.Column(db.Integer,primary_key=True)
    title = db.Column(db.String(20))
    year = db.Column(db.String(20))



# @app.route('/')
# def hello():
#     return 'Hello World!'


@app.context_processor
def inject_user():
    user = User.query.first()
    return dict(user=user)

@app.errorhandler(404)
def page_not_found(e):
    user = User.query.first()
    return render_template('404.html'), 404

@app.route('/index')
def index():
    user = User.query.first()
    movies = Movie.query.all()
    return render_template('index.html', movies=movies)


@app.cli.command()
def forge():
    db.create_all()
    name = 'Grey Li'
    movies = [
        {'title': 'My Neighbor Totoro', 'year': '1988'},
        {'title': 'Dead Poets Society', 'year': '1989'},
        {'title': 'A Perfect World', 'year': '1993'},
        {'title': 'Leon', 'year': '1994'},
        {'title': 'Mahjong', 'year': '1996'},
        {'title': 'Swallowtail Butterfly', 'year': '1996'},
        {'title': 'King of Comedy', 'year': '1999'},
        {'title': 'Devils on the Doorstep', 'year': '1999'},
        {'title': 'WALL-E', 'year': '2008'},
        {'title': 'The Pork of Music', 'year': '2012'},
    ]
    user = User(name=name)
    db.session.add(user)
    for item in movies:
        movie = Movie(title=item['title'],year=item['year'])
        db.session.add(movie)

    db.session.commit()
    click.echo('Dnoe')

# @app.route('/user/<name>')
# def user_page(name):
#     return '<h1>User Page</h1> %s' % name

# @app.route('/info')
# def info():
#     id = request.args.get('id')
#     return 'info:'+id

# @app.route('/test')
# def test_url_for():
#     print (url_for('hello'))
#     print(url_for('user_page', name='gremlin'))
#     print(url_for('user_page', name='peter'))
#     print(url_for('test_url_for'))
#     print(url_for('test_url_for', num=2))
#     return 'Test Page'






if __name__ == '__main__':
    app.run()

