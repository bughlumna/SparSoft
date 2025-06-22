
# A very simple Flask Hello World app for you to get started with...

from flask import Flask, render_template, request
import math
app = Flask(__name__)


zeta_map_for_one_sided_alpha = {"0.01":2.3263479,"0.05":1.6448536,"0.1":1.2815516 }
zeta_map_for_one_sided_beta =  {"0.01":2.3263479, "0.05":1.6448536, "0.1":1.2815516, "0.15":1.0364334, "0.2":0.8416212, "0.25":0.6744898, "0.3":0.5244005 }
zeta_map_for_two_sided_alpha = {"0.01":2.575829,"0.05":1.959964,"0.1":1.6448536 }
zeta_map_for_two_sided_beta = { "0.01":2.3263479,"0.05":1.6448536,"0.1":1.2815516,
      "0.15":1.0364334, "0.2":0.8416212, "0.25":0.6744898, "0.3":0.5244005}

beta_complement_g = 0.0
@app.route('/')
# ‘/’ URL is bound with hello_world() function.
def hello_world():
    return 'Hello World'

@app.route('/calc', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        alpha = request.form['alpha']
        beta = request.form['beta']
        sigma_sqr = request.form['sigma_sqr']
        mu_0 = request.form['mu_0']
        mu_1 = request.form['mu_1']
        test_type = request.form['test_type']
        print(f" vals alpha '{alpha}' beta '{beta}'  sigma_sqr '{sigma_sqr}' mu_0 '{mu_0}' mu_1 '{mu_1}' ")
        #return calculate(float(alpha),float(beta),int(sigma_sqr),int(mu_0),int(mu_1), int(test_type))
    return render_template('form.html')
# def index():
#     if request.method == 'POST'|| request.method == 'GET':
#         alpha = request.form['alpha']
#         beta = request.form['beta']
#         sigma_sqr = request.form['sigma_sqr']
#         mu_0 = request.form['mu_0']
#         mu_1 = request.form['mu_1']
#         test_type = request.form['test_type']
#         print(f" vals alpha '{alpha}' beta '{beta}'  sigma_sqr '{sigma_sqr}' mu_0 '{mu_0}' mu_1 '{mu_1}' ")
#         return calculate(float(alpha),float(beta),int(sigma_sqr),
#         int(mu_0),int(mu_1), int(test_type))
#     return render_template('form.html')

def calculate(alpha:float,beta:float,sigma_sqr:int,mu_0:int,mu_1:int,test_type:int):
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
        return 0
    dividend = sigma_sqr*(zeta_alpha+zeta_beta)**2
    print(f"dividen '{dividend}' ")
    divisor =  (mu_1 - mu_0)**2
    print(f"dividen '{divisor}' ")
    return math.ceil(dividend/divisor)

    print(f"not sure what happend")
    return 0

def calc_test_two_sided1(alpha:float,beta:float,sigma_sqr:int,mu_0:int,mu_1:int) -> int:
    beta_complement = 1 - beta
    try:
        zeta_alpha = zeta_map_for_two_sided_alpha[alpha]
        zeta_beta = zeta_map_for_two_sided_beta[beta_complement]
        dividend = sigma_sqr*(zeta_alpha+zeta_beta)^2
        print(f"dividend '{dividend}'")
        divisor =  (mu_1 - mu_0)^2
        print(f"divisor '{divisor}'")
        return math.ceil(dividend/divisor)
    except KeyError as keyError:
        print(f"Key '{alpha}' or '{beta}' not found in the map: {keyError}")
        return 0
    except Exception as generalError:
        print(f"An error occurred: {generalError}")
        return 0
    print(f"not sure what happend")
    return 0


if __name__ == '__main__':
    app.run(debug=True)

