from flask import Flask, render_template, flash, redirect
from markupsafe import escape
from forms import RegistrarionForm, LoginForm

posts = [
    {
        'author': 'Ivan',
        'title': 'Post 1',
        'content': '1',
        'date_posted': 'April 20, 1997'
    },
    {
        'author': 'Tim',
        'title': 'Post 2',
        'content': '2',
        'date_posted': 'April 20, 2022'
    },
]

app = Flask(__name__)

app.config['SECRET_KEY'] = 'bc1e17893f8b6b2cd35c5d73fee1124e'

from flask import url_for

@app.route('/')
@app.route("/home")
def home():
    return render_template('home.html', posts=posts)

@app.route('/about')
def about():
    return render_template('about.html', title = "About ")

@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegistrarionForm()
    if form.validate_on_submit():
        flash(f"{form.username.data}, you are signed up!", 'Success')
        return redirect(url_for('home'))
    return render_template('register.html', title="register", form=form)

@app.route('/login')
def login():
    form = LoginForm()
    return render_template('login.html', title="login", form=form)

@app.route('/post')
def post():
    return render_template('post.html', title="Post", posts=posts[0])

@app.route('/create_post')
def create_post():
    return render_template('create_post.html', title="Post creation")

if __name__ == "__main__":
    app.run(debug=True)

