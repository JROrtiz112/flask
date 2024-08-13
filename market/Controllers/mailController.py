from flask_mail import Mail, Message
import codecs
import os

class Email:

    #flask-mail.Message(subject, recipients, body, html, sender, cc, bcc, reply-to, date, charset, extra_headers, mail_options, rcpt_options)
    mail = None
    title = ''
    mailFrom = ''
    sendTo = ''

    def __init__(self, app):
        app.config['MAIL_SERVER']='smtp.mailtrap.io'
        app.config['MAIL_PORT'] = 2525
        app.config['MAIL_USERNAME'] = 'f048f27e57a618'
        app.config['MAIL_PASSWORD'] = '04f394c61a3e77'
        app.config['MAIL_USE_TLS'] = True
        app.config['MAIL_USE_SSL'] = False

        self.mail = Mail(app)
        self.title = 'Purchase receipt'
        self.mailFrom = 'yourId@gmail.com'
        self.sendTo = '@gmail.com'
        
    
    def sendMail(self, mail):
        msg = Message(self.title, sender = self.mailFrom, recipients = [mail.lower() + self.sendTo])

        html = codecs.open('/Users/robertoortizsalazar/Documents/flask/market/Templates/base.html', 'r', 'UTF-8')
        
        msg.body = "The following is to inform that your puchase was successfully made"
        msg.html = f"<div><h2>{self.title}</h2><br>The following is to inform that your puchase was successfully made</div>"
        self.mail.send(msg)