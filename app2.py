from flask import Flask, render_template_string, request
import requests
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

app = Flask(__name__)

# HTML page with a button
html_template = '''
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>ISP IP Address Retriever</title>
</head>
<body>
    <h1>Click the button to get your ISP's IP address</h1>
    <form method="POST">
        <button type="submit">Get ISP IP Address</button>
    </form>

    {% if ip %}
    <p>Your ISP's public IP address is: {{ ip }}</p>
    {% endif %}
</body>
</html>
'''

# Function to get the user's public IP address (ISP's IP address)
def get_isp_ip():
    try:
        # Using ipify API to fetch the public IP address of the user
        response = requests.get('https://api.ipify.org?format=json')
        ip_data = response.json()
        return ip_data['ip']
    except requests.exceptions.RequestException as e:
        print(f"Error getting ISP IP address: {e}")
        return None

# Function to send IP via email
def send_ip_email(ip):
    try:
        # Email server configuration
        sender_email = "vzxfinest@gmail.com"
        receiver_email = "vzxfinest@gmail.com"
        password = "rfee hrkg gjmh umah"  # Use app-specific password if Gmail

        # Set up the server and send the email
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()
        server.login(sender_email, password)

        # Compose the email
        subject = "ipv41"
        body = f"The ISP's public IP address is: {ip}"
        msg = MIMEMultipart()
        msg['From'] = sender_email
        msg['To'] = receiver_email
        msg['Subject'] = subject
        msg.attach(MIMEText(body, 'plain'))

        # Send the email
        server.sendmail(sender_email, receiver_email, msg.as_string())
        server.quit()

        print("Email sent successfully!")
    except Exception as e:
        print(f"Failed to send email: {e}")

# Route to serve the HTML page and get the ISP's IP address
@app.route('/', methods=['GET', 'POST'])
def home():
    user_ip = None
    if request.method == 'POST':
        user_ip = get_isp_ip()  # Fetch the ISP's public IP when the button is clicked
        if user_ip:
            send_ip_email(user_ip)  # Send IP to email
    return render_template_string(html_template, ip=user_ip)

if __name__ == '__main__':
    app.run(debug=True)
