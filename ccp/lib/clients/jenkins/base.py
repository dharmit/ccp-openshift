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
            server,
            port=None
    ):
        """
        Initialize Openshift Jenkins Client
        :param server: The URL/IP of jenkins server on openshift.
        :type server str
        :param port: Default None: The port, if any.
        :type port: str
        """
        jenkins_sa_token = OpenshiftCmdClient().\
            get_jenkins_service_account_token()
        authorization = BearerAuthorization(token=jenkins_sa_token)
        super(OpenshiftJenkinsBaseAPIClient, self).__init__(
            server=server,
            secure=False,
            verify_ssl=False,
            port=port,
            authorization=authorization,
        )

    def _jenkins_jobs_from_jobs_ordered_list(self, nested_job_ordered_list):
        """
        Formats query part of URL from ordered job list as /job/j1/job/j2
        :param nested_job_ordered_list: The ordered list of jenkins job names,
        with parent as first and every child below.
        :type nested_job_ordered_list list
        :return: A string of the form /job/j1/job/j2...
        """
        dest = ""
        for i in nested_job_ordered_list:
            dest = "{}/job/{}".format(
                dest,
                i
            )
        return dest
