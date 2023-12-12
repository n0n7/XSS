# create basic todo list website using flask

from flask import Flask, render_template, request, redirect, url_for
from firebase_config import auth
from firebase_admin.auth import UserNotFoundError
from flask_login import login_user, login_required, logout_user, current_user, LoginManager
from flask_session import Session
from user import User

app = Flask(__name__)

app.config['SESSION_TYPE'] = 'filesystem'
app.config['SESSION_PERMANENT'] = False
app.config['SESSION_USE_SIGNER'] = True
app.config['SECRET_KEY'] = 'your_secret_key'
app.config['SESSION_COOKIE_HTTPONLY'] = False
Session(app)

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

@login_manager.user_loader
def load_user(user_id):
    try:
        user = auth.get_account_info(user_id)
        email = user['users'][0]['email']
        # Create a user object and return it
        return User(user_id, email)
    except Exception as e:
        return None

# use text file data.txt for storing tasks
with open('./TodoList/data.txt', 'r') as f:
    tasks = f.read().split('\n')
    tasks = [task for task in tasks if task != '']

# save tasks to text file
def save_tasks():
    with open('./TodoList/data.txt', 'w') as f:
        f.write('\n'.join(tasks))

# home page
@app.route('/')
@login_required
def home():
    return render_template('home.html', tasks=tasks, email=current_user.get_email())

# add task
@app.route('/add', methods=['GET', 'POST'])
@login_required
def add():
    if request.method == 'POST':
        task = request.form['task']
        tasks.append(task)
        save_tasks()
        return redirect(url_for('home'))
    return render_template('add.html', email=current_user.get_email())

# delete task
@app.route('/delete/<int:index>')
def delete(index):
    del tasks[index]
    save_tasks()
    return redirect(url_for('home'))

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        error_message = ""

        try:
            user = auth.create_user_with_email_and_password(email=email, password=password)
            # You can customize user registration logic here (e.g., updating user profiles)
            return redirect(url_for('login'))
        except Exception as e:
            error_message = str(e)

        return render_template('register.html', error_message=error_message)
    
    if request.method == 'GET':
        if current_user.is_authenticated:
            return redirect(url_for('home'))
        return render_template('register.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        error_message = ""

        try:
            user = auth.sign_in_with_email_and_password(email, password)
            user = User( user['idToken'], email)
            login_user(user)
            return redirect(url_for('home'))
        except Exception as e:
            error_message = str(e)


        return render_template('login.html', error_message=error_message)
    
    if request.method == 'GET':
        if current_user.is_authenticated:
            return redirect(url_for('home'))
        return render_template('login.html')
    
@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('login'))


if __name__ == '__main__':
    app.run(debug=True)