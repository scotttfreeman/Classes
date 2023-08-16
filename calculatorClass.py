import pandas as pd
import numpy as np
from fredapi import Fred
fred = Fred(api_key='your api key') # enter your own Fred API key

class Calculator(object):

    def get_fred_data(self, indicators, frequency='m', aggregation_method='eop'):
        '''
        returns FRED data series in data frame format based on list of Fred indicators
        '''
        dfs = []

        freq_mapping = {
            'm': 'M',  # Monthly
            'q': 'Q',  # Quarterly
            'a': 'A'   # Annual
        }

        for indicator in indicators:
            data = fred.get_series(indicator, frequency=frequency, aggregation_method=aggregation_method)
            data.name = indicators[indicator]

            # Ensure data is formatted to end of period
            data = data.resample(freq_mapping[frequency]).last()

            # Filter out zero values
            data = data[data != 0]

            dfs.append(data)

        df_fred = pd.concat(dfs, axis=1)

        return df_fred
        
    def filter_by_date(self, df, start_date, end_date):
        '''
        creates a dataframe of values for a specific date range
        '''
        return df[(df.index >= start_date) & (df.index <= end_date)]
    
    def annualized_change(self, df, frequency, *periods):
        '''
        calculates annualized change of each variable in a data frame.
        you can dynamically calculate multiple annualized periods, for example, 3month, 6month, 18month, etc.
        '''
        freq_to_periods = {
            'd': 252,  # Daily
            'w': 52,   # Weekly
            'm': 12,   # Monthly
            'q': 4,    # Quarterly
            'y': 1     # Yearly
        }
        
        if frequency not in freq_to_periods:
            raise ValueError(f"Unsupported frequency '{frequency}'. Supported frequencies are: {', '.join(freq_to_periods.keys())}")

        annual_periods = freq_to_periods[frequency]
        results = pd.DataFrame()

        for period in periods:
            annualized_rate = ((df / df.shift(period)) ** (annual_periods / period) - 1).add_suffix(f' {period}{frequency} ann % chg')
            results = pd.concat([results, annualized_rate], axis=1)

        return results

    def indexed_perf_around_specific_dates(self, df, target_dates, months):
        '''
        will take each value from your df and index that value to 100 at each date in your target_dates list. then, it will calculate the indexed
        values for each variable a specific amount of months leading up to and following each target date
        '''
        indexed_dfs = []

        for date in target_dates:
            # Handle anchor values for all columns at the given date
            anchor_values = df.loc[date]

            # Determine the start and end dates based on the given range
            start_date = max(date - pd.DateOffset(months=months), df.index.min())
            end_date = min(date + pd.DateOffset(months=months), df.index.max())

            # Subset the dataframe to the relevant period
            period_data = df.loc[start_date:end_date].copy()

            # Normalize each column in the period data by its respective anchor value and multiply by 100
            for col in period_data.columns:
                period_data[col] = period_data[col] / anchor_values[col] * 100
                # Rename the columns to add the target date to the column name
                period_data.rename(columns={col: col + "_" + str(date.date())}, inplace=True)

            # Replace the date-based index with a range index based on the length of the period_data
            range_start = -months
            range_end = range_start + len(period_data)
            period_data.index = range(range_start, range_end)

            indexed_dfs.append(period_data)

        # Concatenate the list of dataframes along the columns axis
        indexed_df = pd.concat(indexed_dfs, axis=1)

        return indexed_df
    
    def avg_indexed_perf_around_specific_dates(self, df, target_dates, months):
        indexed_df = self.indexed_perf_around_specific_dates(df, target_dates, months)
        
        # calculate the average indexed performance for each month relative to the target date
        avg_indexed_by_month = indexed_df.groupby(indexed_df.index).mean()
        
        # split the column names to separate the variable name from the target date
        avg_indexed_by_month.columns = avg_indexed_by_month.columns.str.split('_').str[0]
        
        # calculate the mean of the columns with the same variable name
        avg_indexed_df = avg_indexed_by_month.groupby(avg_indexed_by_month.columns, axis=1).mean()

        return avg_indexed_df
