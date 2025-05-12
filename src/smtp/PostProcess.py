from pathlib import Path
from sys import path
path.append(str(Path(__file__).parent.parent)+'/') # Need to add path for where the source classes are

from csv import writer # Use Csv writers to log the result of both, successes and failures of some critical activity
from smtp.PostProcessInitContext import PostProcessInitContext
from smtp.Incident import Incident

"""
This class encapsulates the logic of how and where to store logs of successes and failures of some critical activity.
"""
class PostProcess():
    def __init__(self, init_context: PostProcessInitContext):

        assert isinstance(init_context,PostProcessInitContext) # Validate that context is of the expected class, PostProcessInitContext

        # Log file for successful sends must not be the same as log file for failed sends
        assert init_context.success_log_filename != init_context.failed_log_filename

        self.success_log_filename = init_context.success_log_filename
        self.failed_log_filename = init_context.failed_log_filename

        # Open files for writing only
        self.success_file = open(self.success_log_filename, 'w', newline='') # Newline='' means relegate line endings to the csv writer class
        self.failed_file = open(self.failed_log_filename, 'w', newline='') # Newline='' means relegate line endings to the csv writer class

        # First line of csv files is the header
        field_names = ['email_addr', 'contact_name', 'title','status','incidentid','email_result']

        # Even if no data is written, the header for successes will still have the header row
        self.csv_success_writer = writer(self.success_file)
        self.csv_success_writer.writerow(field_names) # Header row written

        # Even if no data is written, the header for failures will still have the header row
        self.csv_failed_writer = writer(self.failed_file)
        self.csv_failed_writer.writerow(field_names) # Header row written

    # May need to close files when this class goes out of scope
    def __del__(self):
        if self.success_file and not self.success_file.closed:
            self.success_file.close() # Ensure 'success' output file has all the buffered data, by closing the file if not yet closed

        if self.failed_file and not self.failed_file.closed:
            self.failed_file.close() # Ensure 'failed' output file has all the buffered data, by closing the if noet yet closed

    # Log incident as a success after successfully emailing to contact on the the service incident
    def mark_as_sent(self, incident: Incident):
        if not isinstance(incident, Incident):
            raise TypeError("Parameter incident needs to be of type Incident")

        if not self.success_log_filename:
            raise Exception("Successful log filename not initialized")

        # Write to a csv file, named differently than the file used for logging failures
        self.csv_success_writer.writerow((
            incident.email_addr,
            incident.contact_name,
            incident.title,
            incident.status,
            incident.incidentid,
            'success'
            ))
        
    # Log incident as a failure after failing to email to contact on the service incident
    def mark_as_failed_to_send(self, incident: Incident, e):
        if not isinstance(incident, Incident):
            raise TypeError("Parameter incident needs to be of type Incident")

        if not self.failed_log_filename:
            raise Exception("Failed log filename not initialized.")
        
        # Write to a csv file, named differently than the file used for logging successes
        self.csv_failed_writer.writerow((
            incident.email_addr,
            incident.contact_name,
            incident.title,
            incident.status,
            incident.incidentid,
            e # Include error message raised when failure to send email occurrred
            ))