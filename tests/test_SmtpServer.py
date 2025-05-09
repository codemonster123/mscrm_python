from sys import path
from pathlib import Path
path.append(str(Path(__file__).parent.parent)+'/src/')

from smtp.SmtpServerInitContext import SmtpServerInitContext
from smtp.SmtpServer import SmtpServer
import pytest
from unittest.mock import patch

def test_send_failure():
    # In case initialization for SmtpServer is faulty, make sure send method fails with expected exception
    with patch.object(SmtpServer, '__init__', lambda self, ctx: None):
        smtp_context = SmtpServerInitContext(80,'test_server','me@email.com', 'some_user_id', 'some_password')
        smtp_server = SmtpServer(smtp_context)
        smtp_server.__setattr__('smtp_server',None) # In the unusual case of a bad code revision
                                                    # that leaves critical internal attribute uninitialized
        # Bad initialization of internal smtp_server should result in an exception when send method is called
        with pytest.raises(Exception) as ex_info:
            smtp_server.send(to_name='someone',to_addr='someone@email.com', subject='some_subject', body='some_body')
        assert 'Smtp server is not initialized' in ex_info.value.args[0]

@patch('smtplib.SMTP')  # Assume initialization of internal smtp class went well, just want to make sure 
                        # internal send_message is called
def test_send_success(mock_smtp):
    smtp_context = SmtpServerInitContext(80,'test_server','me@email.com', 'some_user_id', 'some_password')
    smtp_server = SmtpServer(smtp_context)
    smtp_server.send(to_name='someone',to_addr='someone@email.com', subject='some_subject', body='some_body')
    mock_smtp.return_value.send_message.assert_called() # Able to reach end of code, calling send_message.