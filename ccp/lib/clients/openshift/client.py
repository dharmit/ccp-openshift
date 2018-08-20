from ccp.lib.clients.base import CmdClient
import ccp.lib.utils


class OpenshiftCmdClient(CmdClient):
    """
    Basic openshift client
    """

    def __init__(self):
        self.base_cmd = "oc{globalflags} {operation} {what}{which}"

    def get_jenkins_service_account_token(self):
        """
        Queries and gets the jenkins token. This assumes you have access to oc
        command line.
        :return: The token, if it was able to get it.
        """
        token = None
        token_cmd = """
        oc get sa/jenkins --template='{{range .secrets}}{{ .name }} {{end}}' |
         xargs -n 1 oc get secret --template='{{ if .data.token }}{{ .data.token
          }}{{end}}' | head -n 1 | base64 -d -
        """
        out, ex = ccp.lib.utils.run_cmd(token_cmd, shell=True, use_pipes=True)
        if ex:
            raise Exception("Failed to get token due to {}".format(ex))
        else:
            data, err = out
            if data:
                token = data
            else:
                raise Exception("Failed to get token due to {}".format(err))
        return token
