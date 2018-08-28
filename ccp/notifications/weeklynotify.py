#!/usr/bin/env python2

# This python module takes care of getting required details
# and sending email to user about weekly scan


import sys

from ccp.notifications.base import BaseNotify
from ccp.lib.openshift import BuildInfo
from ccp.lib.email import SendEmail


class WeeklyScanNotify(BaseNotify):
    """
    Notify class has related methods to notify
    user about weekly scan status and info
    """

    def __init__(self):
        super(WeeklyScanNotify, self).__init__()

        # create build info object to retrieve build info to send email
        self.buildinfo_obj = BuildInfo(
            service_account="sa/jenkins",
            required_fields=[
                "NOTIFY_EMAIL",
                "REGISTRY_URL",
                "FROM_ADDRESS",
                "SMTP_SERVER"])
        # create send email utility object for sending emails
        self.sendemail_obj = SendEmail()

    def body_of_email(self, status, repository):
        """
        Generate the body of email for weekly scan notification email

        :param status: Status of build - True=Success False=Failure
        :type status bool
        :param repository: Repository name with https:// prefix
        :type repository str
        :return: Body of email in text
        """

        if status:
            body = self.weekly_body.format(
                "Scan status:", "Success",
                "Repository:", repository)
        else:
            body = self.weekly_body.format(
                "Scan status:", "Failure",
                "Repository:", repository)

        return body + "\n\n" + self.email_footer

    def image_absent_email_body(self):
        """
        Generates the body of email for weekly scan notification when
        image is absent in the registry and scan has failed.

        :return: Body of email in text
        """
        body = self.weekly_image_absent_body.format(
            "Scan status:",
            "Image is absent in the registry, scan is aborted.")
        return body + "\n\n" + self.email_footer

    def notify(self,
               status, namespace, jenkins_url,
               image_name, build_number):
        """
        Notify the user by sending email about weekly scan info

        :param status: Status of weekly scan performed
                       ["success", "failed", "image_absent"]
        :type status str
        :param namespace: Namespace of the build
        :type namespace str
        :param jenkins_url: Jenkins URL to fetch the build info
        :type jenkins_url str
        :param image_name: Name of the scanned image
        :type image_name str
        :param build_number: Build number of weekly scan at Jenkins
        :type build_number int or str
        """

        build_info = self.buildinfo_obj.get_build_info(
            namespace, jenkins_url,
            image_name, build_number)

        # possible values are ["success", "failed", "image_absent"]
        if status == "image_absent":
            body = self.image_absent_email_body()
        else:
            # convert status to boolean
            status = True if status == "success" else False

            # get the repository name (without tag)
            repository = "https://" + build_info.get("REGISTRY_URL") + \
                "/" + image_name.split(":")[0]
            # body should have repository name (without tag)
            body = self.body_of_email(status, repository)

        # format the subject of email
        if status and status != "image_absent":
            subject = self.weekly_success_subj.format(image_name)
        else:
            subject = self.weekly_failure_subj.format(image_name)

        print ("Sending weekly scan email to {}".format(
            build_info.get("NOTIFY_EMAIL")))

        self.sendemail_obj.email(
            build_info.get("SMTP_SERVER"),
            subject, body,
            build_info.get("FROM_ADDRESS"),
            [build_info.get("NOTIFY_EMAIL")])


if __name__ == "__main__":
    notify_object = WeeklyScanNotify()
    status = sys.argv[1].strip()
    namespace = sys.argv[2].strip()
    jenkins_url = sys.argv[3].strip()
    image_name = sys.argv[4].strip()
    build_number = sys.argv[5].strip()

    notify_object.notify(
        status, namespace, jenkins_url,
        image_name, build_number)
