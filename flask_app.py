from flask import Flask, render_template, request, redirect, url_for, flash, session
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
from dotenv import load_dotenv, dotenv_values
import os
import sys
import math

app = Flask(__name__)

config = dotenv_values(".env")
#print ( config['SQLALCHEMY_DATABASE_URI'])
#print (config['SQLALCHEMY_DATABASE_URI'])

# --- Configuration ---
# You'll need to set a strong secret key for session management.
# In a real application, get this from environment variables.
#app.config['SECRET_KEY'] = os.environ.get('app = Flask(__name__)
#config = dotenv_values(".env")
#print(config)', 'your_very_secret_key_here_please_change_this')

# MySQL Configuration for PythonAnywhere:
# This is a placeholder. You'll get your actual details from your PythonAnywhere MySQL tab.
# Example format: 'mysql+mysqlconnector://your_username:your_password@your_mysql_host/your_database_name'
# For PythonAnywhere, the host is usually your_username.mysql.pythonanywhere-services.com
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL', 'mysql+mysqlconnector://redsword:some-thing@redsword.mysql.pythonanywhere-services.com/redsword$SparSoftOne')
#app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL',default=None)
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] ="secret"

db = SQLAlchemy(app)

zeta_map_for_one_sided_alpha = {"0.01":2.3263479,"0.05":1.6448536,"0.1":1.2815516 }
zeta_map_for_one_sided_beta =  {"0.01":2.3263479, "0.05":1.6448536, "0.1":1.2815516,
        "0.15":1.0364334, "0.2":0.8416212, "0.25":0.6744898, "0.3":0.5244005 }
zeta_map_for_two_sided_alpha = {"0.01":2.575829,"0.05":1.959964,"0.1":1.6448536 }
zeta_map_for_two_sided_beta = { "0.01":2.3263479,"0.05":1.6448536,"0.1":1.2815516,
      "0.15":1.0364334, "0.2":0.8416212, "0.25":0.6744898, "0.3":0.5244005}

beta_complement_g = 0.0

# --- Database Model ---
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password_hash = db.Column(db.String(512), nullable=False) # Store hashed passwords

    def set_password(self, password):
        password_hash = generate_password_hash(password)
        length = len(password_hash)
        error_message = f"passwordhas ={self.password_hash}, len={length}"
        self.password_hash = password_hash


    def check_password(self, password):
        # error_message = f"password={password}"
        # print(error_message, file=sys.stderr)
        # flash(error_message)
        return check_password_hash(self.password_hash, password)

    def __repr__(self):
        return f'<User {self.username}>'

# --- Routes ---

