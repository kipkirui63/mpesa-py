from flask import Flask, request, render_template,send_from_directory
import json
import requests
import datetime
import base64

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/images/<path:filename>')
def images(filename):
    return send_from_directory('static/images', filename)

# @app.route('/make_payment', methods=['POST'])
# def make_payment():
#     if request.method == 'POST':
#         # Handle the M-PESA payment logic here.
#         # You can use the provided Python code for M-PESA integration.
#         # Process the payment and return a response to the user.

#         # For example:
#         amount = request.form.get('amount')
#         phone = request.form.get('phone')
#         # Perform payment processing here

#         # Respond with a success or failure message
#         response = "Payment Successful"  # Replace with your logic

#         return response



# @app.route('/mpesa_confirmation', methods=['POST'])
# def mpesa_confirmation():
#     response = {
#         "ResultCode": 0,
#         "ResultDesc": "Confirmation Received Successfully"
#     }

#     # Data
#     mpesa_response = request.data.decode('utf-8')

#     # Log the response
#     log_file = "M_PESAConfirmationResponse.txt"

#     with open(log_file, "a") as log:
#         log.write(mpesa_response)

#     return json.dumps(response), 200, {'Content-Type': 'application/json'}


# @app.route('/make_payment', methods=['POST'])
# def make_payment():
#     if request.method == 'POST':
#         consumer_key = 'QpSLa082LRAOeJBlOTsZYkvoBslMBfVC'  # Replace with your M-PESA API Consumer Key
#         consumer_secret = 'GG9NK7lLTEtztDa0'  # Replace with your M-PESA API Consumer Secret
#         business_short_code = 'YourBusinessShortCode'  # Replace with your Business Short Code
#         passkey = 'YourPasskey'  # Replace with your M-PESA Passkey
#         callback_url = 'https://your-callback-url.com/callback'  # Replace with your callback URL
#         # Handle the M-PESA payment logic here.
        
#         # Retrieve user input
#         amount = request.form.get('amount')
#         phone = request.form.get('phone')

#         # Continue with the M-PESA integration code
#         timestamp = datetime.datetime.now().strftime('%Y%m%d%H%M%S')
#         data_to_encode = business_short_code + passkey + timestamp
#         password = base64.b64encode(data_to_encode.encode()).decode('utf-8')

#         # access_token_url = 'https://sandbox.safaricom.co.ke/oauth/v1/generate?grant_type=client_credentials'
#         # access_token_headers = {
#         #     'Content-Type': 'application/json',
#         # }
#         access_token_data = {
#             'consumer_key': consumer_key,
#             'consumer_secret': consumer_secret,
#         }
#        # Obtain an access token
#         access_token_response = requests.get('https://sandbox.safaricom.co.ke/oauth/v1/generate?grant_type=client_credentials', headers={'Authorization': 'Bearer cFJZcjZ6anEwaThMMXp6d1FETUxwWkIzeVBDa2hNc2M6UmYyMkJmWm9nMHFRR2xWOQ=='})
#         access_token_data = access_token_response.json()
#         access_token = access_token_data.get('access_token')


#         initiate_url = 'https://sandbox.safaricom.co.ke/mpesa/stkpush/v1/processrequest'
#         initiate_headers = {
#             'Content-Type': 'application/json',
#             'Authorization': 'Bearer ' + access_token,
#         }
#         initiate_data = {
#             'BusinessShortCode': business_short_code,
#             'Password': password,
#             'Timestamp': timestamp,
#             'TransactionType': 'CustomerPayBillOnline',
#             'Amount': amount,
#             'PartyA': phone,
#             'PartyB': business_short_code,
#             'PhoneNumber': phone,
#             'CallBackURL': callback_url,
#             'AccountReference': '2255',
#             'TransactionDesc': 'Test Payment',
#         }

#         initiate_response = requests.post(initiate_url, headers=initiate_headers, json=initiate_data)
#         response_data = initiate_response.json()

#         # Process the response data and return a success or failure message
#         # Replace the following with your own logic
#         if response_data.get('ResponseCode') == '0':
#             return "Payment Successful"
#         else:
#             return "Payment Failed"



@app.route('/make_payment', methods=['POST'])
def make_payment():
    if request.method == 'POST':
        consumer_key = 'QpSLa082LRAOeJBlOTsZYkvoBslMBfVC'  # Replace with your M-PESA API Consumer Key
        consumer_secret = 'GG9NK7lLTEtztDa0'  # Replace with your M-PESA API Consumer Secret
        business_short_code = 'YourBusinessShortCode'  # Replace with your Business Short Code
        passkey = 'YourPasskey'  # Replace with your M-PESA Passkey
        callback_url = 'https://your-callback-url.com/callback'  # Replace with your callback URL

        amount = request.form.get('amount')
        phone = request.form.get('phone')

        timestamp = datetime.datetime.now().strftime('%Y%m%d%H%M%S')
        data_to_encode = business_short_code + passkey + timestamp
        password = base64.b64encode(data_to_encode.encode()).decode('utf-8')

        access_token_url = 'https://sandbox.safaricom.co.ke/oauth/v1/generate?grant_type=client_credentials'
        access_token_headers = {
            'Content-Type': 'application/json',
        }
        access_token_data = {
            'consumer_key': consumer_key,
            'consumer_secret': consumer_secret,
        }

        # Attempt to obtain an access token
        access_token_response = requests.get(access_token_url, headers=access_token_headers, params=access_token_data)

        if access_token_response.status_code == 200:
            access_token_data = access_token_response.json()
            access_token = access_token_data.get('access_token')

            if access_token:
                initiate_url = 'https://sandbox.safaricom.co.ke/mpesa/stkpush/v1/processrequest'
                initiate_headers = {
                    'Content-Type': 'application/json',
                    'Authorization': 'Bearer ' + access_token,
                }
                initiate_data = {
                    'BusinessShortCode': business_short_code,
                    'Password': password,
                    'Timestamp': timestamp,
                    'TransactionType': 'CustomerPayBillOnline',
                    'Amount': amount,
                    'PartyA': phone,
                    'PartyB': business_short_code,
                    'PhoneNumber': phone,
                    'CallBackURL': callback_url,
                    'AccountReference': '2255',
                    'TransactionDesc': 'Test Payment',
                }

                initiate_response = requests.post(initiate_url, headers=initiate_headers, json=initiate_data)
                response_data = initiate_response.json()

                if response_data.get('ResponseCode') == '0':
                    return "Payment Successful"
                else:
                    return "Payment Failed"
            else:
                return "Access token not received"

        else:
            return "Access token request failed"

if __name__ == '__main__':
    app.run(debug=True)





