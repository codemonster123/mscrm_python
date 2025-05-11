from pathlib import Path
from sys import path
path.append(str(Path(__file__).parent.parent)+'/')
import sys
import os
from smtp.PostProcessInitContext import PostProcessInitContext
from smtp.PostProcess import PostProcess
from smtp.SmtpServerInitContext import SmtpServerInitContext
from smtp.SmtpServer import SmtpServer
from smtp.RepositoryInitContext import RepositoryInitContext
from smtp.IncidentRepository import IncidentRepository

def get_postprocess_initialization_context():
    context = PostProcessInitContext(
        success_log_filename=os.environ['POSTPROCESS_SUCCESS_LOG_FILENAME'],
        failed_log_filename=os.environ['POSTPROCESS_FAILED_LOG_FILENAME']
    )
    return context


def get_smtp_initialization_context():
    context = SmtpServerInitContext(
        port=int(os.environ['SMTP_PORT']), 
        hostname=os.environ['SMTP_HOSTNAME'], 
        from_email_addr=os.environ['SMTP_FROM_EMAIL_ADDR'], 
        user_id=os.environ['SMTP_USER_ID'], 
        password=os.environ['SMTP_PASSWORD'], 
    )
    return context

def get_odbc_initialization_context():
    context = RepositoryInitContext(
        server=os.environ['ODBC_SERVER'],
        database=os.environ['ODBC_DATABASE'],
        username=os.environ['ODBC_NAME'],
        password=os.environ['ODBC_PASSWORD']
    )
    return context


def get_incidents_to_email():
    odbc_init_context = get_odbc_initialization_context()
    incident_repo = IncidentRepository(odbc_init_context)
    return incident_repo.get_incidents_with_status_changes()


def get_content_body_from_incident(incident):
    body = f"""\
    Dear {incident.contact_name},

    The status of your submitted request, ticket# {incident.ticketnumber} '{incident.title}', 
    has changed to {incident.status} (from {incident.prior_status}).
    """
    return body


def main():
    try:
        postprocess_init_context = get_postprocess_initialization_context()
        postprocess = PostProcess(postprocess_init_context)

        smtp_init_context = get_smtp_initialization_context()
        smtp_server = SmtpServer(smtp_init_context)

        for incident in get_incidents_to_email():
            try:
                smtp_server.send(  
                    to_name = incident.contact_name,
                    to_addr = incident.email_addr,
                    subject = f"Status of ticket #{incident.ticketnumber} '{incident.title}' has changed to '{incident.status}'",
                    body = get_content_body_from_incident(incident)
                )

                postprocess.mark_as_sent(incident)

            except Exception as e:
                postprocess.mark_as_failed_to_send(incident, e)
                
    except Exception as e:
        # Hard error related to environment, configuration, or security
        print(f"Encountered error: {e}")
        if __name__ == '__main__':
            sys.exit(-1)

    # Did not encounter errors
    if __name__ == '__main__':
        sys.exit(0)


if __name__ == '__main__':
    main()