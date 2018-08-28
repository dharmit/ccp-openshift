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
    def __init__(
            self, jenkins_server="localhost", jenkins_port=None, test=False
    ):
        self.jenkins_client = None
        self.test = test
        if not test:
            self.jenkins_client = OpenshiftJenkinsWorkflowAPIClient(
                server=jenkins_server,
                port=jenkins_port
            )

    def get_builds_count(self, ordered_job_list, test_data_set=None):
        """
        Get the count of build in the project. Helps indeciding id to query.
        :param ordered_job_list: The ordered list of jobs, with parents,
        followed by children
        :type ordered_job_list list
        :param test_data_set: data set to be used for test run.
        :type test_data_set list
        :return: A number representing number of builds in a job.This number
        will also be id of latest build. -1 is returned on failure.
        """
        if not self.test:
            data_set = self.get_data_from_response(
                self.jenkins_client.get_build_runs(ordered_job_list),
                bad_json=True
            )
        else:
            data_set = test_data_set
        if data_set:
            count = len(data_set)
        else:
            count = -1
        return count

    def get_stage_count(
            self, ordered_job_list, build_number, test_data_set=None
    ):
        """
        Gets the number of stages in a build of a project.
        :param ordered_job_list: The ordered list of jobs, with parents,
        followed by children
        :type ordered_job_list list
        :param build_number: The id of the build.
        :type build_number str
        :param test_data_set: data set to be used for test run.
        :type test_data_set dict
        :raises Exception
        :return: The number of stages in the project. None is returned on
        failure
        """
        result = None
        stages = None
        if not self.test:
            data_set = self.get_data_from_response(
                self.jenkins_client.describe_build_run(
                    ordered_job_list, build_number=build_number
                ),
                bad_json=True
            )
        else:
            data_set = test_data_set
        if data_set:
            stages = data_set.get("stages")
        if data_set and stages:
            result = len(stages)

        return result

    def get_stage_id(
            self, ordered_job_list, build_number, stage, stage_is_name=True,
            test_data_set=None
    ):
        """
        Gets the stage id, of a particular stage in a particular build of a
        project
        :param ordered_job_list: The ordered list of jobs, with parents,
        followed by children
        :type ordered_job_list list
        :param build_number: The id of the build.
        :type build_number str
        :param stage: The name of the pipeline stage of the build
        :type stage str
        :param stage_is_name: Default True, if true, stage is treated as name
        of stage, else it is treaded as stage number
        :type stage_is_name bool
        :param test_data_set: data set to be used for test run.
        :type test_data_set dict
        :raises Exception
        :return: The id of the stage, in build build_id in project
        ordered_job_list. None is returned on failure
        """
        result = None
        stages = None
        if not self.test:
            data_set = self.get_data_from_response(
                self.jenkins_client.describe_build_run(
                    ordered_job_list, build_number=build_number
                ),
                bad_json=True
            )
        else:
            data_set = test_data_set
        if data_set:
            stages = data_set.get("stages")
        if data_set and stages:
            if stage_is_name:
                for item in stages:
                    if item.get("name") == stage:
                        result = item.get("id")
                        break
            else:
                result = stages[int(stage)-1].get("id")

        return result

    def get_stage_flow_node_ids(
            self, ordered_job_list, build_number, node_number,
            test_data_set=None
    ):
        """
        Gets the stage flow node id the node where where a stage ran for build
        in project.
        :param ordered_job_list: The ordered list of jobs, with parents,
        followed by children
        :param build_number: The id of the build.
        :param node_number: The number of the node, this is usually the stage
        id got from get_stage_id
        :param test_data_set: data set to be used for test run.
        :return: The ids of the stage flow nodes, None on failure
        """
        result = None
        stage_flow_nodes = None
        stage_flow_node_ids = []
        if not self.test:
            data_set = self.get_data_from_response(
                self.jenkins_client.describe_execution_node(
                    ordered_job_list, build_number, node_number
                ),
                bad_json=True
            )
        else:
            data_set = test_data_set
        if data_set:
            stage_flow_nodes = data_set.get("stageFlowNodes")
        if data_set and stage_flow_nodes:
            for item in stage_flow_nodes:
                stage_flow_node_ids.append(
                    item.get("id")
                )
            result = stage_flow_node_ids
        return result

    def get_stage_logs(
            self, ordered_job_list, build_number, stage, stage_is_name=True,
            test_data_set=None
    ):
        """
        Gets the logs of a particular stage of a particular build of a project.
        :param ordered_job_list: The ordered list of jobs, with parents,
        followed by children
        :type ordered_job_list list
        :param build_number: The id of the build
        :type build_number str
        :param stage: The name of the stage whole logs are to be fetched
        :type stage str
        :param stage_is_name : Default True, if true, stage is treated as name
        of stage, else it is treaded as stage number
        :type stage_is_name bool
        :param test_data_set: data set to be used for test run.
        :return: A string containing the logs. None is returned on failure
        """
        result = None
        stage_flow_nodes = None
        if not self.test:
            stage_id = self.get_stage_id(
                ordered_job_list, build_number=build_number, stage=stage,
                stage_is_name=stage_is_name
            )
        else:
            stage_id = self.get_stage_id(
                ordered_job_list, build_number=build_number, stage=stage,
                test_data_set=test_data_set[0]
            )
        if stage_id:
            if not self.test:
                stage_flow_nodes = self.get_stage_flow_node_ids(
                    ordered_job_list, build_number=build_number,
                    node_number=stage_id
                )
            else:
                stage_flow_nodes = self.get_stage_flow_node_ids(
                    ordered_job_list, build_number=build_number,
                    node_number=stage_id, test_data_set=test_data_set[1]
                )
        if stage_flow_nodes:
            if not self.test:
                result = []
                for n in stage_flow_nodes:
                    r = self.get_data_from_response(
                        self.jenkins_client.get_logs_of_execution_node(
                            ordered_job_list, build_number=build_number,
                            node_number=n
                        )
                    )
                    if r:
                        result.append(
                            {
                                "log": r.get("text"),
                                "name": r.get("name"),
                                "description": r.get("parameterDescription")
                            }
                        )
            else:
                result = [
                    stage_id,
                    stage_flow_nodes,
                    test_data_set[2].get("text")
                ]

        return result
