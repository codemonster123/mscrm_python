import smtplib
from email.message import EmailMessage
from email.utils import formataddr

class SmtpServer():
    def __init__(self, context):
        self.from_email_addr = context.from_email_addr

        self.smtp_server = smtplib.SMTP(port=context.port, local_hostname=context.hostname)
        self.smtp_server.starttls()
        self.smtp_server.login(user=context.user_id, password=context.password)

    def __del__(self):
        self.smtp_server.quit()

    def send(self, to_name, to_addr, subject, body):
        if self.smtp_server == None:
            raise Exception("Smtp server is not initialized")
        
        msg = EmailMessage()
        msg.set_content(body)
        msg['Subject'] = subject
        msg['From'] = self.from_email_addr
        msg['To'] = formataddr((to_name, to_addr))

        self.smtp_server.send_message(msg)


