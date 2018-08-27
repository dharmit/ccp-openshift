"""
This file contains are the basic utility functions to be used by the clients.
"""
import json
import base64
import subprocess
import requests
import ast


def request_url(
        request, params=None, verify_ssl=False, auth=None, headers=None
):
    """
    Queries a specified URL and returns data, if any
    :param request: The url to send the request to.
    :type request str
    :param params: Any params that are to be passed on to the request
    :type params dict
    :param verify_ssl: IF False, ssl errors are ignored.
    :type verify_ssl bool
    :param auth: This will be passed along to requests as is. Note: Passing
    auth overrides any Authorization headers passed already.
    :type auth dict
    :param headers: Any extra headers that you wish to pass along.
    :type headers dict
    :raises Exception
    :return: The response object, or None upon failure, if any or None
    """

    try:
        response = requests.get(
            request, params=params, verify=verify_ssl, headers=headers,
            auth=auth
        )
    except Exception as ex:
        response = None
        raise ex

    return response


def encode(data):
    """
    Applyies base64 encoding to passed string
    :param data: The string to encode
    :type data str
    :return: Encoded string.
    """
    return base64.b64encode(data)


def decode(data):
    """
    Decodes a base64 encoded string.
    :param data: The encoded string to decode
    :return: The decoded string
    """
    return base64.b64decode(data)


def run_cmd(cmd, shell=False, use_pipes=False):
    """
    Runs the command that is passed to it via subprocess.Popen
    :param cmd: The command that needs to be executed
    :type cmd str or list
    :param shell: Default False, not recommended but for cases when needed
    :type shell bool
    :param use_pipes: Default False. If true, uses pipes to store the output
    instead of printing on screen.
    :type use_pipes bool
    :raises Exception
    :return: Returns  a tuple containing output and error.
    """
    try:
        p = subprocess.Popen(
            cmd, shell=shell, stdout=subprocess.PIPE, stderr=subprocess.PIPE
        ) if use_pipes else subprocess.Popen(cmd, shell=shell)
        p.wait()
        out = p.communicate()
    except Exception as ex:
        raise ex
    return out


def json_to_python(data):
    """
    Parses the json and loads the data
    :param data:
    :raises Exception
    :return:
    """
    p = None
    try:
        json.loads(data)
    except Exception as ex:
        raise ex
    return p


def parse_literals(data):
    """
    Parses literal, use to parse of string contains
    quotes.
    """
    p = None
    try:
        p = ast.literal_eval(data)
    except Exception as ex:
        raise ex
    return p

