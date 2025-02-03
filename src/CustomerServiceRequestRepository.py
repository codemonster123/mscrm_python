from Customer import Customer

class CustomerRepository():
    def get_customers_with_service_request_status_changes():
        
        while True:
            customer = Customer()
            yield customer