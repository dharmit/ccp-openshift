from ccp.lib.clients.jenkins.base import OpenshiftJenkinsBaseAPIClient


class OpenshiftJenkinsWorkflowAPIClient(OpenshiftJenkinsBaseAPIClient):

    def __init__(
            self,
            server="localhost",
            port=None
    ):
        super(OpenshiftJenkinsWorkflowAPIClient, self).__init__(
            server=server,
            port=port
        )

    def describe_build_run(self, project, build_number, super_project=None):
        return self._query(
            "{}/job{}{}".format(
                "/" + super_project + "/job" if super_project else "",
                "/" + project,
                "/" + build_number
            )
        )
