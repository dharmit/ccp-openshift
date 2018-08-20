"""
This file contains ready to use Jenkins Clients.
"""
from ccp.lib.clients.jenkins.base import OpenshiftJenkinsBaseAPIClient


class OpenshiftJenkinsWorkflowAPIClient(OpenshiftJenkinsBaseAPIClient):
    """
    Helps query the jenkins workflow api endpoints.
    """

    def __init__(
            self,
            server="localhost",
            port=None
    ):
        super(OpenshiftJenkinsWorkflowAPIClient, self).__init__(
            server=server,
            port=port
        )

    def get_build_runs(self, ordered_jobs_list):
        """
        Gets the build runs of specified job/subjob from API server
        :param ordered_jobs_list: The ordered list of jobs, with parents,
        followed by children
        :type ordered_jobs_list list
        :return: The Response returned by api server.
        """
        return self._query(
            "{}/wfapi/runs".format(
                self._jenkins_jobs_from_jobs_ordered_list(
                    ordered_jobs_list
                )
            )
        )

    def describe_build_run(
            self, ordered_jobs_list, build_number
    ):
        """
        Describes a particular build run of job/subjob from API server
        :param ordered_jobs_list: The ordered list of jobs, with parents,
        followed by children
        :type ordered_jobs_list list
        :param build_number: The number of build to describe.
        :type build_number str
        :return: The Response returned by the API server.
        """
        return self._query(
            "{}/{}/wfapi/describe".format(
                self._jenkins_jobs_from_jobs_ordered_list(
                    ordered_jobs_list
                ),
                build_number
            )
        )

    def describe_execution_node(
            self, ordered_jobs_list, build_number, node_number
    ):
        """
        Describes an execution node for job/subjob from API server
        :param ordered_jobs_list: The ordered list of jobs, with parents,
        followed by children
        :param build_number:The number of the build to describe.
        :param node_number: The number of the node to describe
        :return: The Response from the api server
        """
        return self._query(
            "{}/{}/execution/node/{}/wfapi/describe".format(
                self._jenkins_jobs_from_jobs_ordered_list(
                    ordered_jobs_list
                ),
                build_number,
                node_number
            )
        )

    def get_logs_of_execution_node(
            self, ordered_jobs_list, build_number, node_number
    ):
        return self._query(
            "{}/{}/execution/node/{}/wfapi/log".format(
                self._jenkins_jobs_from_jobs_ordered_list(
                    ordered_jobs_list
                ),
                build_number,
                node_number
            )
        )
