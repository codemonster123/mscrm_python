from sys import path
from pathlib import Path
path.append(str(Path(__file__).parent.parent)+'/src/')

from smtplib import SMTP
from smtp.SmtpServerInitContext import SmtpServerInitContext
from smtp.SmtpServer import SmtpServer
from pytest import raises
from unittest.mock import patch, MagicMock

def test_send_failure():
    # In case initialization for SmtpServer is faulty, make sure send method fails with expected exception
    with patch.object(SmtpServer, '__init__', lambda self, ctx: None):
        smtp_context = SmtpServerInitContext(80,'test_server','me@email.com', 'some_user_id', 'some_password')
        smtp_server = SmtpServer(smtp_context)
        smtp_server.__setattr__('smtp_server',None) # In the unusual case of a bad code revision
                                                    # that leaves critical internal attribute uninitialized
        # Bad initialization of internal smtp_server should result in an exception when send method is called
        with raises(Exception) as ex_info:
            smtp_server.send(to_name='someone',to_addr='someone@email.com', subject='some_subject', body='some_body')
        assert 'Smtp server is not initialized' in ex_info.value.args[0]

def test_send_success():
    smtp_context = SmtpServerInitContext(80,'test_server','me@email.com', 'some_user_id', 'some_password')
    with patch.multiple(SMTP, starttls=MagicMock(side_effect=lambda :None),
                        login=MagicMock(side_effect=lambda user, password: None),
                        send_message=MagicMock(side_effect=lambda msg: None)) as mock_smtp:
        smtp_server = SmtpServer(smtp_context)
        smtp_server.send(to_name='someone',to_addr='someone@email.com', subject='some_subject', body='some_body')