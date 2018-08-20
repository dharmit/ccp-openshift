"""
This file conains the base for all client ways of querying data.
"""

from ccp.lib.utils import request_url, run_cmd


class Client(object):
    pass


class ApiClient(Client):
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
