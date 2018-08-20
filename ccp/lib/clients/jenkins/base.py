"""
This file contains the base of all jenkins clients
"""

from ccp.lib.clients.utils.authorization import BearerAuthorization
from ccp.lib.clients.base import APIClient
from ccp.lib.clients.openshift.client import OpenshiftCmdClient


class OpenshiftJenkinsBaseAPIClient(APIClient):
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

    def _jenkins_jobs_from_jobs_ordered_list(self, jobs_ordered_list):
        """
        Formats query part of url from ordered job list as /job/j1/job/j2
        :param jobs_ordered_list: The ordered list of jenkins job names, with
        parent as first and every child below.
        :return: A string of the form /job/j1/job/j2...
        """
        dest = ""
        for i in jobs_ordered_list:
            dest = "{}/job/{}".format(
                dest,
                i
            )
        return dest
