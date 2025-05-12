"""
This class is a convenience class used to initialize the the PostProcess class. 
It is a good place to add validation, instead of to the PostProcess class, which
should remain focused on the work of writing logs to some destination.
"""
class PostProcessInitContext():
    def __init__(self, success_log_filename: str, failed_log_filename: str):
        if not success_log_filename:
            raise ValueError("Success_log_filename is missing")
        self._success_log_filename = success_log_filename

        if not failed_log_filename:
            raise ValueError("Failed_log_filename is missing")
        self._failed_log_filename = failed_log_filename
    
    @property
    def success_log_filename(self): # Avoid having a setter so that instance can be immutable
        return self._success_log_filename
    
    @property
    def failed_log_filename(self): # Avoid having a setter so that instance can be immutable
        return self._failed_log_filename