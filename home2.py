import os, requests
from bs4 import BeautifulSoup
from flask import Flask, render_template, send_from_directory
import hashlib
import time

app = Flask(__name__)

# Function to calculate MD5 hashing of a string
def password_md5(s):
    return hashlib.md5(s.encode()).hexdigest()

# Function to perform login
def perform_login(session, username, password):
    # Replace with your actual login URL
    router_url = 'http://192.168.1.2'

    #Define headers
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/118.0.0.0 Safari/537.36'
    }
    response = session.get(router_url, headers=headers, allow_redirects=False)
    #Check if there is a redirect
    if response.is_redirect:
        redirect_url = response.headers['Location']
        # Follow the redirect manually
        #print("Redirection url = ", redirect_url)
        response = session.get(redirect_url, headers=headers)
        time.sleep(2) # Add a delay to ensure any dynamic content is loaded.
    else:
        redirect_url = router_url
   
   # print("Redirection URL = ", redirect_url)
    login_url = 'http://192.168.1.2/login_security.html'
    # Prepare login data
    login_data = {
        'Login_Name' : username,
        'Login_Pwd' : password,
        'texttpLoginBtn' : 'Login'  # Adjust this based on the actual name of the login button
    }
        # Send a POST request to the login endpoint
    headers1 = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/118.0.0.0 Safari/537.36',
        'Referer': 'http://192.168.1.2',
    }
    response = session.post(login_url, data=login_data, headers=headers1, allow_redirects=False)
    #print(response.text)
    #if 'You have exceeded five attempts' not in response.text:
    # Check if the server sets any cookies
    if session.cookies:
        print("Cookies:")
        for cookie in session.cookies:
            print(f"{cookie.name}: {cookie.value}")

    # You can then access a specific cookie using its name, for example:
    # if 'your_session_cookie_name' in session.cookies:
    #     print(f"Found session cookie: {session.cookies['your_session_cookie_name'].value}")
    else:
        print('No cookies found.')
    
    if response.is_redirect:
        redirect_url = response.headers['Location']
        # Follow the redirect manually
        print("Redirection url = ", redirect_url)
        response = session.get(redirect_url, headers=headers1)
        time.sleep(2) # Add a delay to ensure any dynamic content is loaded.
    rpSys_url = 'http://192.168.1.2/rpSys.html'
    response = session.get(rpSys_url, headers=headers1, allow_redirects=False)
    if response.is_redirect:
        redirect_url = response.headers['Location']
        # Follow the redirect manually
        print("Redirection url = ", redirect_url)
        response = session.get(redirect_url, headers=headers1)
        time.sleep(2) # Add a delay to ensure any dynamic content is loaded.
    headers2 = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/118.0.0.0 Safari/537.36',
        'Referer': 'http://192.168.1.2/rpSys.html',        
    }
    if response.status_code == 200:
        print('Login Successful!')
        # Form the status_url based on the structures of the HTML
        status_page_urls = [
            url for url in [
            'http://192.168.1.2/status.html',
            'http://192.168.1.2/navigation-status.html',
            'http://192.168.1.2/status/status_deviceinfo.html',
            'http://192.168.1.2/css/style.css',
            'http://192.168.1.2/js/general.js',
            'http://192.168.1.2/Images/Logo.gif',
            'http://192.168.1.2/Images/tb3.gif',
            'http://192.168.1.2/css/style.css',
            'http://192.168.1.2/css/style.css'] if url is not None        
        ]
        html_content = ""
        for url in status_page_urls:
            response = session.get(url, headers=headers2, allow_redirects=False)
            html_content += response.text
        #status_urls  = redirect_url + '/rpSys.html'
        #response = session.get(status_urls, headers=headers)
        #html_content = response.text
        soup = BeautifulSoup(html_content, 'html.parser')
        status_page_data = soup.prettify()
        return status_page_data 
    else:
        #Extract status page data (modify this based on the actual structure of the page)
        print('Login Failed!')
        return False

# Route for displaying router data
@app.route('/status_page')
def display_status_page():
    # Create a session
    session = requests.Session()
    your_username = 'admin'
    your_password = 'Shesh@72246'
    your_hashed_password = password_md5(your_password)
    #Perform login
    data = perform_login(session, your_username, your_hashed_password)

    return render_template('status_page.html', data=str(data))

# Route for favicon
@app.route('/favicon.ico')
def favicon():
    return send_from_directory(os.path.join(app.root_path, 'static'),
                               'favicon.ico', mimetype='image/vnd.microsoft.icon')

# Run the app if this script is executed
if __name__ == '__main__':
    app.run(host='192.168.1.100', port=80, debug=True)