"""
This file contains authorization handlers that take care of adding the header.
"""


class Authorization(object):
    """
    Base class for all the authorization mechanisms
    """
    def __init__(self):
        self.authorization_header_string = ""

    def add_header(self, headers):
        """
        Adds appropriately formatted Authorization header
        :param headers: The headers dict to populate
        :type dict
        """
        headers["Authorization"] = self.authorization_header_string


class BearerAuthorization(Authorization):
    """
    Handles setting up request header for Bearer Authorization.
    """
    def __init__(self, token):
        super(BearerAuthorization, self).__init__()
        self.authorization_header_string = "Bearer %s" % token
