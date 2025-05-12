from smtplib import SMTP # SMTP functionality in the standard Python library is adequate for our needs
from email.message import EmailMessage # Use a convenience class for packaging individual emails for sending
from email.utils import formataddr

from smtp.SmtpServerInitContext import SmtpServerInitContext # Use a convenience function to handle encoding of email addresses

"""
This class encapsulates SMTP functionality and at this time, supports only the 'send' functionality.
The SMTP server is expected to support TLS (Transport Layer Security).
"""
class SmtpServer():
    """
    As soon as this class is instantiated, it should be ready to send email, given mainly
    destination email address, subject line, and body.
    """
    def __init__(self, context: SmtpServerInitContext):
        assert isinstance(context, SmtpServerInitContext)
        self.from_email_addr = context.from_email_addr

        self.smtp_server = SMTP(port=context.port, local_hostname=context.hostname)
        self.smtp_server.starttls() # Insist on using TLS security when for all SMTP communication, as best practice.
        self.smtp_server.login(user=context.user_id, password=context.password)

    def __del__(self):
        self.smtp_server.quit() # Terminate SMTP server when the instance of this class goes out of scope

    def send(self, to_name: str, to_addr: str, subject: str, body: str):
        if self.smtp_server == None: # Make sure SMTP connection is established before sending emails
            raise Exception("Smtp server is not initialized")
        
        # Prepare message for sending
        msg = EmailMessage()
        msg.set_content(body)
        msg['Subject'] = subject
        msg['From'] = self.from_email_addr
        msg['To'] = formataddr((to_name, to_addr)) # Pass friendly name, followed by email address

        # Send immediately to SMTP server.
        self.smtp_server.send_message(msg)


