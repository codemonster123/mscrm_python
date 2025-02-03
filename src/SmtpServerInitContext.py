class SmtpServerInitContext():
    def __init__(self, port, hostname, from_email_addr, user_id, password):
        self.port = port
        self.hostname = hostname
        self.from_email_addr = from_email_addr
        self.user_id = user_id
        self.password = password
    
    @property
    def port(self):
        return self.port
    
    @property
    def hostname(self):
        return self.hostname
    
    @property
    def from_email_addr(self):
        return self.from_email_addr
    
    @property
    def user_id(self):
        return self.user_id
    
    @property
    def password(self):
        return self.password