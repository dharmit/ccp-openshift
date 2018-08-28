"""
This file contains ready to use Jenkins Clients.
"""

from ccp.lib.clients.jenkins.base import OpenshiftJenkinsBaseAPIClient


class OpenshiftJenkinsWorkflowAPIClient(OpenshiftJenkinsBaseAPIClient):
    """
    Helps query the jenkins workflow API endpoints.
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
        super(OpenshiftJenkinsWorkflowAPIClient, self).__init__(
            server=server,
            port=port
        )

    def get_build_runs(self, job_ordered_list):
        """
        Gets the build runs of specified job/subjob from API server
        :param job_ordered_list: The ordered list of jobs, with parents,
        followed by children
        :type job_ordered_list list
        :raises Exception
        :return: The Response returned by API server, if it is received.
        """
        return self._query(
            "{}/wfapi/runs".format(
                self._jenkins_jobs_from_jobs_ordered_list(
                    job_ordered_list
                )
            )
        )

    def describe_build_run(self, job_ordered_list, build_number):
        """
        Describes a particular build run of job/subjob from API server
        :param job_ordered_list: The ordered list of jobs, with parents,
        followed by children
        :type job_ordered_list list
        :param build_number: The number of build to describe.
        :type build_number str
        :raises Exception
        :return: The Response returned by the API server, if it is received.
        """
        return self._query(
            "{}/{}/wfapi/describe".format(
                self._jenkins_jobs_from_jobs_ordered_list(
                    job_ordered_list
                ),
                build_number
            )
        )

    def describe_execution_node(
            self, job_ordered_list, build_number, node_number
    ):
        """
        Describes an execution node for job/subjob from API server
        :param job_ordered_list: The ordered list of jobs, with parents,
        followed by children
        :param build_number:The number of the build to describe.
        :param node_number: The number of the node to describe
        :raises Exception
        :return: The Response from the API server, if it is received.
        """
        return self._query(
            "{}/{}/execution/node/{}/wfapi/describe".format(
                self._jenkins_jobs_from_jobs_ordered_list(
                    job_ordered_list
                ),
                build_number,
                node_number
            )
        )

    def get_logs_of_execution_node(
            self, job_ordered_list, build_number, node_number
    ):
        """
        Lets the logs of a jenkins execution node, if possible
        :param job_ordered_list: The ordered list of jobs, with parents,
        followed by children
        :param build_number: The number of the build to describe.
        :param node_number: The number of the node to describe
        :raises Exception
        :return: The response from API server, if it is received.
        """
        return self._query(
            "{}/{}/execution/node/{}/wfapi/log".format(
                self._jenkins_jobs_from_jobs_ordered_list(
                    job_ordered_list
                ),
                build_number,
                node_number
            )
        )
