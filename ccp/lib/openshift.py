from ccp.lib.utils import run_cmd


class OpenshiftCmdClient(object):

    def __init__(self, namespace=None):
        self.namespace = namespace
        self.oc_cmd = "oc "
        self.oc_apply_cmd = str.format(
            "{} apply {} -f -",
            self.oc_cmd,
            "" if not self.namespace else "-n {}".format(self.namespace)

        )
        self.oc_get_cmd = str.format(
            "{} get {obj} {} ",
            self.oc_cmd,
            "" if not self.namespace else "-n {}".format(self.namespace),
            obj="{obj}"
        )
        self.oc_process_cmd = str.format(
            "{} process {} ",
            self.oc_cmd,
            "" if self.namespace else "-n {}".format(self.namespace)
        )

    def oc_process(self, what, params, extra=None, apply=True):
        p = ""
        for k, v in params:
            p = str.format(
                "{} -p {}={}",
                p, k, v
            )
        command = str.format(
            "{process_cmd} {process_what} {process_params}{extra} {apply}",
            process_cmd=self.oc_process_cmd,
            process_what=what,
            process_params=p,
            extra=extra if extra else "",
            apply=self.oc_apply_cmd if apply else ""
        )
        return run_cmd(command, shell=True)


class BuildConfigManager(OpenshiftCmdClient):

    def __init__(self, registry_url, namespace, from_address, smtp_server):
        super(BuildConfigManager, self).__init__(namespace)
        self.registry_url = registry_url
        self.namespace = namespace
        self.from_address = from_address
        self.smtp_server = smtp_server

