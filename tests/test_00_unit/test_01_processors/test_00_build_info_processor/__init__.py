import unittest


from ccp.lib.processors.pipeline_information.builds import BuildInfo


class TestBuildInfo(unittest.TestCase):
    """
    Tests the BuildInfo Processor that queries jenkins and processes returned
    information
    """
    def setUp(self):
        self.ordered_project_list = [
            "test",
            "test1"
        ]
        self.test_jenkins_server = "localhost"
        self.test_jenkins_port = "10000"
        self.test_build_number = "1"
        self.test_node_number = "2"
        self.test_stage_flow_node_number = "3"
        self.test_stage_name = "Test Stage"
        self.test_logs = "Test logs"

        self.build_info = BuildInfo(
            jenkins_server=self.test_jenkins_server,
            jenkins_port=self.test_jenkins_port,
            test=True
        )

    def test_00_gets_correct_build_count(self):

        test_data_set = [
            {
                "_links": {
                    "self": {
                        "href": "blah"
                    }
                },
                "durationMillis": 0,
                "id": self.test_build_number
            }
        ]

        self.assertEquals(
            self.build_info.get_builds_count(
                self.ordered_project_list,
                test_data_set=test_data_set
            ),
            1,
            "Both are equal"
        )

    def test_01_gets_correct_stage_id(self):

        test_data_set = {
            "_links": {
                "self": {
                    "href": "blah"
                }
            },
            "durationMillis": 0,
            "id": self.test_build_number,
            "stages": [
                {
                    "_links": {
                        "self": {
                            "href": "blah"
                        }
                    },
                    "id": "1",
                    "name": "blah stage"
                },
                {
                    "_links": {
                        "self": {
                            "href": "blah"
                        }
                    },
                    "id": self.test_node_number,
                    "name": self.test_stage_name
                }
            ]
        }

        self.assertEquals(
            self.build_info.get_stage_id(
                self.ordered_project_list,
                self.test_build_number,
                self.test_stage_name,
                test_data_set=test_data_set
            ),
            self.test_node_number,
            "Both are equal"
        )

    def test_02_gets_correct_stage_flow_id(self):

        test_data_set = {
            "_links": {
                "self": {
                    "href": "blah"
                }
            },
            "id": self.test_node_number,
            "name": self.test_stage_name,
            "pauseDurationMillis": 0,
            "stageFlowNodes": [
                {
                    "_links": {
                        "self": {
                            "href": "blah"
                        }
                    },
                    "durationMillis": 0,
                    "id": self.test_stage_flow_node_number,
                    "name": "blah",
                    "parentNodes": [
                        self.test_node_number
                    ]
                }
            ]
        }

        self.assertEquals(
            self.build_info.get_stage_flow_node_id(
                self.ordered_project_list,
                self.test_build_number,
                self.test_node_number,
                test_data_set=test_data_set
            ),
            self.test_stage_flow_node_number,
            "Both are equal"
        )

    def test_03_gets_logs_correcty(self):

        test_data_set = [
            {
                "_links": {
                    "self": {
                        "href": "blah"
                    }
                },
                "durationMillis": 0,
                "id": self.test_build_number,
                "stages": [
                    {
                        "_links": {
                            "self": {
                                "href": "blah"
                            }
                        },
                        "id": "1",
                        "name": "blah stage"
                    },
                    {
                        "_links": {
                            "self": {
                                "href": "blah"
                            }
                        },
                        "id": self.test_node_number,
                        "name": self.test_stage_name
                    }
                ]
            },
            {
                "_links": {
                    "self": {
                        "href": "blah"
                    }
                },
                "id": self.test_node_number,
                "name": self.test_stage_name,
                "pauseDurationMillis": 0,
                "stageFlowNodes": [
                    {
                        "_links": {
                            "self": {
                                "href": "blah"
                            }
                        },
                        "durationMillis": 0,
                        "id": self.test_stage_flow_node_number,
                        "name": "blah",
                        "parentNodes": [
                            self.test_node_number
                        ]
                    }
                ]
            },
            {
                "text": self.test_logs
            }
        ]
        # Note this will not test actual result which would be the logs
        # themselves, but for test purposes, for now assumes that logs are
        # correct so long as correct stage and stageflow are identified
        self.assertEquals(
            self.build_info.get_stage_logs(
                self.ordered_project_list,
                self.test_build_number,
                self.test_stage_name,
                test_data_set=test_data_set
            ),
            [
                self.test_node_number,
                self.test_stage_flow_node_number,
                self.test_logs
            ]
        )
