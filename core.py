import os
import requests

class config:
    """
    Centralized configuration and utility methods.
    """
    API_URL = "https://www.traderjoes.com/api/graphql"
    QUERIES_DIR = os.path.join("H:\\", "repos", "traderjoes3", "src", "api", "queries")
    STORE_ID = "138"
    PAGE_SIZE = 25
    CURRENT_PAGE = 1

    @staticmethod
    def get_path(filename):
        """
        Get the full path to a file in the queries directory.

        Args:
            filename (str): The name of the file.

        Returns:
            str: The full path to the file.
        """
        return os.path.join(config.QUERIES_DIR, filename)


class query:
    """
    Handles loading GraphQL queries from files.
    """
    @staticmethod
    def load_query(file_path):
        """
        Load a GraphQL query from a file.

        Args:
            file_path (str): The path to the query file.

        Returns:
            str: The contents of the query file.
        """
        with open(file_path, "r") as file:
            return file.read()


class api_com:
    """
    Handles API communication with Trader Joe's GraphQL endpoint.
    """
    @staticmethod
    def fetch_data(query, variables=None):
        """
        Make a GraphQL API request.

        Args:
            query (str): The GraphQL query string.
            variables (dict): Variables for the query.

        Returns:
            dict: The API response.
        """
        if variables is None:
            variables = {
                "pageSize": config.PAGE_SIZE,
                "currentPage": config.CURRENT_PAGE,
                "storeCode": config.STORE_ID
            }
        headers = {"Content-Type": "application/json"}
        payload = {"query": query, "variables": variables}
        response = requests.post(config.API_URL, json=payload, headers=headers)
        response.raise_for_status()
        return response.json()
