#! /usr/bin/python -W ignore
"""
This file contains the command line tooling to get pipeline information
"""

from ccp.lib.processors.pipeline_information.builds import BuildInfo
import argparse


def _run_handler(key, handlers, lmd=None):
    """

    :param key: The key to filter the handler
    :param handlers: The dict containing the string and handler function as key
    and value
    :type handlers dict
    :param lmd: Default None, the lambda, what should happen if it does not
    match
    :return: The return of the call of handler, if it can get it or None
    """
    h = handlers.get(
        key,
        lambda : lmd
    )
    if h:
        return h()
    else:
        return None


class Engine(object):
    """
    The engine is the one that parses the arguments and takes action on them.
    """

    def __init__(self):
        self.args = None
        self.jenkins_server = None
        self._init_parser()

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
                "logs",
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

    def _handle_build_logs(self):
        """
        Fetches entire log collection
        :return: The output to be printed
        """
        job = self.args.job
        build_info = BuildInfo(jenkins_server=self.jenkins_server)
        buildid = self.args.buildid
        if not buildid:
            out = "Need build number to fetch stages of"
        else:
            build_logs = build_info.get_build_logs(
                ordered_job_list=job, build_number=buildid
            )
            out = ""
            if build_logs:
                for stage_info in build_logs:
                    logs = ""
                    logs_info = stage_info.get("logs")
                    if logs_info:
                        for item in logs_info:
                            log = item.get('log')
                            name = item.get('name')
                            description = item.get('description')
                            logs = "{}{}{}{}\n".format(
                                logs,
                                "" if not name else "Name : {}\n".format(
                                    name
                                ),
                                "" if not description else
                                "Description: {}\n".format(
                                    description
                                ),
                                log if log else "No Logs"
                            )
                    else:
                        logs = "No logs could be fetched. might be a parent" \
                               " stage\n"
                    out = "{}STAGE : {}\n{}\n".format(
                        out,
                        stage_info.get("name"),
                        logs
                    )
        return out

    def _handle_builds(self):
        """
        Handles all operations related to build sub-command
        """
        what = self.args.what
        out = _run_handler(
            key=what,
            handlers={
                "logs": self._handle_build_logs,
                "stage-count": self._handle_build_stage_count,
                "stage-logs": self._handle_build_stage_logs
            }
        )
        print(
            out if out else "Could not get the requested information"
        )

    def _handle_object(self, obj):
        """
        Runs the appropriate sub command handler (object to handle)
        :param obj: The name of object.
        """
        _run_handler(
            key=obj,
            handlers={
                "build": self._handle_builds
            }
        )

    def run(self):
        """
        Run the engine
        """
        self._handle_object(self.args.object)


if __name__ == '__main__':
    Engine().run()
