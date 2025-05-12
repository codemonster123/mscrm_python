from sys import path
from pathlib import Path; 
path.append(str(Path(__file__).parent.parent)+'/src/')

from smtp.IncidentRepository import IncidentRepository
from smtp.Incident import Incident
from smtp.RepositoryInitContext import RepositoryInitContext
from unittest.mock import patch, MagicMock

def test_properties_returned():
    # Parameters passed in RepositoryInitContext should appear as respective properties in IncidentRepository
    repoCtx = RepositoryInitContext(server='server', database='database', username='username', password='password')
    repo = IncidentRepository(repoCtx)
    assert repo.server == 'server'
    assert repo.database == 'database'
    assert repo.username == 'username'
    assert repo.password == 'password'

@patch('smtp.IncidentRepository.connect')
def test_get_incidents_with_status_changes(mock_connect):
    repoCtx = RepositoryInitContext(server='server', database='database', username='username', password='password')

    # Fabricate returned row from fetchall
    incident = {'incidentid': 'incidentid', 'emailaddress': 'email_addr', 'contactidname': 'contact_name', 'title': 'title', 'new_prior_statuscode': 'prior_status', 'statuscode': 'status', 'ticketnumber': 'ticketnumber'}

    mock_connect().cursor().fetchall.return_value = [incident]
    repo = IncidentRepository(repoCtx)

   # Make sure the field mapping from what was queried to what is initialized with the Incident object is correct
    fetched_incident = next(repo.get_incidents_with_status_changes())
    assert fetched_incident
    assert fetched_incident.incidentid == incident['incidentid']
    assert fetched_incident.email_addr == incident['emailaddress']
    assert fetched_incident.contact_name == incident['contactidname']
    assert fetched_incident.title == incident['title']
    assert fetched_incident.prior_status == incident['new_prior_statuscode']
    assert fetched_incident.status == incident['statuscode']
    assert fetched_incident.ticketnumber == incident['ticketnumber']