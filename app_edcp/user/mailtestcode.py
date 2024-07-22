import smtplib
from email.mime.text import MIMEText

msg = MIMEText('Test email body')
msg['Subject'] = 'Test email subject'
msg['From'] = 'pythondomotique@gmail.com'
msg['To'] = 'fouriersaint@gmail.com'

server = smtplib.SMTP('smtp.gmail.com', 587)
server.starttls()
# Utilisez le mot de passe d'application généré ici
server.login('pythondomotique@gmail.com', 'elng myjb mtas otbx')
server.sendmail('pythondomotique@gmail.com', ['fouriersaint@gmail.com'], msg.as_string())
server.quit()
