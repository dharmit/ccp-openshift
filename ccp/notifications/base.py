#!/usr/bin/env python2

# This python module defines a BaseNotify class
# to be inheirted by child build and weekly scan classes.
# This is a single place to lookup for formatting of subject
# and email body for notifications email to be sent to users.


class BaseNotify(object):
    """
    BaseNotify class has related common methods and
    initialization for build and weekly scan notification
    classes.
    """

    def __init__(self):
        # container build success/failure subject lines
        self.build_success_subj = \
            "[registry.centos.org] SUCCESS: Container build {}"
        self.build_failure_subj = \
            "[registry.centos.org] FAILED: Container build {}"
        # weekly scan success/failure subject lines
        self.weekly_success_subj = "SUCCESS: Weekly scan for {} is complete"
        self.weekly_failure_subj = "FAILED: Weekly scan for {} has failed"

        # for build success notifications
        self.build_success_body = """\
{0:<30}{1}
{2:<30}{3}
{4:<30}{5}"""

        # for build failure notifications
        self.build_failure_body = """\
{0:<30}{1}
{2:<30}{3}"""

        # for weekly scan success/failure case
        self.weekly_body = """\
{0: <20}{1}
{2: <20}{3}"""

        # for weekly scan failure case when image is absent in registry
        self.weekly_image_absent_body = "{0: <20}{1}"

        # email footer to be added in all types of notifications
        self.email_footer = """\
--
Do you have a query?
Talk to Pipeline team on #centos-devel at freenode
CentOS Community Container Pipeline Service
https://wiki.centos.org/ContainerPipeline
https://github.com/centos/container-index
"""
