
class Authorization(object):
    """
    Base class for all the authorization mechanisms
    """
    def __init__(self):
        self.authorization_header_string = ""

    def add_header(self, headers):
        headers["Authorization"] = self.authorization_header_string


class BearerAuthorization(Authorization):
    def __init__(self, token):
        super(BearerAuthorization, self).__init__()
        self.authorization_header_string = "Bearer %s" % token
