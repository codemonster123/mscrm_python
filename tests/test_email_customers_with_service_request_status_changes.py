from pathlib import Path
from sys import path
path.append(str(Path(__file__).parent.parent)+'/src/')

from os import environ
from smtp.email_customers_with_service_request_status_changes import (
    get_postprocess_initialization_context,
    get_smtp_initialization_context,
    get_odbc_initialization_context,
    get_incidents_to_email,
    get_content_body_from_incident,
    main
)
from unittest.mock import (patch,MagicMock)
from smtp.Incident import Incident
from smtp.PostProcess import PostProcess
from smtplib import SMTP

def test_get_postprocess_initialization_context():
    environ['POSTPROCESS_SUCCESS_LOG_FILENAME'] = 'successfile'
    environ['POSTPROCESS_FAILED_LOG_FILENAME'] = 'failedfile'
    ctx = get_postprocess_initialization_context()
    assert ctx.success_log_filename == 'successfile'
    assert ctx.failed_log_filename == 'failedfile'

def test_get_smtp_initialization_context():
    environ['SMTP_PORT'] = '25'
    environ['SMTP_HOSTNAME'] = 'smtp_hostname'
    environ['SMTP_FROM_EMAIL_ADDR'] = 'some@email.com'
    environ['SMTP_USER_ID'] = 'some_user'
    environ['SMTP_PASSWORD'] = 'some_password'
    ctx = get_smtp_initialization_context()
    assert ctx.port == 25
    assert ctx.hostname == 'smtp_hostname'
    assert ctx.from_email_addr == 'some@email.com'
    assert ctx.user_id == 'some_user'
    assert ctx.password == 'some_password'

def test_odbc_initialization_context():
    environ['ODBC_SERVER'] = 'some_server'
    environ['ODBC_DATABASE'] = 'some_database'
    environ['ODBC_NAME'] = 'some_username'
    environ['ODBC_PASSWORD'] = 'some_password'
    ctx = get_odbc_initialization_context()
    assert ctx.server == 'some_server'
    assert ctx.database == 'some_database'
    assert ctx.username == 'some_username'
    assert ctx.password == 'some_password'

@patch('smtp.IncidentRepository.connect')
def test_get_incidents_to_email(mock_connect):
    environ['ODBC_SERVER'] = 'some_server'
    environ['ODBC_DATABASE'] = 'some_database'
    environ['ODBC_NAME'] = 'some_username'
    environ['ODBC_PASSWORD'] = 'some_password'
    mock_connect().cursor().fetchall.return_value = [
        {
            'incidentid': 'some_incidentid',
            'emailaddress': 'some@email.com',
            'contactidname': 'some_contact',
            'title': 'some_title',
            'new_prior_statuscode': 'some_prior_status',
            'statuscode': 'some_status',
            'ticketnumber': 'some_ticketnumber'
        }
    ]
    incident = next(get_incidents_to_email())
    assert incident
    assert incident.incidentid == 'some_incidentid'
    assert incident.email_addr == 'some@email.com'
    assert incident.contact_name == 'some_contact'
    assert incident.title == 'some_title'
    assert incident.prior_status == 'some_prior_status'
    assert incident.status == 'some_status'
    assert incident.ticketnumber == 'some_ticketnumber'

def test_get_content_body_from_incident():
    body = get_content_body_from_incident(
        Incident(
            incidentid='some_incidentid',
            email_addr='some@email.com',
            contact_name='some_contact',
            title='some_title',
            prior_status='some_prior_status',
            status='some_status',
            ticketnumber='some_ticketnumber'
        )
    )
    assert 'Dear some_contact' in body
    assert 'ticket# some_ticketnumber' in body
    assert 'some_title' in body
    assert 'changed to some_status' in body
    assert 'from some_prior_status' in body

