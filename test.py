import pandas as pd
import numpy as np
from fredapi import Fred
import matplotlib.pyplot as plt
from calculatorClass import Calculator  # Import the Calculator class
from plottingClass import Plotting

# Create an instance of the Calculator class
c = Calculator()
p = Plotting()


# Define the indicators to fetch from FRED
indicators = {
    # 'ICSA': 'Initial Claims',
    # 'PERMIT': 'Building Permits',
    # 'SP500': 'S&P 500'
    'CPIAUCSL': 'CPI',
    'CPILFESL': 'Core CPI'
}

recession_start = pd.to_datetime(['1970-01-31','1973-12-31','1980-02-29','1981-08-31', '1990-08-31', '2001-04-30','2008-01-31'])
date_range1 = ('1966-03-31', '1982-12-31')
date_range2 = ('2013-09-30', '2023-07-31')

df_fred = c.get_fred_data(indicators).dropna()
print(df_fred)

# df_filtered = c.filter_by_date(df_fred, '12/31/2000', '12/31/2010')
# print(df_filtered)

# indexed_data = c.indexed_perf_around_specific_dates(df_fred, recession_start, 18)
# print(indexed_data)

# avg_indexed_data = c.avg_indexed_perf_around_specific_dates(df_fred, recession_start, 18)
# print(avg_indexed_data)

# pct_change = c.annualized_change(df_fred,'m',12)
# print(pct_change)

perf_df = c.annualized_change(df_fred,'m', 1, 3, 12)
print(perf_df)
# p.plot_two_date_ranges(perf_df, date_range1, date_range2)

annual_changes_df = c.annualized_change(df_fred, 'm', 1,3,12)
annual_changes_df = c.filter_by_date(annual_changes_df, '12/31/2018', '7/31/2023')
p.plot_annualized_changes(annual_changes_df)