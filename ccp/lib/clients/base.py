"""
This file conains the base for all client ways of querying data.
"""

from ccp.lib.utils import request_url, run_cmd


class Client(object):
    """
    Base class of all clients
    """
    pass


class APIClient(Client):
    """
    Base class for all clients that query an API Server for information
    """
    def __init__(
            self,
            secure=True,
            verify_ssl=True,
            authorization=None,
            server="localhost",
            port="none"
    ):
        self.server_endpoint = "{}://{}{}".format(
            "https" if secure else "http",
            server if server else "localhost",
            ":{}".format(
                port
            ) if port else ""
        )
        self.authorization = authorization
        self.skip_ssl = verify_ssl

    def _query(self, target):
        """
        Given a target (query without url), queries endpoint and gets data
        :param target: The query to send to the api server, including after
        destination
        :type target str
        :return:The response object and exception object, if any was raised.
        """
        query_url = "{}{}".format(
            self.server_endpoint,
            target
        )
        headers = {}

        self.authorization.add_header(headers)
        return request_url(
            query_url, verify_ssl=self.skip_ssl, headers=headers
        )


class CmdClient(Client):
    pass