@patch('smtp.IncidentRepository.connect')
def test_main(mock_connect):
    environ['POSTPROCESS_SUCCESS_LOG_FILENAME'] = 'successfile'
    environ['POSTPROCESS_FAILED_LOG_FILENAME'] = 'failedfile'
    environ['SMTP_PORT'] = '25'
    environ['SMTP_HOSTNAME'] = 'smtp_hostname'
    environ['SMTP_FROM_EMAIL_ADDR'] = 'some@email.com'
    environ['SMTP_USER_ID'] = 'some_user'
    environ['SMTP_PASSWORD'] = 'some_password'
    environ['ODBC_SERVER'] = 'some_server'
    environ['ODBC_DATABASE'] = 'some_database'
    environ['ODBC_NAME'] = 'some_username'
    environ['ODBC_PASSWORD'] = 'some_password'
    mock_connect().cursor().fetchall.return_value = [
        {
            'incidentid': 'some_incidentid',
            'emailaddress': 'some@email.com',
            'contactidname': 'some_contact',
            'title': 'some_title',
            'new_prior_statuscode': 'some_prior_status',
            'statuscode': 'some_status',
            'ticketnumber': 'some_ticketnumber'
        }
    ]
    with patch.multiple(SMTP,starttls=MagicMock(side_effect=lambda : None),
                        login=MagicMock(side_effect=lambda user, password: None),
                        send_message=MagicMock(side_effect=lambda msg: None)) as mock_smtp:
        main()

@patch('smtp.IncidentRepository.connect')
def test_main_fail_sending_email(mock_connect):
    environ['POSTPROCESS_SUCCESS_LOG_FILENAME'] = 'successfile'
    environ['POSTPROCESS_FAILED_LOG_FILENAME'] = 'failedfile'
    environ['SMTP_PORT'] = '25'
    environ['SMTP_HOSTNAME'] = 'smtp_hostname'
    environ['SMTP_FROM_EMAIL_ADDR'] = 'some@email.com'
    environ['SMTP_USER_ID'] = 'some_user'
    environ['SMTP_PASSWORD'] = 'some_password'
    environ['ODBC_SERVER'] = 'some_server'
    environ['ODBC_DATABASE'] = 'some_database'
    environ['ODBC_NAME'] = 'some_username'
    environ['ODBC_PASSWORD'] = 'some_password'
    mock_connect().cursor().fetchall.return_value = [
        {
            'incidentid': 'some_incidentid',
            'emailaddress': 'some@email.com',
            'contactidname': 'some_contact',
            'title': 'some_title',
            'new_prior_statuscode': 'some_prior_status',
            'statuscode': 'some_status',
            'ticketnumber': 'some_ticketnumber'
        }
    ]
    with patch.multiple(SMTP,starttls=MagicMock(side_effect=lambda : None),
                        login=MagicMock(side_effect=lambda user, password: None),
                        send_message=MagicMock(side_effect=Exception("Failed to send"))) as mock_smtp:
        main()

@patch('smtp.IncidentRepository.connect')
def test_main_fail_mark_failed_to_send(mock_connect):
    environ['POSTPROCESS_SUCCESS_LOG_FILENAME'] = 'successfile'
    environ['POSTPROCESS_FAILED_LOG_FILENAME'] = 'failedfile'
    environ['SMTP_PORT'] = '25'
    environ['SMTP_HOSTNAME'] = 'smtp_hostname'
    environ['SMTP_FROM_EMAIL_ADDR'] = 'some@email.com'
    environ['SMTP_USER_ID'] = 'some_user'
    environ['SMTP_PASSWORD'] = 'some_password'
    environ['ODBC_SERVER'] = 'some_server'
    environ['ODBC_DATABASE'] = 'some_database'
    environ['ODBC_NAME'] = 'some_username'
    environ['ODBC_PASSWORD'] = 'some_password'
    mock_connect().cursor().fetchall.return_value = [
        {
            'incidentid': 'some_incidentid',
            'emailaddress': 'some@email.com',
            'contactidname': 'some_contact',
            'title': 'some_title',
            'new_prior_statuscode': 'some_prior_status',
            'statuscode': 'some_status',
            'ticketnumber': 'some_ticketnumber'
        }
    ]
    with patch.object(PostProcess,'mark_as_failed_to_send', side_effect=Exception('test')):
        with patch.multiple(SMTP,starttls=MagicMock(side_effect=lambda : None),
                            login=MagicMock(side_effect=lambda user, password: None),
                            send_message=MagicMock(side_effect=Exception("Failed to send"))) as mock_smtp:
            main()