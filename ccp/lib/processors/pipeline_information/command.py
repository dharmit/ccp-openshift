#! /usr/bin/python -W ignore
"""
This file contains the command line tooling to get pipeline information
"""

from ccp.lib.processors.pipeline_information.builds import BuildInfo
import argparse


class Engine(object):
    """
    The engine is the one that parses the arguments and takes action on them.
    """

    def __init__(self):
        self.args = None
        self.jenkins_server = None
        self._handlers = None
        self._build_handlers = None
        self._init_parser()
        self._init_handlers()

    def _init_handlers(self):
        """
        Initializes the handlers
        """
        self._handlers = {
            "build": self._handle_builds()
        }
        self._build_handlers = {
            "stage-count": self._handle_build_stage_count(),
            "stage-logs": self._handle_build_stage_logs()
        }

    def _init_parser(self):
        """
        Initialises the argument parser and parses arguments.
        """
        parser = argparse.ArgumentParser(
            description="This tool can be used to query pipeline information."
        )
        parser.add_argument(
            "-s",
            "--jenkinsserver",
            help="Give url of jenkins server without port",
            required=True
        )
        sub_parsers = parser.add_subparsers(
            help="The type of information you are looking for",
            dest="object"
        )

        # Build Sub Command
        build_subcommand = sub_parsers.add_parser(
            "build", help="Interact with pipeline builds",
        )

        # Build Sub Command params
        build_subcommand.add_argument(
            "-j", "--job", nargs="+",
            help="Provide ordered list of jobs, where previous job is parent of"
                 " next. This is mainly for directories in jenkins",
            required=True
        )
        build_subcommand.add_argument(
            "-b", "--buildid",
            help="Provide the id of the build, whole logs you want",
        )
        build_subcommand.add_argument(
            "--stagename",
            help="Provide the name of the stage."
        )
        build_subcommand.add_argument(
            "--stagenumber",
            help="Provide the number of the stage."
        )
        build_subcommand.add_argument(
            "what",
            default="logs",
            choices=[
                "stage-logs",
                "stage-count"
            ]
        )

        self.args = parser.parse_args()
        self.jenkins_server = self.args.jenkinsserver
        if not self.jenkins_server:
            raise Exception(
                "Could not extract information about jenkins server"
            )

    def _handle_build_stage_logs(self):
        """
        Handles getting build stage logs
        :return: The output to be printed
        """
        out = ""
        job = self.args.job
        build_info = BuildInfo(jenkins_server=self.jenkins_server)
        buildid = self.args.buildid
        stage = self.args.stagename or self.args.stagenumber
        stage_is_name = bool(self.args.stagename)
        if not buildid or not stage:
            print("Missing buildid or stage needed to fetch logs")
            return
        logs_info = build_info.get_stage_logs(
            ordered_job_list=job,
            build_number=buildid,
            stage=stage,
            stage_is_name=stage_is_name
        )
        for item in logs_info:
            log = item.get('log')
            name = item.get('name')
            description = item.get('description')
            out = "{}{}{}{}\n".format(
                out,
                "" if not name else "Name : {}\n".format(
                    name
                ),
                "" if not description else "Description: {}\n".format(
                    description
                ),
                log if log else "No Logs"
            )
        return out

    def _handle_build_stage_count(self):
        """
        Handles getting build stage count
        :return: The output to be printed
        """
        job = self.args.job
        build_info = BuildInfo(jenkins_server=self.jenkins_server)
        buildid = self.args.buildid
        if not buildid:
            out = "Need build number to fetch stages of"

        else:
            out = build_info.get_stage_count(
                ordered_job_list=job,
                build_number=buildid
            )
        return out

    def _handle_builds(self):
        """
        Handles all operations related to build sub-command
        """
        what = self.args.what
        h = self._build_handlers.get(
            what,
            lambda: None
        )

        if h:
            out = h()
            print(out)

    def _run_handler(self, obj):
        """
        Runs the appropriate sub command handler
        :param obj: The sub command
        """

        h = self._handlers.get(
            obj,
            lambda: None
        )
        if h:
            h()

    def run(self):
        """
        Run the engine
        """
        self._run_handler(self.args.object)


if __name__ == '__main__':
    Engine().run()
