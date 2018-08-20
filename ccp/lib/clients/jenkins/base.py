from ccp.lib.clients.utils.authorization import BearerAuthorization
from ccp.lib.clients.base import ApiClient
from ccp.lib.clients.openshift.client import OpenshiftCmdClient


class OpenshiftJenkinsBaseAPIClient(ApiClient):
    """
    Acts as base for all Jenkins API Clients
    """

    def __init__(
            self,
            server="localhost",
            port=None
    ):
        super(OpenshiftJenkinsBaseAPIClient, self).__init__(
            secure=False,
            verify_ssl=False,
            server=server,
            port=port,
            authorization=BearerAuthorization(
                OpenshiftCmdClient().get_jenkins_service_account_token()
            ),
        )
