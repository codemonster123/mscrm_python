class RepositoryInitContext():
    def __init__(self, server, database, username, password):
        self.server = server
        self.database = database
        self.username = username
        self.password = password
    
    @property
    def server(self):
        return self.server
    
    @property
    def database(self):
        return self.database
    
    @property
    def username(self):
        return self.username
    
    @property
    def password(self):
        return self.password
    