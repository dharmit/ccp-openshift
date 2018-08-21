"""
This file contains base classes of query processor.
"""

from ccp.lib.utils import json_to_python


class QueryProcessor(object):
    """
    Acts as base of all Query Processor
    """
    pass


class JSONQueryProcessor(QueryProcessor):
    """
    Acts as base of JSONQueryProcessor
    """

    def get_data_from_response(self, response):
        """
        Extracts json data from a requests response object
        :param response: The response from which we need to extract information
        :type response requests.response
        :return: response result as json, if it can get it, Else None
        """
        data = None
        if response:
            data = json_to_python(response.text)
        return data
