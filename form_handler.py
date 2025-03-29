from flask import Flask, request, jsonify # type: ignore
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

# Initialize Flask app
app = Flask(__name__)

# Email configuration
SMTP_SERVER = 'smtp.gmail.com'
SMTP_PORT = 587
EMAIL_ADDRESS = 'llacy366@gmail.com'
EMAIL_PASSWORD = 'fitda5-bonQup-cykzux'

@app.route('./send-message', methods=['POST'])
def send_message():
    # Parse JSON data from the request
    data = request.json

    # Get the user's name, email, and message content
    name = data.get('name')
    sender_email = data.get('email')
    message = data.get('message')

    # Validate input fields
    if not name or not sender_email or not message:
        return jsonify({'error': 'All fields are required'}), 400 # Return error if a field is missing
    
    try:
        # Create the email message
        msg = MIMEMultipart()
        msg['From'] = EMAIL_ADDRESS
        msg['To'] = EMAIL_ADDRESS
        msg['Subject'] = f'New Message from {name}' 

        # Construct the body of the email
        body = f'Name: {name}\nEmail: {sender_email}\n\nMessage:\n{message}'
        msg.attach(MIMEText(body, 'plain'))

        # Connect to the SMTP server and send email
        server = smtplib.SMTP(SMTP_SERVER, SMTP_PORT) # Connect to SMTP server
        server.starttls() # Secure the connection
        server.login(EMAIL_ADDRESS, EMAIL_PASSWORD) # Log in to my email
        server.sendmail(EMAIL_ADDRESS, EMAIL_ADDRESS, msg.as_string()) # Send email to myself
        server.quit() # Close the connection

        return jsonify({'success': 'Message sent successfully'}) # Return success response

    except Exception as e:
        return jsonify({'error': str(e)}), 500 # Return error response if email fails

# Run the Flask app
if __name__ == '__main__':
    app.run(debug=True) # Enable debug mode for development