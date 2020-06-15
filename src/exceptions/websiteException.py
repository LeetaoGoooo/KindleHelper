
class NecessaryElementNotFoundException(Exception):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)


class NetWorkException(Exception):
    def __init__(self, tag, status_code, response):
        print(f'{tag} exception \n status_code : {status_code} \n response: {response}')