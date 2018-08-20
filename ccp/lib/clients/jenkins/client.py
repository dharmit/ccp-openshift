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

    def get_runs(self, ordered_project_list):
        return self._query(
            "{}/wfapi/runs".format(
                self._jenkins_jobs_from_jobs_ordered_list(
                    ordered_project_list
                )
            )
        )

    def describe_build_run(
            self, ordered_projects_list, build_number
    ):
        return self._query(
            "{}/{}/wfapi/describe".format(
                self._jenkins_jobs_from_jobs_ordered_list(
                    ordered_projects_list
                ),
                build_number
            )
        )

    def describe_execution_node(
            self, ordered_projects_list, build_number, node_number
    ):
        return self._query(
            "{}/{}/execution/node/{}/wfapi/describe".format(
                self._jenkins_jobs_from_jobs_ordered_list(
                    ordered_projects_list
                ),
                build_number,
                node_number
            )
        )

    def get_logs_of_execution_node(
            self, ordered_projects_list, build_number, node_number
    ):
        return self._query(
            "{}/{}/execution/node/{}/wfapi/log".format(
                self._jenkins_jobs_from_jobs_ordered_list(
                    ordered_projects_list
                ),
                build_number,
                node_number
            )
        )
