import pandas as pd

class PhilDataGetter():
    """Class to extract data for the Philippines.

    Attributes:
        - data (pd.DataFrame) : the dataframe containing all the data for PHL.
    
    Methods:
        - get_region_data() : method to get data for regions
        - get_market_data() : method to get data for markets
    """

    def __init__(self, fpi_csv_path:str, er_csv_path:str) -> None:
        """Constructor of class.
        
        Parameters:
            - fpi_csv_path (str) : the path to the csv file containing all the price index data 
            for the several regions, markets, and products found in the Philippines.
            - er_csv_path (str) : the path to the csv file containing all the exchange rate data 
            for the several regions and markets found in the Philippines.
            
        Returns
            - None
        """

        self.fpi_data = pd.read_csv(fpi_csv_path)
        self.er_data = pd.read_csv(er_csv_path)


    def get_region_data(self, data_type:str, target_regions:str, target_markets:str|list[str], target_products:str|list[str]=None,
                        write_to_csv:bool=False, path_to_file:str='./Data/region_data.csv') -> pd.DataFrame|None:
        """Grab data for local markets for the specified products (under specified regions) that are 
        available in those regions' markets.
        
        Parameters: 
            - data_type (str) : the type of data to get from the provided csv files. It can be 'er' 
                                for exchange rate data OR 'fpi' for food price index data.
            - target_regions (str or list): regions to extract data for.
            - target_markets (str or list) : a string or list of strings specifying the market or 
                                             markets to extract data for.
            - target_products (str or list) : a string or list of strings specifying the product
                                              or products to get data for, under the specified 
                                              market(s) and region(s). Defaulted to None.
            - write_to_csv (bool) : whether to write the created dataframe to a csv file. Defaulted to 
                                   False.
            - path_to_file (str) : a string denoting the path to use to write and store the create 
                                  dataframe. Defaulted to './Data/region_data.csv'.
        
        Returns:
            - pd.DataFrame : the dataframe containing the region(s), market(s) and product(s) 
                             price index data
                             index by DateTimeIndex.
        """

        if (data_type.lower() != 'er') and (data_type.lower() != 'fpi'):
            raise ValueError("Data type to extract must be either 'fpi' for food price indices OR 'er' for exchange rates.")

        if data_type == 'er':
            
            if isinstance(target_markets, str):
                target_markets = [target_markets]
            if isinstance(target_regions, str):
                target_regions = [target_regions]
            num_regions = len(target_regions)
            num_markets = len(target_markets)

            df = self.er_data[self.er_data['Market'].isin(target_markets) & (self.er_data['Region'].isin(target_regions))]
            df.index = pd.to_datetime(df['Date'])
            df = df.asfreq('MS')
            df = df.drop(labels=['Date'], axis=1)

            if num_markets == 1:
                df = df.drop(labels=['Market'], axis=1)

        else:

            if isinstance(target_regions, str):
                target_regions = [target_regions]
            if isinstance(target_markets, str):
                target_markets = [target_markets]
            if isinstance(target_products, str):
                target_products = [target_products]

            num_regions = len(target_regions)
            num_markets = len(target_markets)
            num_products = len(target_products)

            df = self.dpi_data[((self.fpi_data['Region'].isint(target_regions)) & (self.fpi_data['Market']).isin(target_markets)) & ((self.fpi_data['Product']).isin(target_products))]
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

        if write_to_csv:
            print(f'Exporting merged dataframe to path: {path_to_file}')
            df.to_csv(path_to_file, date_format='%Y-%m-%d', index=True, index_label='Date')

        return df

    def get_market_data(self, data_type:str, target_markets:str|list[str], target_products:str|list[str]=None,
                        write_to_csv:bool=False, path_to_file:str="./Data/market_data.csv") -> pd.DataFrame:
        """Grab data for local markets for the specified products that are available in those markets.
        
        Parameters: 
            - data_type (str) : the type of data to get from the provided csv files. It can be 'er' 
                                for exchange rate data OR 'fpi' for food price index data.
            - target_markets (str or list) : a string or list of strings specifying the market or 
                                             markets to extract data for.
            - target_products (str or list) : a string or list of strings specifying the product
                                              or products to get data for, under the specified 
                                              market(s). Defaulted to None.
            - write_to_csv (bool) : whether to write the created dataframe to a csv file. Defaulted to 
                                   False.
            - path_to_file (str) : a string denoting the path to use to write and store the create 
                                  dataframe. Defaulted to './Data/market_data.csv'.
        
        Returns:
            - pd.DataFrame : the dataframe containing the market(s) and product(s) price index data
                             index by DateTimeIndex.
        """


        if (data_type.lower() != 'er') and (data_type.lower() != 'fpi'):
            raise ValueError("Data type to extract must be either 'fpi' for food price indices OR 'er' for exchange rates.")

        if data_type == 'er':

            if isinstance(target_markets, str):
                target_markets = [target_markets]
            num_markets = len(target_markets)

            df = self.er_data[self.er_data['Market'].isin(target_markets)]
            df.index = pd.to_datetime(df['Date'])
            df = df.asfreq('MS')
            df = df.drop(labels=['Region', 'Date'], axis=1)

            if num_markets == 1:
                df = df.drop(labels=['Market'], axis=1)

        else:

            if isinstance(target_markets, str):
                target_markets = [target_markets]

            if target_products is None:
                raise ValueError("For fpi, target_products must be specified")
            else:
                if isinstance(target_products, str):
                    target_products = [target_products]

            num_markets = len(target_markets)
            num_products = len(target_products)
            df = self.fpi_data[((self.fpi_data['Market']).isin(target_markets)) & ((self.fpi_data['Product']).isin(target_products))]
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

        if write_to_csv:
            print(f'Exporting merged dataframe to path: {path_to_file}')
            df.to_csv(path_to_file, date_format='%Y-%m-%d', index=True, index_label='Date')

        return df
    
