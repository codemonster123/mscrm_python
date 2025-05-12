"""
This is a convenience class for initialzing the IncidentRepository class.
Avoid using setters for this class, to keep instance immutable, to reduce
chance of bugs from inadvertent mutation.
"""
class RepositoryInitContext():
    def __init__(self, server: str, database: str, username: str, password: str):
        if not server:
            raise ValueError("Server is missing")
        self._server = server # SQL Server instance name

        if not database:
            raise ValueError("Database is missing")
        self._database = database # Database where CRM data resides
        
        if not username:
            raise ValueError("Username is missing")
        self._username = username
        
        if not password:
            raise ValueError("Password is missing")
        self._password = password # 
    
    @property
    def server(self):
        return self._server
    
    @property
    def database(self):
        return self._database
    
    @property
    def username(self):
        return self._username
    
    @property
    def password(self):
        return self._password
    