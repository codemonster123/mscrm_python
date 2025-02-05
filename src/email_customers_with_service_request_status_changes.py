import sys
import os
import PostProcessInitContext
from PostProcess import PostProcess
import SmtpServerInitContext
import SmtpServer
import CustomerServiceRequestRepository

def get_postprocess_initialization_context():
    context = PostProcessInitContext(
        success_log_filename=os.environ['POSTPROCESS_FAILED_LOG_FILENAME'],
        failed_log_filename=os.environ['POSTPROCESS_FAILED_LOG_FILENAME']
    )
    return context


def get_smtp_initialization_context():
    context = SmtpServerInitContext(
        port=os.environ['SMTP_PORT'], 
        hostname=os.environ['SMTP_HOSTNAME'], 
        from_email_addr=os.environ['SMTP_FROM_EMAIL_ADDR'], 
        user_id=os.environ['SMTP_USER_ID'], 
        password=os.environ['SMTP_PASSWORD'], 
    )
    return context


def get_smtp_server(init_context):
    return SmtpServer(init_context)


def get_customer_service_requests_to_email():
    cust_repo = CustomerServiceRequestRepository()
    return cust_repo.get_customers_with_service_request_status_change()


def get_content_body_from_customer(customer_service_request):
    body = f"""\
    Dear {customer_service_request.first_name + ' ' +customer_service_request.last_name},

    The status of your submitted request, '{customer_service_request.service_request_descr}', 
    has changed to {customer_service_request.service_request_status}.
    """
    return body


def process_after_sent_successfully(customer_service_request):
    customer_service_request.mark_as_sent()


def process_after_failure_to_send(customer_service_request, e):
    customer_service_request.mark_as_failed_to_send()


def main():
    try:
        postprocess_init_context = get_postprocess_initialization_context()
        postprocess = PostProcess(postprocess_init_context)

        smtp_init_context = get_smtp_initialization_context()
        smtp_server = get_smtp_server(smtp_init_context)

        for customer_service_request in get_customer_service_requests_to_email():
            try:
                smtp_server.send(  
                    to_name = customer_service_request.first_name + ' ' + customer_service_request.last_name,
                    to_addr = customer_service_request.email_addr,
                    subject = f"Status of request '{customer_service_request.service_request_descr}' has changed to '{customer_service_request.service_request_status}'",
                    body = get_content_body_from_customer(customer_service_request)
                )

                postprocess.mark_as_sent(customer_service_request)

            except Exception as e:
                postprocess.mark_as_failed_to_send(customer_service_request, e)
                
    except Exception as e:
        # Hard error related to environment, configuration, or securuity
        print(e.message)
        sys.exit(-1)

    # Did not encounter errors
    sys.exit(0)


if __name__ == '__main__':
    main()