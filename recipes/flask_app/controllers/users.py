
from flask import redirect, render_template, session, request
from flask_app import app
from flask_app.models.user import User
from flask_bcrypt import Bcrypt
bcrypt = Bcrypt(app)

@app.route('/')
def index():
        return render_template("index.html")


@app.route('/register', methods=['POST'])
def register():
    if not User.validate_registration(request.form):
        return redirect('/')

    data = {
        "first_name": request.form["first_name"],
        "last_name": request.form["last_name"],
        "email": request.form["email"],
        "password": bcrypt.generate_password_hash(request.form['password'])
    }
    id = User.save_user(data)
    session['user_id'] = id
    return redirect('/recipes/home')

@app.route("/login", methods=["POST"])
def login():
    active_user = User.get_user_by_email(request.form)
    if not active_user:
        return redirect('/')
    session['user_id'] = active_user.id
    return redirect('/recipes/home')


@app.route('/logout')
def logout():
    session.clear()
    return redirect('/')