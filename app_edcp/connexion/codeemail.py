import smtplib
from email.mime.text import MIMEText

smtp_server = 'smtp.office365.com'
smtp_port = 587
smtp_user = 'info-apdcp@artci.ci'
smtp_password = 'jeFs3oq-jycjZr%1sYwfu'

msg = MIMEText('This is a test email.')
msg['Subject'] = 'Test Email'
msg['From'] = smtp_user
msg['To'] = 'pythondomotique@gmail.com'

try:
    with smtplib.SMTP(smtp_server, smtp_port) as server:
        print("Connecting to SMTP server...")
        response = server.ehlo()
        print(f"EHLO response: {response}")

        server.starttls()
        response = server.ehlo()
        print(f"EHLO response after STARTTLS: {response}")

        server.login(smtp_user, smtp_password)
        print("Authenticated successfully.")

        response = server.send_message(msg)
        print(f"Send message response: {response}")

        print('Test email sent successfully')
except smtplib.SMTPException as smtp_error:
    print('SMTP error occurred:', smtp_error)
except Exception as e:
    print('An unexpected error occurred:', e)