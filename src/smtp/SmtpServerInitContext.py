"""
This class is used to store the parameters, including a default 'from' email address, needed to 
login to a specific SMTP server. Instances of this class should be passed to the SmtpServer class.
"""
class SmtpServerInitContext():
    """
    Allow specifying parameters only during initialization of class. Keeping the properties immutable
    reduces the possibility of bugs from inadvertent changes to state.
    """
    def __init__(self, port: int, hostname: str, from_email_addr: str, user_id: str, password: str):
        if not port:
            raise ValueError("Missing port value of SMTP server")
        if not isinstance(port, int):
            raise TypeError("Port must be an int")
        if port <= 0:
            raise ValueError("Port must be greater than zero")
        self._port = port # Typically, the SMTP port is 25 (not recommended, not TLS; 587 or 2525 for TLS.

        if not hostname:
            raise ValueError("Missing hostname of SMTP server")
        if '@' in hostname:
            raise ValueError("Unexpected '@' character found in hostname")
        self._hostname = hostname # Name or IP address of SMTP server.

        if not from_email_addr:
            raise ValueError("Missing 'From Email Addr' needed to initialize class SmtpServerInitContext")
        if '@' not in from_email_addr:
            raise ValueError("Expected 'From Email Addr' to contain an '@' character to be a valid email address")
        self._from_email_addr = from_email_addr # This email address is not used to login to the SMTP server, 
                                                # but used as the default 'from' email address when sending out email.
        
        if not user_id:
            raise ValueError("Missing 'User Id' needed to initialize class SmtpServerInitContext")
        self._user_id = user_id # User Id needed to log into the SMTP server.

        if not password:
            raise ValueError("Missing 'Password' needed to initialize class SmtpServerInitContext")
        self._password = password # Password needed to lg into the SMTP server.
    
    @property
    def port(self):
        return self._port # Keep property read-only (no need for setter)
    
    @property
    def hostname(self):
        return self._hostname  # Keep property read-only (no need for setter)
    
    @property
    def from_email_addr(self):
        return self._from_email_addr # Keep property read-only (no need for setter)
    
    @property
    def user_id(self):
        return self._user_id # Keep property read-only (no need for setter)
    
    @property
    def password(self):
        return self._password # Keep property read-only (no need for setter)