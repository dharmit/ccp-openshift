"""
This file contains Jenkins query processors for build information
"""

from ccp.lib.processors.base import JSONQueryProcessor
from ccp.lib.clients.jenkins.client import OpenshiftJenkinsWorkflowAPIClient


class BuildInfo(JSONQueryProcessor):
    """
    This class processes queried information from jenkins
    for requested information.
    """
    def __init__(self, jenkins_server="localhost", jenkins_port=None):
        self.jenkins_client = OpenshiftJenkinsWorkflowAPIClient(
            server=jenkins_server,
            port=jenkins_port
        )

    def get_builds_count(self, ordered_job_list):
        """
        Get the count of build in the project. Helps indeciding id to query.
        :param ordered_job_list: The ordered list of jobs, with parents,
        followed by children
        :return: A number representing number of builds in a job.This number
        will also be id of latest build. -1 is returned on failure.
        """
        data_set = self.get_data_from_response(
            self.jenkins_client.get_build_runs(ordered_job_list)
        )
        if data_set:
            count = len(data_set)
        else:
            count = -1
        return count

    def get_stage_id(self, ordered_job_list, build_number, stage):
        """
        Gets the stage id, of a particular stage in a particular build of a
        project
        :param ordered_job_list: The ordered list of jobs, with parents,
        followed by children
        :param build_number: The id of the build.
        :param stage: The name of the pipeline stage of the build
        :return: The id of the stage, in build build_id in project
        ordered_job_list. None is returned on failure
        """
        result = None
        stages = None
        data_set = self.get_data_from_response(
            self.jenkins_client.describe_build_run(
                ordered_job_list, build_number=build_number
            )
        )
        if data_set:
            stages = data_set.get("stages")
        if data_set and stages:
            for item in stages:
                if item.get("name") == stage:
                    result = item.get("id")
                    break
        return result

    def get_stage_flow_node_id(
            self, ordered_job_list, build_number, node_number
    ):
        """
        Gets the stage flow node id the node where where a stage ran for build
        in project.
        :param ordered_job_list: The ordered list of jobs, with parents,
        followed by children
        :param build_number: The id of the build.
        :param node_number: The number of the node, this is ussually the stage
        id got from get_stage_id
        :return: The id of the stage flow node, None on failure
        """
        result = None
        stage_flow_nodes = None
        data_set = self.get_data_from_response(
            self.jenkins_client.describe_execution_node(
                ordered_job_list,build_number, node_number
            )
        )
        if data_set:
            stage_flow_nodes = data_set.get("stageFlowNodes")
        if data_set and stage_flow_nodes:
            result = stage_flow_nodes.get("id")
        return result

    def get_stage_logs(self, ordered_job_list, build_number, stage_name):
        """
        Gets the logs of a particular stage of a particular build of a project.
        :param ordered_job_list: The ordered list of jobs, with parents,
        followed by children
        :param build_number: The id of the build
        :param stage_name: The name of the stage whole logs are to be fetched
        :return: A string containing the logs. None is returned on failure
        """
        result = None
        stage_id = self.get_stage_id(
            ordered_job_list, build_number=build_number, stage=stage_name
        )
        if stage_id:
            stage_flow_node = self.get_stage_flow_node_id(
                ordered_job_list, build_number=build_number,
                node_number=stage_id
            )
            if stage_flow_node:
                result = self.get_data_from_response(
                    self.jenkins_client.get_logs_of_execution_node(
                        ordered_job_list, build_number=build_number,
                        node_number=stage_flow_node
                    )
            )
        return result
