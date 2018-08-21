"""
This file contains are the basic utility functions to be used by the clients.
"""
import json
import base64
import subprocess
import requests


def request_url(
        request, params=None, verify_ssl=False, auth=None, headers=None
):
    """
    Queries a specified url and returns data, if any
    :param request: The url to send the request to.
    :type request str
    :param params: Any params that are to be passed on to the request
    :param verify_ssl: IF true, ssl errors are ignored
    :type verify_ssl bool
    :param auth: This will be passed along to requests as is.
    :type auth dict
    :param headers: Any extra headers that you wish to pass along.
    :type headers dict
    :return: The response object, or None upon failure, alongwith exception
    message, if any or None
    """
    exception = None

    try:
        response = requests.get(
            request, params=params, verify=verify_ssl, headers=headers,
            auth=auth
        )
    except Exception as ex:
        response = None
        exception = ex

    return response, exception


def encode(data):
    return base64.b64encode(data)


def decode(data):
    return base64.b64decode(data)


def run_cmd(cmd, shell=False, use_pipes=True):
    """
    Runs the command that is passed to it via subprocess.Popen
    :param cmd: The command that needs to be executed
    :param shell: Default False, not recommended but for cases when needed
    :param use_pipes: Default true. If true, uses pipes to store the output
    instead of printing on screen.
    :return: Returns 2 objects, the first a tuple containing output and error
    message of executed command, if use_pipes=True, and the second which is
    exception object if any was raised during command execution.
    """
    out = None
    exception = None
    try:
        p = subprocess.Popen(
            cmd, shell=shell, stdout=subprocess.PIPE, stderr=subprocess.PIPE
        ) if use_pipes else subprocess.Popen(cmd, shell=shell)
        out = p.communicate()
    except Exception as ex:
        exception = ex
    return out, exception


def json_to_python(data):
    """
    Parses the json and loads the data
    :param data:
    :return:
    """
    p = None
    try:
        json.loads(data)
    except Exception:
        pass
    return p
