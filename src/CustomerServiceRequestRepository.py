from CustomerServiceRequest import CustomerServiceRequest

class CustomerServiceRequestRepository():
    def get_customers_with_service_request_status_changes():
        
        while True:
            customer_service_request_ = CustomerServiceRequest()

            sql = """\
                select 
                    incident.incidentid,
                    incident.ticketnumber, 
                    incident.title, 
                    incident.contactidname, 
                    incident.emailaddress,
                    incident.statuscode
                from incident
                where (incident.new_statuscode_change_notified_cust_on is null 
                    or incident.new_statuscode_change_notified_cust_on < new_statuscode_lastupdated
            """
            yield customer