def merger(dfs:list[pd.DataFrame], date_range:tuple[str, str]=('2007-01-01', '2022-12-01'), along_axis:int=1,
           cols_to_drop:dict[int:list[str]|None]=None, cols_to_rename:dict[int:dict[str:str]|None]=None, 
           write_to_csv:bool=False, path_to_file:str='./Data/PHL_data.csv') -> pd.DataFrame:
    """Merge any given time series data (in pd.DataFrame)  along a given date range into one dataframe
    whose time series frequency is 'MS' (i.e. month start).
    
    Parameters:
        - dfs (list) : the dataframes to merge.
        - date_range (tuple) : a tuple comprised of two strings where the first denotes the starting date and 
                        the last the ending date with which to index the merged dataframe with. Defaulted to 
                        ('2007-01-01', '2022-12-01').
        - along_axis (int) : an int denoting the axis on which to merge the given dfs. Defaulted to 1 for column
                             wise merging. NOTE that in order for merging to take place along axis 0, each df in
                             dfs must have the same column names; else, merging will be along axis 1 and columns
                             may contain NaNs.
        - cols_to_drop (dict or None) : a dictionary comprising of integer keys and lists of string 
                                        elements (or None) as the values, where key k denotes dfs[k] 
                                        and the value is a list of labels of the columns that must be dropped 
                                        from dfs[k] along axis 1. If the value of dfs[k] is None, no columns
                                        are dropped. This parameter is defaulted to None which denotes no 
                                        columns are dropped from any of the datasets.
        - cols_to_rename (dict or None) : a dictionary comprising of integer keys and dictionaries as keys (or None).
                                          Key k denotes dfs[k] and the value contains a dict whose keys are the string
                                          names of the columns that needs to be renamed and the values are the new names
                                          of those columns. If the value of dfs[k] is None, no columns are renamed.
                                          This parameter is defaulted to None.
        - write_to_csv (bool) : whether to write the created merged dataframe to a csv file. Defaulted to False.
        - path_to_file (str) : a string denoting the path to use to write and store the merged dataframe. Defaulted
                               to './Data/PHL_data.csv'.

    Returns:
        - (pd.DataFrame) : a dataframe merging all the given dfs.
    """

    time_freq = 'MS'                                                                 # Monthly Start
    dates = pd.date_range(start=date_range[0], end=date_range[1], freq=time_freq)
    dataframes = []

    if cols_to_drop is None:
        cols_to_drop = {j:None for j in range(len(dfs))}

    if cols_to_rename is None:
        cols_to_rename = {j:None for j in range(len(dfs))}

    for i, df in enumerate(dfs):

        if not isinstance(df.index, pd.DatetimeIndex):
            df.index = pd.to_datetime(df.index)

        data_freq = df.index.freq

        if cols_to_drop[i] is not None:
            df = df.drop(labels=cols_to_drop[i], axis=1)
        
        if cols_to_rename[i] is not None:
            df = df.rename(cols_to_rename[i], axis=1)

        if data_freq != time_freq:

            if data_freq is None:
                freq = input(f"Enter the frequency of dataframe {i+1}")
                df = df.asfreq(freq)

            # Average out Daily to Monthly
            if data_freq == 'D':
                df = df.resample(time_freq).mean()

            # Linearly interpolate yearly data to make monthly
            elif data_freq == 'YS':
                df = (df.resample(time_freq)).interpolate('linear')

        if along_axis == 1:
            df = df.reindex(dates)
        dataframes += [df]

    merged = pd.concat(dataframes, axis=along_axis)

    if write_to_csv:
        print(f'Exporting merged dataframe to path: {path_to_file}')
        merged.to_csv(path_to_file, date_format='%Y-%m-%d', index=True, index_label='Date')
    
    return merged
