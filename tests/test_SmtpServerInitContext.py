from sys import path
from pathlib import Path; 
path.append(str(Path(__file__).parent.parent)+'/src/')

from smtp.SmtpServerInitContext import SmtpServerInitContext
import pytest

def test_port_invalid():
    # Make sure port is not missing
    with pytest.raises(ValueError) as ex_info:
        SmtpServerInitContext('','some_hostname', 'some@example.com', 'some_user_id', 'some_password')
    assert 'Missing' in ex_info.value.args[0]

    # Make sure port is numeric
    with pytest.raises(TypeError) as ex_info:
        SmtpServerInitContext('abc','some_hostname', 'some@example.com', 'some_user_id', 'some_password')
    assert 'Port must be an int' in ex_info.value.args[0]

    # Make sure port is greater than zero
    with pytest.raises(ValueError) as ex_info:
        SmtpServerInitContext(-1,'some_hostname', 'some@example.com', 'some_user_id', 'some_password')
    assert 'Port must be greater than zero' in ex_info.value.args[0]

def test_from_email_addr_invalid():
    # Make sure 'from email address' is not missing
    with pytest.raises(ValueError) as ex_info:
        SmtpServerInitContext(80, 'some_hostname', '', 'some_user_id', 'some_password')
    assert 'Missing' in ex_info.value.args[0]

    # Make sure 'from email address' has '@'
    with pytest.raises(ValueError) as ex_info:
        SmtpServerInitContext(80, 'some_hostname', 'some_from_email_addr', 'some_user_id', 'some_password')
    assert "Expected 'From Email Addr' to contain an '@'" in ex_info.value.args[0]

def test_hostname_invalid():
    # Make sure 'hostname' is not missing
    with pytest.raises(ValueError) as ex_info:
        SmtpServerInitContext(80, '', 'some@example.com', 'some_user_id', 'some_password')
    assert 'Missing' in ex_info.value.args[0]

    # Make sure 'hostname' does not have an '@'
    with pytest.raises(ValueError) as ex_info:
        SmtpServerInitContext(80, 'some@host', 'some@email.com', 'some_user_id', 'some_password')
    assert "Unexpected '@' character" in ex_info.value.args[0]

def test_user_id_invalid():
    # Make sure 'user_id' is not missing
    with pytest.raises(ValueError) as ex_info:
        SmtpServerInitContext(80, 'some_host', 'some@email.com', '', 'some_password')
    assert 'Missing' in ex_info.value.args[0]

def test_password_invalid():
    # Make sure 'password' is not missing
    with pytest.raises(ValueError) as ex_info:
        SmtpServerInitContext(80, 'some_host', 'some@example.com', 'some_user_id', '')
    assert 'Missing' in ex_info.value.args[0]

def test_properties_returned():
    # Make sure all properties return the values expected, the values passed for class instantiation
    context = SmtpServerInitContext(80, 'some_hostname', 'some@email.com', 'some_user_id', 'some_password')
    assert context.port == 80
    assert context.hostname == 'some_hostname'
    assert context.from_email_addr == 'some@email.com'
    assert context.user_id == 'some_user_id'
    assert context.password == 'some_password'
