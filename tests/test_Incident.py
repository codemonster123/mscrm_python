from sys import path
from pathlib import Path; 
path.append(str(Path(__file__).parent.parent)+'/src/')
from smtp.Incident import Incident
import pytest

def test_properties_returned():
    incident = Incident(incidentid='incident_1', 
                        email_addr='me@example.com', 
                        contact_name='contact_name', 
                        title='title', 
                        prior_status='prior_status', 
                        status='status', 
                        ticketnumber='ticket#')
    
    assert incident.incidentid == 'incident_1'
    assert incident.email_addr=='me@example.com'
    assert incident.contact_name=='contact_name'
    assert incident.title=='title'
    assert incident.prior_status=='prior_status'
    assert incident.status=='status'
    assert incident.ticketnumber=='ticket#'
