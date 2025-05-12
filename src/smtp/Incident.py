"""
This class is used to store service incidents from the database
"""
class Incident():
    def __init__(self, incidentid: str, email_addr: str, contact_name: str, title: str, prior_status: str, status, ticketnumber: str):
        self.incidentid = incidentid    # This is the system-generated id in the CRM system, not friendly/useful enough 
                                        # to show to the contact on the service incident
        self.email_addr = email_addr # Assume this is the email address of the main contact for the service incident
        self.contact_name = contact_name # Full name of the primary contact the on the service incident
        self.title = title # Assume all incidents have a title, however generic and/or unspecific
        self.prior_status = prior_status    # Augment CRM incident entity to record the prior status, and have it shown here
                                            # in emails to the contact, as contact would want to know the prior status
        self.status = status # This represents the current status of the service incident
        self.ticketnumber = ticketnumber # Incident Id is probably not as helpful to the email to the contact as ticket number
    