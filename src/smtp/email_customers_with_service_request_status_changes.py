from pathlib import Path
from sys import path, exit
path.append(str(Path(__file__).parent.parent)+'/') # Need to include top level folder for the source of classes used in this script

from os import environ # Look up environment variables for operating parameters
from smtp.PostProcessInitContext import PostProcessInitContext
from smtp.PostProcess import PostProcess # Use to log successes and failures of emailing contacts on service incidents
from smtp.SmtpServerInitContext import SmtpServerInitContext
from smtp.SmtpServer import SmtpServer # Use to send emails
from smtp.RepositoryInitContext import RepositoryInitContext
from smtp.IncidentRepository import IncidentRepository # Use to retrieve service incidents whose status has recently changed

# Gets file logging parameters from environment variables, and passes them to the PostProcess class
def get_postprocess_initialization_context():
    context = PostProcessInitContext(
        success_log_filename=environ['POSTPROCESS_SUCCESS_LOG_FILENAME'],
        failed_log_filename=environ['POSTPROCESS_FAILED_LOG_FILENAME']
    )
    return context

# Gets SMTP parameters from environment variables, and passes them to the SmtpServer class
def get_smtp_initialization_context():
    context = SmtpServerInitContext(
        port=int(environ['SMTP_PORT']), 
        hostname=environ['SMTP_HOSTNAME'], 
        from_email_addr=environ['SMTP_FROM_EMAIL_ADDR'], 
        user_id=environ['SMTP_USER_ID'], 
        password=environ['SMTP_PASSWORD'], 
    )
    return context

# Gets ODBC parameters from environment variables, and passes them to the IncidentRepository class
def get_odbc_initialization_context():
    context = RepositoryInitContext(
        server=environ['ODBC_SERVER'],
        database=environ['ODBC_DATABASE'],
        username=environ['ODBC_NAME'],
        password=environ['ODBC_PASSWORD']
    )
    return context

# Enumerates service incidents, stored in a database, whose status has 'recently' changed
def get_incidents_to_email():
    odbc_init_context = get_odbc_initialization_context()
    incident_repo = IncidentRepository(odbc_init_context)
    return incident_repo.get_incidents_with_status_changes()

# The body content of each email relies on information contained in an Incident class.
def get_content_body_from_incident(incident):
    body = f"""\
    Dear {incident.contact_name},

    The status of your submitted request, ticket# {incident.ticketnumber} '{incident.title}', 
    has changed to {incident.status} (from {incident.prior_status}).
    """
    return body # Should confirm in a unit test that all place-holders have been populated with Incident data

"""
This is the main function for this script. This function:
1. Retrieves operating parameters from a handful of environment variables
2. Opens log files for logging the results of sending emails regarding status changes to service incidents
3. Connects to an SMTP server for sending emails
"""
def main():
    try:
        postprocess_init_context = get_postprocess_initialization_context() # Gets operating parameters from OS environmental variables
        postprocess = PostProcess(postprocess_init_context) # Encapsulates logging logic, of both, successful and failed emailing

        smtp_init_context = get_smtp_initialization_context() # Gets operating parameters from OS environmental variables
        smtp_server = SmtpServer(smtp_init_context) # Encapsulates SMTP logic

        # Iterate qualified service incidents from database and try to send individual emails to contact on incident
        for incident in get_incidents_to_email():
            try:
                smtp_server.send(  
                    to_name = incident.contact_name,
                    to_addr = incident.email_addr,
                    subject = f"Status of ticket #{incident.ticketnumber} '{incident.title}' has changed to '{incident.status}'",
                    body = get_content_body_from_incident(incident)
                )
                # If no exception is raised, then log the emailing of status for this incident as successful
                postprocess.mark_as_sent(incident)

            except Exception as e:
                # Detected failure in emailing, so need to log in separate file for future follow-up
                postprocess.mark_as_failed_to_send(incident, e)
                
    except Exception as e:
        # Hard error related to environment, configuration, or security
        print(f"Encountered error: {e}")
        if __name__ == '__main__':
            exit(-1)

    # Did not encounter errors
    if __name__ == '__main__':
        exit(0)


if __name__ == '__main__':
    main()