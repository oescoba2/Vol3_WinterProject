import pandas as pd

class PhilDataGetter():
    """Class to extract region, market, and product data for the Philippines.

    Attributes:
        - data (pd.DataFrame) : the dataframe containing all the data for PHL.
    
    Methods:
        - get_region_data() : method to get data for regions
        - get_market_data() : method to get data for markets
    """

    def __init__(self, market_csv_path:str) -> None:
        """Constructor of class.
        
        Parameters:
            - market_csv_path (str) : the path to the csv file containing all the price index data 
            for the several regions, markets, and products found in the Philippines.
            
        Returns
            - None
        """

        self.data = pd.read_csv(market_csv_path)

    def get_region_data(self, target_regions:str, target_markets:str|list[str], target_products:str|list[str],
                        write_to_csv:bool=False, path_to_file:str='./Data/region_data.csv') -> pd.DataFrame:
        """Grab data for local markets for the specified products (under specified regions) that are 
        available in those regions' markets.
        
        Parameters: 
            - target_regions (str or list): 
            - target_markets (str or list) : a string or list of strings specifying the market or 
                                             markets from which to extract product information.
            - target_products (str or list) : a string or list of strings specifying the product
                                              or products to get data for, under the specified 
                                              market(s).
            - write_to_csv (bool) : whether to write the created dataframe to a csv file. Defaulted to 
                                   False.
            - path_to_file (str) : a string denoting the path to use to write and store the create 
                                  dataframe. Defaulted to './Data/region_data.csv'.
        
        Returns:
            - pd.DataFrame : the dataframe containing the region(s), market(s) and product(s) 
                             price index data
                             index by DateTimeIndex.
        """

        if isinstance(target_regions, str):
            target_regions = [target_regions]
        if isinstance(target_markets, str):
            target_markets = [target_markets]
        if isinstance(target_products, str):
            target_products = [target_products]

        num_regions = len(target_regions)
        num_markets = len(target_markets)
        num_products = len(target_products)

        df = self.data[((self.data['Region'].isint(target_regions)) & (self.data['Market']).isin(target_markets)) & ((self.data['Product']).isin(target_products))]
        df.index = pd.to_datetime(df['Date'])
        df = df.asfreq('MS')

        if (num_regions == 1) and (num_markets == 1) and (num_products == 1):
            df = df.drop(labels=['Date', 'Product', 'Region', 'Market'], axis=1)

        elif (num_regions == 1) and (num_markets == 1) and (num_products != 1):
            df = df.drop(labels=['Date', 'Region', 'Market'], axis=1)

        elif (num_regions == 1) and (num_markets != 1) and (num_products == 1):
            df = df.drop(labels=['Date', 'Region', 'Product'], axis=1)   

        elif (num_regions != 1) and (num_markets == 1) and (num_products == 1):
            df = df.drop(labels=['Date', 'Market', 'Product'], axis=1)   

        elif (num_regions == 1) and (num_markets != 1) and (num_products != 1):
            df = df.drop(labels=['Date', 'Region'], axis=1)

        elif (num_regions != 1) and (num_markets != 1) and (num_products == 1):
            df = df.drop(labels=['Date', 'Product'], axis=1)

        elif (num_regions != 1) and (num_markets == 1) and (num_products != 1):
            df = df.drop(labels=['Date', 'Market'], axis=1)

        elif (num_regions != 1) and (num_markets != 1) and (num_products != 1):
            df = df.drop(labels=['Date'], axis=1)  

        return df

    def get_market_data(self, target_markets:str|list[str], target_products:str|list[str],
                        write_to_csv:bool=False, path_to_file:str="./Data/market_data.csv") -> pd.DataFrame:
        """Grab data for local markets for the specified products that are available in those markets.
        
        Parameters: 
            - target_markets (str or list) : a string or list of strings specifying the market or 
                                             markets from which to extract product information.
            - target_products (str or list) : a string or list of strings specifying the product
                                              or products to get data for, under the specified 
                                              market(s).
            - write_to_csv (bool) : whether to write the created dataframe to a csv file. Defaulted to 
                                   False.
            - path_to_file (str) : a string denoting the path to use to write and store the create 
                                  dataframe. Defaulted to './Data/market_data.csv'.
        
        Returns:
            - pd.DataFrame : the dataframe containing the market(s) and product(s) price index data
                             index by DateTimeIndex.
        """

        if isinstance(target_markets, str):
            target_markets = [target_markets]
        if isinstance(target_products, str):
            target_products = [target_products]

        num_markets = len(target_markets)
        num_products = len(target_products)
        df = self.data[((self.data['Market']).isin(target_markets)) & ((self.data['Product']).isin(target_products))]
        df.index = pd.to_datetime(df['Date'])
        df = df.asfreq('MS')

        # One product for one market
        if (num_markets == 1) and (num_products == 1):
            df = df.drop(labels=['Date', 'Product', 'Region', 'Market'], axis=1)

        # Several products for one market
        elif (num_markets == 1) and (num_products != 1):
            df = df.drop(labels=['Date', 'Region', 'Market'], axis=1)

        elif (num_markets != 1) and (num_products != 1):
            df = df.drop(labels=['Date', 'Region'], axis=1)

        return df
    
