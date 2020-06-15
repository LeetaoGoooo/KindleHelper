
class ConfigNotFoundError(FileNotFoundError):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)


class ConfigLackException(Exception):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)