@app.route('/')
def index():
    if 'username' in session:
        return render_template('index.html', username=session['username'])
    return render_template('index.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        if not username or not password:
            flash('Username and password are required.','error')
            return redirect(url_for('register'))

        existing_user = User.query.filter_by(username=username).first()
        if existing_user:
            flash('Username already exists. Please choose a different one.','error')
            return redirect(url_for('register'))

        new_user = User(username=username)
        new_user.set_password(password) # Hash the password
        db.session.add(new_user)
        db.session.commit()

        flash('Registration successful! Please log in.','success')
        return redirect(url_for('login'))
    return render_template('register.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if 'username' in session:
        return render_template('inputdata.html')
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        user = User.query.filter_by(username=username).first()

        if user and user.check_password(password):
            #error_message = f"user.username={user.username}"
            #print(error_message, file=sys.stderr)
            session['username'] = user.username
            #flash('Logged in successfully!','success')

            return render_template('inputdata.html')
        else:
            flash('Invalid username or password.','error')
    return render_template('login.html')

@app.route('/logout')
def logout():
    session.pop('username', None)
    flash('You have been logged out.','success')
    return redirect(url_for('index'))

@app.route('/inputdata', methods=['POST'])
def inputdata():
    # 'username' in session:
     #  return redirect(url_for('login'))
    flash('inputdata called')
    if request.method == 'POST':
        flash('POST  called')
        alpha = request.form['alpha']
        beta = request.form['beta']
        sigma_sqr = request.form['sigma_sqr']
        mu_0 = request.form['mu_0']
        mu_1 = request.form['mu_1']
        test_type = request.form['test_type']
        print(f"len(alpha) {len(alpha)} {isEmpty(alpha)} ",file=sys.stderr)
        if len(alpha) == 0: #or isEmpty(beta) or  isEmpty(sigma_sqr)  or isEmpty(mu_0) or isEmpty(mu_1):
            flash('all values should be entered','error')
            render_template('inputdata.html')

        print(f" vals alpha '{alpha}' beta '{beta}'  sigma_sqr '{sigma_sqr}' mu_0 '{mu_0}' mu_1 '{mu_1}' ",file=sys.stderr)
        return calculate(float(alpha),float(beta),int(sigma_sqr),int(mu_0),int(mu_1), int(test_type))
    return render_template('result.html')

def calculate(alpha:float,beta:float,sigma_sqr:int,mu_0:int,mu_1:int,test_type:int):
    print(f"inside calculate", file=sys.stderr)
    if test_type == 1:
        n = calc_test_one_sided(float(alpha),float(beta),int(sigma_sqr),
        int(mu_0),int(mu_1))
    elif test_type == 2:
        n = calc_test_two_sided(float(alpha),float(beta),int(sigma_sqr),
        int(mu_0),int(mu_1))
    return render_template('result.html', alpha=alpha, beta=beta,
      sigma_sqr=sigma_sqr,mu_0=mu_0,mu_1=mu_1,test_type=test_type,result=n, beta_complement=beta_complement_g)

def calc_test_one_sided(alpha:float,beta:float,sigma_sqr:int,mu_0:int,mu_1:int) -> int:
    try:
        key = str(alpha);
        print(f"Key '{alpha}'  key '{key}'")
        zeta_alpha = zeta_map_for_one_sided_alpha[key]
        print(f"Key '{alpha}'  found value '{zeta_alpha}'")
    except KeyError as ke1:
        print(f"Key '{key}'  not found in the map: {ke1}")
        return 0
    try:
        beta_complement_float = 1 - beta
        key = str(alpha);
        print(f"Key '{alpha}'  key '{key}'")
        zeta_alpha = zeta_map_for_one_sided_alpha[key]
        print(f"Key '{alpha}'  found value '{zeta_alpha}'")
    except KeyError as ke1:
        print(f"Key '{key}'  not found in the map: {ke1}")
        return 0
    try:
        beta_complement_float = 1 - beta
        print(f"beta_complement_float  '{beta_complement_float}'")
        beta_complement = round(beta_complement_float,ndigits=2)
        print(f"beta_complement  '{beta_complement}'")
        beta_complement_g = beta_complement
        print(f"beta_complement_g  '{beta_complement_g}'")
        key = str(beta_complement);
        print(f"beta  '{beta_complement}'  key '{key}'")
        zeta_beta = zeta_map_for_one_sided_beta[key]
        print(f"Key '{beta_complement}'  found value '{zeta_beta}'")
    except KeyError as ke2:
        print(f"Key '{beta}' not found in the map: {ke2}")
        return 0
    dividend = sigma_sqr*(zeta_alpha+zeta_beta)**2
    print(f"dividen '{dividend}' ")
    divisor =  (mu_1 - mu_0)**2
    print(f"divisor '{divisor}' ")
    return math.ceil(dividend/divisor)

    print(f"not sure what happend")
    return 0


    try:
        key = str(alpha);
        print(f"Key '{alpha}'  key '{key}'")
        zeta_alpha = zeta_map_for_one_sided_alpha[key]
        print(f"Key '{alpha}'  found value '{zeta_alpha}'")
    except KeyError as ke1:
        print(f"Key '{key}'  not found in the map: {ke1}")
        return 0
    try:
        beta_complement_float = 1 - beta
        print(f"beta_complement_float  '{beta_complement_float}'")
        beta_complement = round(beta_complement_float,ndigits=2)
        print(f"beta_complement  '{beta_complement}'")
        key = str(beta_complement);
        print(f"beta  '{beta_complement}'  key '{key}'")
        zeta_beta = zeta_map_for_one_sided_beta[key]
        print(f"Key '{beta_complement}'  found value '{zeta_beta}'")
    except KeyError as ke2:
        print(f"Key '{beta}' not found in the map: {ke2}")
        return 0
    dividend = sigma_sqr*(zeta_alpha+zeta_beta)**2
    print(f"dividen '{dividend}' ")
    divisor =  (mu_1 - mu_0)**2
    print(f"divisor '{divisor}' ")
    return math.ceil(dividend/divisor)

    print(f"not sure what happend")
    return 0


    try:
        key = str(alpha);
        print(f"Key '{alpha}'  key '{key}'")
        zeta_alpha = zeta_map_for_one_sided_alpha[key]
        print(f"Key '{alpha}'  found value '{zeta_alpha}'")
    except KeyError as ke1:
        print(f"Key '{key}'  not found in the map: {ke1}")
        return 0
    try:
        beta_complement_float = 1 - beta
        print(f"beta_complement_float  '{beta_complement_float}'")
        beta_complement = round(beta_complement_float,ndigits=2)
        print(f"beta_complement  '{beta_complement}'")
        key = str(beta_complement);
        print(f"beta  '{beta_complement}'  key '{key}'")
        zeta_beta = zeta_map_for_one_sided_beta[key]
        print(f"Key '{beta_complement}'  found value '{zeta_beta}'")
    except KeyError as ke2:
        print(f"Key '{beta}' not found in the map: {ke2}")
        return 0
    dividend = sigma_sqr*(zeta_alpha+zeta_beta)**2
    print(f"dividen '{dividend}' ")
    divisor =  (mu_1 - mu_0)**2
    print(f"dividen '{divisor}' ")
    return math.ceil(dividend/divisor)

    print(f"not sure what happend")
    return 0

def calc_test_two_sided(alpha:float,beta:float,sigma_sqr:int,mu_0:int,mu_1:int) -> int:

    try:
        key = str(alpha);
        print(f"Key '{alpha}'  key '{key}'")
        zeta_alpha = zeta_map_for_two_sided_alpha[key]
        print(f"Key '{alpha}'  found value '{zeta_alpha}'")
    except KeyError as ke1:
        print(f"Key '{key}'  not found in the map: {ke1}")
        return 0
    try:
        beta_complement_float = 1 - beta
        print(f"beta_complement_float  '{beta_complement_float}'")
        beta_complement = round(beta_complement_float,ndigits=2)
        print(f"beta_complement  '{beta_complement}'")
        key = str(beta_complement);
        print(f"beta  '{beta_complement}'  key '{key}'")
        zeta_beta = zeta_map_for_two_sided_beta[key]
        print(f"Key '{beta_complement}'  found value '{zeta_beta}'")
    except KeyError as ke2:
        print(f"Key '{beta}' not found in the map: {ke2}")
        return 0
    dividend = sigma_sqr*(zeta_alpha+zeta_beta)**2
    print(f"dividen '{dividend}' ")
    divisor =  (mu_1 - mu_0)**2
    print(f"dividen '{divisor}' ")
    return math.ceil(dividend/divisor)

    print(f"not sure what happend")
    return 0


    try:
        key = str(alpha);
        print(f"Key '{alpha}'  key '{key}'")
        zeta_alpha = zeta_map_for_one_sided_alpha[key]
        print(f"Key '{alpha}'  found value '{zeta_alpha}'")
    except KeyError as ke1:
        print(f"Key '{key}'  not found in the map: {ke1}")
        return 0
    try:
        beta_complement_float = 1 - beta
        print(f"beta_complement_float  '{beta_complement_float}'")
        beta_complement = round(beta_complement_float,ndigits=2)
        print(f"beta_complement  '{beta_complement}'")
        key = str(beta_complement);
        print(f"beta  '{beta_complement}'  key '{key}'")
        zeta_beta = zeta_map_for_one_sided_beta[key]
        print(f"Key '{beta_complement}'  found value '{zeta_beta}'")
    except KeyError as ke2:
        print(f"Key '{beta}' not found in the map: {ke2}")
    dividend = sigma_sqr*(zeta_alpha+zeta_beta)**2
    print(f"dividen '{dividend}' ")
    divisor =  (mu_1 - mu_0)**2
    print(f"dividen '{divisor}' ")
    return math.ceil(dividend/divisor)

    print(f"not sure what happend")
    return 0


    try:
        key = str(alpha);
        print(f"Key '{alpha}'  key '{key}'")
        zeta_alpha = zeta_map_for_one_sided_alpha[key]
        print(f"Key '{alpha}'  found value '{zeta_alpha}'")
    except KeyError as ke1:
        print(f"Key '{key}'  not found in the map: {ke1}")
        return 0
    try:
        beta_complement_float = 1 - beta
        print(f"beta_complement_float  '{beta_complement_float}'")
        beta_complement = round(beta_complement_float,ndigits=2)
        print(f"beta_complement  '{beta_complement}'")
        key = str(beta_complement);
        print(f"beta  '{beta_complement}'  key '{key}'")
        zeta_beta = zeta_map_for_one_sided_beta[key]
        print(f"Key '{beta_complement}'  found value '{zeta_beta}'")
    except KeyError as ke2:
        print(f"Key '{beta}' not found in the map: {ke2}")
        return 0
    dividend = sigma_sqr*(zeta_alpha+zeta_beta)**2
    print(f"dividen '{dividend}' ")
    divisor =  (mu_1 - mu_0)**2
    print(f"dividen '{divisor}' ")
    return math.ceil(dividend/divisor)

    print(f"not sure what happend")
    return 0

def isEmpty(input:str):
    return len(input.strip()) == 0

def calculate_critical_values(levels: list[float], half_level: bool = False) -> list[float]:
    """
    Calculates critical values from a list of significance levels using the inverse
    cumulative distribution function (quantile function) of the standard normal distribution.

    This function is equivalent to R's qnorm(level, lower.tail=F) or qnorm(level/2, lower.tail=F).

    Args:
        levels (list[float]): A list of significance levels (alpha values), e.g., [0.01, 0.05, ...].
                              These values represent the probability in the upper tail.
        half_level (bool, optional): If True, each level will be divided by 2 before
                                     calculating the critical value. This is typically
                                     used for two-tailed tests where the alpha level
                                     is split equally between the two tails.
                                     Defaults to False (for a one-tailed test).

    Returns:
        list[float]: A list of calculated critical values. Each value corresponds to
                     the point on the standard normal distribution curve beyond which
                     the specified (or halved) probability lies in the upper tail.
    """
    critical_values = []
    for level_val in levels:
        # If half_level is True, we divide the significance level by 2.
        # Otherwise, we use the level as is.
        effective_level = level_val / 2 if half_level else level_val

        # In R's qnorm(prob, lower.tail=F), 'prob' is the probability in the upper tail.
        # scipy.stats.norm.ppf(q) expects 'q' as the cumulative probability (P(X <= x)).
        # So, if 'effective_level' is the upper tail probability, the cumulative
        # probability 'q' is 1 - effective_level.
        cumulative_probability = 1 - effective_level

        critical_values.append(norm.ppf(cumulative_probability))

    return critical_values

# Define the list of significance levels
# levels_data = [0.01, 0.05, 0.10, 0.15, 0.20, 0.25, 0.30]

# print("--- Calculating Critical Values (One-Tailed, equivalent to R's qnorm(Level[i], lower.tail=F)) ---")
#  Call the function for a one-tailed test (half_level=False)
# critical_one_tail = calculate_critical_values(levels_data, half_level=False)
# for i, level in enumerate(levels_data):
#     print(f"Level: {level:.2f}, Critical Value: {critical_one_tail[i]:.4f}")

# print("\n--- Calculating Critical Values (Two-Tailed, equivalent to R's qnorm((Level/2)[i], lower.tail=F)) ---")
#  Call the function for a two-tailed test (half_level=True)
# critical_two_tail = calculate_critical_values(levels_data, half_level=True)
# for i, level in enumerate(levels_data):
#     print(f"Level: {level:.2f}, Critical Value: {critical_two_tail[i]:.4f}")

# --- Run the app ---
if __name__ == '__main__':
    # Create tables if they don't exist
    with app.app_context():
        db.create_all()
    app.run(debug=True) # debug=True for development, set to False for production
