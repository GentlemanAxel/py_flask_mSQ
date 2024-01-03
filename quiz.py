# quiz.py
from flask import Flask, render_template, redirect, url_for, request, flash, session
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, UserMixin, login_user, logout_user, login_required, current_user
from werkzeug.security import generate_password_hash, check_password_hash
import random
from datetime import datetime, timedelta
import json

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'
app.secret_key = '32cookies'

db = SQLAlchemy(app)

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'


class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100), unique=True)
    password = db.Column(db.String(100))
    score = db.Column(db.Integer, default=0)
    is_banned = db.Column(db.Boolean, default=False)
    is_admin = db.Column(db.Boolean, default=False)


@app.before_request
def before_request():
    request.environ['wsgi.url_scheme'] = 'https'


@app.route('/admin')
@login_required
def admin_panel():
    with open('admin_users.json', 'r') as admin_file:
        admin_users = json.load(admin_file)

    if current_user.is_authenticated and current_user.username in admin_users:
        users = User.query.all()
        return render_template('admin_panel.html', users=users)
    else:
        return redirect(url_for('home'))


@app.route('/unban', methods=['POST'])
@login_required
def unban_user():
    with open('admin_users.json', 'r') as admin_file:
        admin_users = json.load(admin_file)

    if current_user.is_authenticated and current_user.username in admin_users:
        user_id_to_unban = request.form.get('user_id_to_unban')

        if user_id_to_unban:
            user_to_unban = User.query.get(user_id_to_unban)

            if user_to_unban:
                user_to_unban.is_banned = False
                user_to_unban.ban_reason = None
                user_to_unban.ban_expiration_time = None
                db.session.commit()
                flash(f'User {user_to_unban.username} has been unbanned.')

    return redirect(url_for('admin_panel'))


@app.route('/ban/<int:user_id>', methods=['POST'])
@login_required
def ban_user(user_id):
    with open('admin_users.json', 'r') as admin_file:
        admin_users = json.load(admin_file)

    if current_user.is_authenticated and current_user.username in admin_users:
        user = User.query.get(user_id)
        if user:
            user.is_banned = True
            user.ban_reason = request.form.get('reason')
            ban_days = request.form.get('ban_days')
            print(user.ban_reason, ban_days)

            if ban_days:
                try:
                    ban_days = int(ban_days)
                    expiration_time = datetime.now() + timedelta(days=ban_days)
                except ValueError:
                    expiration_time = None
            else:
                expiration_time = None

            user.ban_expiration_time = expiration_time
            db.session.commit()
            flash(f'User {user.username} has been banned.')

        return redirect(url_for('admin_panel'))


@app.route('/banned')
def banned():
    if current_user.is_authenticated and current_user.is_banned:
        return render_template('account_banned.html', current_time=datetime.now())
    else:
        return redirect(url_for('home'))


@app.route('/complain', methods=['GET', 'POST'])
@login_required
def complain():
    if request.method == 'POST':
        # todo : Handle the complaint submission.

        flash('Your complaint has been submitted. We will review it soon.')
        return render_template('account_banned.html', current_time=datetime.now())

    return render_template('complain.html')


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


@app.route('/')
def home():
    session.pop('points', None)
    return render_template('home.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')

        user = User.query.filter_by(username=username).first()

        if not user or not check_password_hash(user.password, password):
            flash('Please check your login details and try again.')
            return redirect(url_for('login'))

        with open('admin_users.json', 'r') as admin_file:
            admin_users = json.load(admin_file)

        if username in admin_users:
            user.is_admin = True
            db.session.commit()

        login_user(user)
        return redirect(url_for('profile'))

    return render_template('login.html')


@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')

        user = User.query.filter_by(username=username).first()

        if user:
            flash('Username already exists.')
            return redirect(url_for('register'))

        with open('admin_users.json', 'r') as admin_file:
            admin_users = json.load(admin_file)

        new_user = User(username=username, password=generate_password_hash(password, method='sha256'))

        if username in admin_users:
            new_user.is_admin = True

        db.session.add(new_user)
        db.session.commit()

        login_user(new_user)
        return redirect(url_for('profile'))

    return render_template('register.html')


@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('home'))


@app.route('/profile')
@login_required
def profile():
    return render_template('profile.html')


# La liste des symboles mathématiques et leur signification
symbols = {
    'Intégrale': '∫',  # Intégrale
    'Intégrale de flux': '∮',  # Intégrale de flux
    'Identique à': '≡',  # Identique à
    "Il n'existe pas": '∄',  # Il n'existe pas
    'Symbole somme': '∑',  # Symbole somme
    'Appartient': '∈',  # Appartient
    'Entier naturel (0,1,2,3…)': 'ℕ',  # Entier naturel (0,1,2,3…)
    'Privé de 0': '*',  # Privé de 0
    'Entier (positif ou négatif)': 'ℤ',  # Entier (positif ou négatif)
    'Ensemble des nombres pouvant être écrits sous forme d’un quotient': 'ℚ',  # Ensemble des nombres pouvant être écrits sous forme d’un quotient
    'Ensemble des nombres réels': 'ℝ',  # Ensemble des nombres réels
    'Ensemble des nombres complexes': 'ℂ',  # Ensemble des nombres complexes
    'Pour tout': '∀',  # Pour tout
    'Il existe': '∃',  # Il existe
    'N’appartient pas': '∉',  # N’appartient pas
    'Inclus': '⊂',  # Inclus
    'Non-inclus': '⊄',  # Non-inclus
    'Ensemble vide': 'Ø',  # Ensemble vide
    'Implique': '⇒',  # Implique
    'Equivalent': '⇔',  # Équivalent
    'Inter': '∩',  # Intersection
    'Union': '∪',  # Union
    'Infini': '∞',  # Infini
    'Limites': 'Lim',  # Limites
    'Modulo': '[ ]',  # Modulo
    'Perpendiculaire': '⊥'  # Perpendiculaire
}


def generate_question():
    meaning = random.choice(list(symbols.keys()))
    symbol = symbols[meaning]
    options = list(symbols.values())
    random.shuffle(options)
    while options.index(symbol) > 4:
        random.shuffle(options)
    options = options[:5]
    return symbol, meaning, options


@app.route('/test', methods=['GET', 'POST'])
@login_required
def test():
    if request.method == 'GET':
        session['points'] = 0

    if request.method == 'POST' and 'points' not in session:
        session['points'] = 0

    if request.method == 'POST':
        user_answer = request.form['answer']
        user_meaning = next(meaning for meaning, symbol in symbols.items() if symbol == user_answer)
        correct_meaning = request.form.get('meaning')
        is_correct = user_meaning == correct_meaning

        if is_correct:
            session['points'] += 3
            feedback = "Bonne réponse !"
        else:
            session['points'] -= 2
            feedback = f"Mauvaise réponse. Le symbole correct était : {symbols[correct_meaning]}"

    else:
        feedback = None

    symbol, meaning, options = generate_question()
    points = session.get('points', 0)
    return render_template('test.html', symbol=symbol, meaning=meaning, options=options, feedback=feedback, points=points)


@app.route('/statistics')
@login_required
def statistics():
    users = User.query.order_by(User.score.desc()).all()
    rank = users.index(current_user) + 1
    return render_template('statistics.html', score=current_user.score, rank=rank)


if __name__ == "__main__":
    with app.app_context():
        db.create_all()
    app.run(debug=True)