def merger(dataframes:list[pd.DataFrame], cols_to_drop:dict[int:list[str]|None]=None, 
           date_range:tuple[str, str]=('2007-01-01', '2022-12-01'), 
            write_to_csv:bool=False, path_to_file:str='./Data/PHL_data.csv') -> pd.DataFrame:
    """Merge any given time series data (in pd.DataFrame)  along a given date range into one dataframe
    whose time series frequency is 'MS' (i.e. month start).
    
    Parameters:
        - dataframes (list) : the dataframes to merge.
        - cols_to_drop (dict or None) : a dictionary comprising of integer keys and lists of string 
                                        elements (or None) as the values, where key k denotes data_path[k] 
                                        and the value is a list of labels of the columns that must be dropped 
                                        from data_path[k] along axis 1. If the value of data_path[k] is None, 
                                        no columns are dropped. This parameter is defaulted to None which 
                                        denotes no columns are dropped from any of the datasets.
        - date_range (tuple) : a tuple comprised of two strings where the first denotes the starting date and 
                               the last the ending date with which to index the merged dataframe with. Defaulted to 
                               ('2007-01-01', '2022-12-01').
        - write_to_csv (bool) : whether to write the created merged dataframe to a csv file. Defaulted to False.
        - path_to_file (str) : a string denoting the path to use to write and store the merged dataframe. Defaulted
                               to './Data/PHL_data.csv'.

    Returns:
        - (pd.DataFrame) : a dataframe containing merging all the specified data_paths.
    """

    time_freq = 'MS'                                                                 # Monthly Start
    dates = pd.date_range(start=date_range[0], end=date_range[1], freq=time_freq)
    dfs = []

    if cols_to_drop is None:
        cols_to_drop = {j:None for j in range(len(dataframes))}

    for i, df in enumerate(dataframes):

        df.index = pd.to_datetime(df.index)
        data_freq = df.index.freq

        if cols_to_drop[i] is not None:
            df = df.drop(labels=cols_to_drop[i], axis=1)

        if data_freq != time_freq:

            # Average out Daily to Monthly
            if data_freq == 'D':
                df = df.resample(time_freq).mean()

            # Linearly interpolate yearly data to make monthly
            elif data_freq == 'YS':
                df = (df.resample(time_freq)).interpolate('linear')

        df = df.reindex(dates)
        dfs += [df]

    merged = pd.concat(dfs, axis=1)

    if write_to_csv:
        print(f'Exporting merged dataframe to path: {path_to_file}')
        merged.to_csv(path_to_file, date_format='%Y-%m-%d', index=True, index_label='Date')
    
    return merged
