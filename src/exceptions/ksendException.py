
class EmailSendException(Exception):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)


class SendFileNotFoundError(FileNotFoundError):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)