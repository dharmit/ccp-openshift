from ccp.lib.processors.pipeline_information.builds import BuildInfo
import argparse


class Engine(object):

    def __init__(self):
        self.args = None
        self.jenkins_server = None
        self.init_parser()

    def init_parser(self):
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
            "-s", "--stage",
            help="Provide the name of the stage."
        )
        build_subcommand.add_argument(
            "what",
            default="logs",
            choices=[
                "logs"
            ]
        )

        self.args = parser.parse_args()

    def handle_builds(self):
        what = self.args.what
        job = self.args.job
        build_info = BuildInfo(jenkins_server=self.jenkins_server)
        if what == "logs":
            buildid = self.args.buildid
            stage = self.args.stage
            if not buildid or not stage:
                print("Missing buildid or stage needed to fetch logs")
                return
            logs_info = build_info.get_stage_logs(
                ordered_job_list=job,
                build_number=buildid,
                stage=stage
            )
            data = ""
            for item in logs_info:
                log = item.get('log')
                name = item.get('name')
                description = item.get('description')
                data = "{}{}{}{}\n".format(
                    data,
                    "" if not name else "Name : {}\n".format(
                        name
                    ),
                    "" if not description else "Description: {}\n".format(
                        description
                    ),
                    log if log else "No Logs"
                )
            print(data)

    def run_handler(self, obj):
        self.jenkins_server = self.args.jenkinsserver
        handlers = {
            "build": self.handle_builds()
        }

        h = handlers.get(
            obj,
            lambda: None
        )
        if h:
            h()

    def run(self):
        self.run_handler(self.args.object)


if __name__ == '__main__':
    Engine().run()