class PostProcessInitContext():
    def __init__(self, success_log_filename, failed_log_filename):
        if not success_log_filename:
            raise ValueError("Success_log_filename is missing")
        self._success_log_filename = success_log_filename

        if not failed_log_filename:
            raise ValueError("Failed_log_filename is missing")
        self._failed_log_filename = failed_log_filename
    
    @property
    def success_log_filename(self):
        return self._success_log_filename
    
    @property
    def failed_log_filename(self):
        return self._failed_log_filename