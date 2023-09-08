from flask import Flask, render_template, request, redirect, jsonify
from flask import redirect, request, url_for
import subprocess
from object.payment_info import PaymentInfo


app = Flask(__name__)

selected_wallet_name = ""

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/get_status', methods=['POST'])
def get_status():
    try:
        command = 'curl -s --data-binary \'{"jsonrpc":"2.0","id":"1","method":"getstatus"}\' http://127.0.0.1:37128/ | jq'
        result = subprocess.run(command, shell=True, capture_output=True, text=True)
        json_output = result.stdout
        return json_output
    except Exception as e:
        print(f"Error: {e}")
        return "An error occurred while processing the request.", 500

@app.route('/create_wallet', methods=['GET', 'POST'])
def create_wallet():
    if request.method == 'POST':
        wallet_name = request.form['wallet_name']
        user_password = request.form['user_password']

        try:
            command = f'curl -s --data-binary \'{{"jsonrpc":"2.0","id":"1","method":"createwallet","params":["{wallet_name}", "{user_password}"]}}\' http://127.0.0.1:37128/ | jq'
            result = subprocess.run(command, shell=True, capture_output=True, text=True)
            json_output = result.stdout

            return redirect(url_for('index'))  # Redirect to the index page with POST method
        except Exception as e:
            print(f"Error: {e}")
            return "An error occurred while creating the wallet.", 500

    return render_template('createwallet.html')


@app.route('/get_wallet_info', methods=['POST'])
def get_wallet_info():
    try:
        command = 'curl -s --data-binary \'{"jsonrpc":"2.0","id":"1","method":"getwalletinfo"}\' http://127.0.0.1:37128/ | jq'
        result = subprocess.run(command, shell=True, capture_output=True, text=True)
        json_output = result.stdout
        print(f"Output: {json_output}")
        return json_output
    except Exception as e:
        print(f"Error: {e}")
        return "An error occurred while processing the request.", 500
    
@app.route('/select_wallet', methods=['GET', 'POST'])
def select_wallet():
    if request.method == 'POST':
        wallet_name = request.form['wallet_name']
        global selected_wallet_name
        selected_wallet_name = wallet_name
        try:
            command = f'curl -s --data-binary \'{{"jsonrpc":"2.0","id":"1","method":"selectwallet","params":["{wallet_name}", "true"]}}\' http://127.0.0.1:37128/ | jq'
            result = subprocess.run(command, shell=True, capture_output=True, text=True)
            json_output = result.stdout
      
            return redirect(url_for('index'))  # Redirect to the index page with POST method
        except Exception as e:
            print(f"Error: {e}")
            return "An error occurred while creating the wallet.", 500

    return render_template('selectwallet.html')    

@app.route('/generate_new_address', methods=['POST'])
def generate_new_address():
    try:
        global selected_wallet_name
        command = f'curl -s --data-binary \'{{"jsonrpc":"2.0","id":"1","method":"getnewaddress","params":["Command line"]}}\' http://127.0.0.1:37128/{selected_wallet_name} | jq'
        result = subprocess.run(command, shell=True, capture_output=True, text=True)
        if result.returncode == 0:
            json_output = result.stdout.strip()
            return json_output
        else:
            return 'Failed to generate new address', 500
    except Exception as e:
        print(f"Error: {e}")
        return "An error occurred while generating a new address.", 500
    
@app.route('/send', methods=['GET', 'POST'])
def send():
    if request.method == 'POST':
        payments = PaymentInfo()

        payments.Sendto = request.form['bitcoin_address']
        payments.Amount = request.form['amount']
        payments.Label = request.form['label']

        coins = []
        coins.append(request.form['outpoint'])

        feeTarget = 1

        password = "1234"


        try:
            command = f'curl -s --data-binary \'{{"jsonrpc":"2.0","id":"1","method":"send","params":["{payments}", "{coins}", "{feeTarget}", "{password}"]}}\' http://127.0.0.1:37128/ | jq'
            result = subprocess.run(command, shell=True, capture_output=True, text=True)
            json_output = result.stdout

            return redirect(url_for('index'))  # Redirect to the index page with POST method
        except Exception as e:
            print(f"Error: {e}")
            return "An error occurred while creating the wallet.", 500

    return render_template('send.html')    

@app.route('/list_unspent_coins', methods=['POST'])
def list_unspent_coins():
    try:
        global selected_wallet_name
        command = f'curl -s --data-binary \'{{"jsonrpc":"2.0","id":"1","method":"listunspentcoins"}}\' http://127.0.0.1:37128/{selected_wallet_name} | jq'
        result = subprocess.run(command, shell=True, capture_output=True, text=True)
        json_output = result.stdout
        return json_output
    except Exception as e:
        print(f"Error: {e}")
        return "An error occurred while processing the request.", 500  
    
@app.route('/list_coins', methods=['POST'])
def list_coins():
    try:
        global selected_wallet_name
        command = f'curl -s --data-binary \'{{"jsonrpc":"2.0","id":"1","method":"listcoins"}}\' http://127.0.0.1:37128/{selected_wallet_name} | jq'
        result = subprocess.run(command, shell=True, capture_output=True, text=True)
        json_output = result.stdout
        return json_output
    except Exception as e:
        print(f"Error: {e}")
        return "An error occurred while processing the request.", 500    

if __name__ == '__main__':
    app.run(debug=True)
