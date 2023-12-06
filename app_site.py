import requests
from bs4 import BeautifulSoup
import hashlib
from flask import Flask, render_template, abort
import webbrowser # Import the webbrowser module

app = Flask(__name__)

# Function to calculate MD5 hashing of a string
def password_md5(s):
    return hashlib.md5(s.encode()).hexdigest()

# Function to perform login
def perform_login(session, username, password):
    # Replace with your actual login URL
    submit_url = 'http://192.168.1.2/Forms/login_security_1.html'
    # Prepare login data
    login_data = {
        'Login_Name' : password_md5(username),
        'Login_Pwd' : password_md5(password),
    }
    # Send a POST request to the login endpoint
    response = session.post(submit_url, data=login_data, allow_redirects=True)
    #Check if there is a redirect
    if response.is_redirect:
        redirect_url = response.headers['Location']
        print(redirect_url)
        webbrowser.open(redirect_url) # Open the redirected URL in the default web browser
        # Follow the redirect manually
        response = session.get(redirect_url)
    
    # Check if login was successful (you might need to adjust this based on the actual response)
    if 'The username or password is incorrect,please input again.' in response.text:
        print('Login failed')
        return False
    else:
        print('Login successful')
        return True

# Function to scrape connected devices data
def scrape_connected_devices(session):
     #Replace the URL with the actual URL for connected devices data
    connected_devices_urls = [
        'http://192.168.1.2/rpSys.html',
        'http://192.168.1.2/status.html',
        'http://192.168.1.2/navigation-status.html',
        'http://192.168.1.2/status/status_deviceinfo.html',
        'http://192.168.1.2/css/style.css',
        'http://192.168.1.2/js/general.js',
        'http://192.168.1.2/Images/Logo.gif',
        'http://192.168.1.2/Images/tb3.gif'
    ]
    html_content = ""
    # Send a GET request to the connected devices page
    for url in connected_devices_urls:
        response = session.get(url)
        html_content += response.text

    # Parse the HTML content
    soup = BeautifulSoup(html_content, 'html.parser')
    #Extract connected devices data (modify this based on the actual structure of the page)
    connected_devices_data = soup.prettify()
    return connected_devices_data

# Route for displaying router data
@app.route('/connected_devices')
def display_connected_devices():
    # Create a session
    session = requests.Session()

    #set your login credentials
    your_username = 'admin'
    your_password = 'Shesh72246'

    #Perform login
    if perform_login(session, your_username, your_password):
        #If login is successful, proceed to scrape connected devices data
        data = scrape_connected_devices(session)
        return render_template('connected_devices.html', connected_devices_table=str(data))
    else:
        # If login fails, return an error response
        abort(401, 'Login failed. Check your credentials and URL.')

# Route for displaying router data
@app.route('/router_data')
def display_router_data():
    # Create a session
    session = requests.Session()

    # Set your login credentials
    your_username = 'admin'
    your_password = 'Shesh@72246'

    # Perform login
    if perform_login(session, your_username, your_password):
        # If login is successful, proceed to scrape router data
        data = scrape_router_data(session)
        return render_template('index.html', router_data=str(data))
    else:
        # If login fails, return an error response
        abort(401, 'Login failed. Check your credentials and URL.')

# Function to scrape router data
def scrape_router_data(session):
    router_data_url = 'http://192.168.1.2/rpSys.html'  # Replace with your actual router data URL

    # Send a GET request to the router data page
    response = session.get(router_data_url)

    # Parse the HTML content
    soup = BeautifulSoup(response.text, 'html.parser')

    # Extract and print router data
    router_data = soup.find('pre').text
    return router_data

# Run the app if this script is executed
if __name__ == '__main__':
    app.run(host='192.168.1.100', port=80, debug=False)