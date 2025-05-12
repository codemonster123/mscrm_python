from pyodbc import connect # Let's access the CRM data through an ODBC connection, assuming the data is stored in an MS SQL Server database
from pathlib import Path
from sys import path
path.append(str(Path(__file__).parent.parent)+'/') # Need to add path for where the source classes are

from smtp.Incident import Incident # This class represents the service incident record stored in Dynamics CRM
from smtp.RepositoryInitContext import RepositoryInitContext

"""
Encapsulate the database connection for service incidents behind a repository class.
Don't hardcode SQL inside business domain calls. Instead, express SQL in this repository class
for looser coupling.
"""
class IncidentRepository():
    def __init__(self, context: RepositoryInitContext):
        self.server = context.server # Name of SQL Server instance
        self.database = context.database # Name of the CRM database
        self.username = context.username
        self.password = context.password # Assume we are using standard security with SQL Server

    """
    The incident.new_statuscode_change_notified_cust_on field represents the date the contact on the service ticket
    was last notified of an incident status change. The new_statuscode_lastupdated date represents the date the current
    status was set. We want to query only service incidents where the customer has not been notified of the current status, yet.
    Assume, because of the restrictive where clause on new_statuscode_change_notified_cust_on field,
    that no more 10,000 rows are returned, and can be fetched with a fetch all call.
    """
    def get_incidents_with_status_changes(self):
        connectionString = f'DRIVER={{ODBC Driver 18 for SQL Server}};SERVER={self.server};DATABASE={self.database};UID={self.username};PWD={self.password}'
        conn = connect(connectionString) #Log into the SQL Server
        
        sql = """\
            select 
                incident.incidentid,
                incident.ticketnumber, 
                incident.title, 
                incident.contactidname, 
                incident.emailaddress,
                incident.statuscode,
                incident.new_prior_statuscode
            from incident
            where incident.new_prior_statuscode is not null
                and incident.new_statuscode_change_notified_cust_on < new_statuscode_lastupdated;
        """
        cursor = conn.cursor()
        cursor.execute(sql)

        # Wrap each returned row, representing a service incident, in an Incident instance
        # and return them all in a generator
        for row in cursor.fetchall():
            yield Incident(
                incidentid=row['incidentid'],
                email_addr=row['emailaddress'],
                contact_name=row['contactidname'],
                title=row['title'],
                prior_status=row['new_prior_statuscode'],
                status=row['statuscode'],
                ticketnumber=row['ticketnumber']
            )
