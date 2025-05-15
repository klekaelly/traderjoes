import pandas as pd

class DataFrameHandler:
    @staticmethod
    def flatten_dict(d, parent_key='', sep='.'):
        """
        Flattens a nested dictionary into a single-level dictionary.

        Args:
            d (dict): The dictionary to flatten.
            parent_key (str): The base key string for recursion.
            sep (str): Separator for nested keys.

        Returns:
            dict: A flattened dictionary.
        """
        def process_dict(value, key):
            return DataFrameHandler.flatten_dict(value, key, sep=sep).items()

        def process_list(value, key):
            items = []
            if all(isinstance(i, str) for i in value):
                for i, val in enumerate(value):
                    items.append((f"{key}[{i + 1}]", val))
            else:
                for i, item in enumerate(value):
                    items.extend(DataFrameHandler.flatten_dict(item, f"{key}[{i}]", sep=sep).items())
            return items

        items = []
        for k, v in d.items():
            new_key = f"{parent_key}{sep}{k}" if parent_key else k
            if isinstance(v, dict):
                items.extend(process_dict(v, new_key))
            elif isinstance(v, list):
                items.extend(process_list(v, new_key))
            else:
                items.append((new_key, v))
        return dict(items)

    @staticmethod
    def response_to_dataframe(response, top_level_key=None):
        """
        Converts the API response into a DataFrame.

        Args:
            response (dict): The API response.
            top_level_key (str): The top-level key in the response containing the data.

        Returns:
            pd.DataFrame: The resulting DataFrame.
        """
        if 'errors' in response:
            print("GraphQL Errors:", response['errors'])
            return pd.DataFrame()
        data = response.get('data', {})
        if not data:
            print("No data available in the response.")
            return pd.DataFrame()
        if not top_level_key:
            top_level_key = next(iter(data), None)
        if not top_level_key:
            print("No top-level key found in the response.")
            return pd.DataFrame()
        items = data[top_level_key].get('items', [])
        if not isinstance(items, list):
            print("Expected a list of items but got something else.")
            return pd.DataFrame()
        flattened_items = [DataFrameHandler.flatten_dict(item) for item in items]
        return pd.DataFrame(flattened_items)

    @staticmethod
    def post_process_dataframe(df):
        if 'popularity' in df.columns:
            df['Rank'] = df['popularity'].astype(float).rank(method='min', ascending=False).astype(int)
            df = df.drop(columns=['popularity'])
            
        return df
