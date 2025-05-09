import pyodbc
from pathlib import Path
from sys import path
path.append(str(Path(__file__).parent.parent)+'/')

from smtp.Incident import Incident
from smtp.RepositoryInitContext import RepositoryInitContext

class IncidentRepository():
    def __init__(self, context: RepositoryInitContext):
        self.server = context.server
        self.database = context.database
        self.username = context.username
        self.password = context.password

    def get_incidents_with_status_changes(self):
        connectionString = f'DRIVER={{ODBC Driver 18 for SQL Server}};SERVER={self.server};DATABASE={self.database};UID={self.username};PWD={self.password}'
        conn = pyodbc.connect(connectionString)
        
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
