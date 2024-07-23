import smtplib
from email.mime.text import MIMEText

smtp_server = "smtp.office365.com"
smtp_port = 587
smtp_user = 'info-apdcp@artci.ci'
smtp_password = 'jeFs3oq-jycjZr%1sYwfu'

msg = MIMEText("Ceci est un test d'envoi d'email.")
msg['Subject'] = 'Test Email'
msg['From'] = smtp_user
msg['To'] = 'fouriersaint@gmail.com'

try:
    server = smtplib.SMTP(smtp_server, smtp_port)
    server.starttls()
    server.login(smtp_user, smtp_password)
    server.sendmail(smtp_user, ['fouriersaint@gmail.com'], msg.as_string())
    print("E-mail envoyé avec succès")
    server.quit()
except smtplib.SMTPDataError as e:
    print(f"Échec de l'envoi de l'e-mail : {e.smtp_error.decode()}")
except Exception as e:
    print(f"Une erreur s'est produite : {e}")
