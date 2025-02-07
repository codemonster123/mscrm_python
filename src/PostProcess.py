import csv

class PostProcess():
    def __init__(self, init_context):
        assert init_context
        # Log file for successful sends must not be the same as log file for failed sends
        assert init_context.success_log_filename != init_context.failed_log_filename

        self.success_log_filename = init_context.success_log_filename
        self.failed_log_filename = init_context.failed_log_filename

        self.success_file = open(self.success_log_filename, 'w', newline='')
        self.failed_file = open(self.failed_log_filename, 'w', newline='')

        field_names = ['email_addr', 'contact_name', 'title','status','incidentid','email_result']
        self.csv_success_writer = csv.writer(self.success_file)
        self.csv_success_writer.writerow(field_names)

        self.csv_failed_writer = csv.writer(self.failed_file)
        self.csv_failed_writer.writerow(field_names)

    def __del__(self):
        if self.success_file and not self.success_file.closed():
            self.success_file.close()

        if self.failed_file and not self.failed_file.closed():
            self.failed_file.close()


    def mark_as_sent(self, incident):
        if self.success_log_filename == None:
            raise Exception("Successful log filename not initialized")

        self.csv_success_writer.writerow((
            incident.email_addr,
            incident.contact_name,
            incident.title,
            incident.status,
            incident.incidentid,
            'sucess'
            ))
        

    def mark_as_failed_to_send(self, incident, e):
        if self.failed_log_filename == None:
            raise Exception("Failed log filename not initialized.")
        
        self.csv_success_writer.writerow((
            incident.email_addr,
            incident.contact_name,
            incident.title,
            incident.status,
            incident.incidentid,
            e
            ))