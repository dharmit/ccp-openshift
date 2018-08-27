"""
This file contains operational Openshift clients
"""

from ccp.lib.clients.base import CmdClient
import ccp.lib.utils


class OpenshiftCmdClient(CmdClient):
    """
    Basic openshift client
    """

    def __init__(self):
        self.core_oc_cmd = "/usr/bin/oc"
        self.oc_params = "{globalflags} {operation} {what}{which}"

    def get_jenkins_service_account_token(self):
        """
        Queries and gets the Jenkins token. This assumes you have access to oc
        command line.
        :return: The token, if it was able to get it. Else, it returns None
        """
        token_cmd = """{core_oc_cmd} get sa/jenkins --template='{template1}' | \
        xargs -n 1 {core_oc_cmd} get secret --template='{template2}' | \
        head -n 1 | base64 -d -\
        """.format(
            core_oc_cmd=self.core_oc_cmd,
            template1="{{range .secrets}}{{ .name }} {{end}}",
            template2="{{ if .data.token }}{{ .data.token }}{{end}}"
        )
        out, ex = ccp.lib.utils.run_cmd(token_cmd, shell=True, use_pipes=True)
        if ex:
            raise Exception("Failed to get token due to {}".format(ex))
        else:
            if out:
                return out.strip()
            return None

