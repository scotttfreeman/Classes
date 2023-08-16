import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

class Plotting(object):

    def filter_by_date(self, df, start_date, end_date):
        '''
        creates a dataframe of values for a specific date range
        '''
        return df[(df.index >= start_date) & (df.index <= end_date)]
    
    def create_mapped_index(self, df1, df2, frequency='M'):
        '''
        align indexes of two data series over different time periods
        '''
        return pd.date_range(df1.index[0], periods=len(df2), freq=frequency)
    
    def index_to_100(self, df):
        '''
        index a data series to 100, starting at its first value
        '''
        return (df / df.iloc[0]) * 100
    
    def plot_two_date_ranges(self, df, date_range1, date_range2, index_to_100=False):
        '''
        plot two data series from two different time periods.
        e.g., data from Jan 1967 to Jan 1980 and Mar 2020 to July 2023

        set index_to_100 = True if you want to plot indexed data for the specific time periods
        '''
        
        # Loop through every column in the dataframe
        for column in df.columns:
            # Filter the dataframe for the two date ranges
            filtered_df1 = self.filter_by_date(df[[column]], *date_range1)
            filtered_df2 = self.filter_by_date(df[[column]], *date_range2)
            
            if index_to_100:
                indexed_df1 = self.index_to_100(filtered_df1)
                indexed_df2 = self.index_to_100(filtered_df2)
                
                # Create a new index for indexed_df2 to match the length of indexed_df1
                new_index = self.create_mapped_index(indexed_df1, indexed_df2)
                
                # Replace the index of indexed_df2 with the new index
                indexed_df2.index = new_index

                plot_df1 = indexed_df1
                plot_df2 = indexed_df2

            else:
                new_index = self.create_mapped_index(filtered_df1, filtered_df2)
                filtered_df2.index = new_index

                plot_df1 = filtered_df1
                plot_df2 = filtered_df2

            # Plotting
            plt.figure(figsize=(10, 6))
            
            # Plot data for the first date range
            plt.plot(plot_df1.index, plot_df1[column], label=f"{column}: {date_range1[0]} to {date_range1[1]}", color='blue')
            
            # Plot data for the second date range with the mapped index
            plt.plot(new_index, plot_df2[column], label=f"{column}: {date_range2[0]} to {date_range2[1]}", color='red', linestyle='--')
            
            # plt.title(f"{column} Data Comparison")
            # plt.ylabel(column)
            plt.legend()
            plt.grid(True)
            plt.tight_layout()
            plt.show()

    def plot_annualized_changes(self, df_annual_changes):
        '''
        Plots each annualized change as a line on a subplot for each variable.
        df_annual_changes is the output of the annualized_change method.
        '''
        # Extract unique variable names from column names
        unique_vars = set([col.split(' ')[0] for col in df_annual_changes.columns])
        
        fig, axes = plt.subplots(nrows=len(unique_vars), figsize=(10, 6 * len(unique_vars)))
        
        # If there's only one variable, axes is not an array, so we make it one for consistent handling
        if len(unique_vars) == 1:
            axes = [axes]

        for i, var in enumerate(unique_vars):
            # Columns related to this specific variable
            relevant_cols = [col for col in df_annual_changes.columns if col.startswith(var)]
            
            for col in relevant_cols:
                # Plot the data on the specific subplot
                axes[i].plot(df_annual_changes.index, df_annual_changes[col], label=col[0:])
            
            # axes[i].set_title(f"Annualized Changes for {var}")
            axes[i].legend(loc='best')
            axes[i].grid(True)
            axes[i].yaxis.set_major_formatter(plt.FuncFormatter(lambda y, _: '{:.0%}'.format(y)))
            
        plt.tight_layout()
        plt.show()
