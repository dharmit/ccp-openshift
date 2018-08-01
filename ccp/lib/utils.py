"""
This file contains utility functions to be used by all of the pipeline.
"""

import subprocess
import yaml


def run_cmd(cmd, shell=False):
    """
    Runs the given shell command

    :param cmd: Command to run
    :param shell: Whether to run raw shell commands with '|' and redirections
    :type cmd: str
    :type shell: boolean

    :return: Command output
    :rtype: str
    :raises: subprocess.CalledProcessError
    """
    if shell:
        return subprocess.check_output(cmd, shell=True)
    else:
        return subprocess.check_output(cmd.split(), shell=False)


def load_yaml(file_path, base_loader=True, raise_execption=False):
    """
    Loads data from specified yaml file.
    :param file_path: The path of the yaml file from where to load data.
    :param base_loader: If true, yaml.BaseLoader is used to load data.
    :param raise_execption: If true, then exception is raised on failure
    :return: The data, if the read was successfull, else None
    """
    data = None
    try:
        with open(file_path) as f:
            if base_loader:
                data = yaml.load(f, Loader=yaml.BaseLoader)
            else:
                data = yaml.load(f)
    except yaml.YAMLError as exc:
        print ("Failed to read {}".format(file_path))
        if raise_execption:
            raise exc
    return data


def dump_yaml(file_path, data, base_dumper=True, raise_exception=False):
    try:
        with open(file_path, "w") as f:
            if base_dumper:
                yaml.dump(data, f, Dumper=yaml.BaseDumper)
            else:
                yaml.dump(data, f)
    except yaml.YAMLError as exc:
        print ("Failed to write to {}".format(file_path))
        if raise_exception:
            raise exc


def replace_dot_slash_colon_(value):
    """
    Given a value with either dot slash or underscore,
    replace each with hyphen
    :param value: The string in which the replacing is needed
    """
    return value.replace("_", "-").replace("/", "-").replace(
        ".", "-").replace(":", "-")
