import sys
import pandas as pd
from pytz import timezone

# create a dataframe from the log file
info_df = pd.read_csv('capture.log', delimiter=';', names= ["Product", "Price", "Date Time"],
                        dtype={'Price': 'int', 'Product': 'str'},
                        parse_dates=['Date Time'], 
                        date_parser=lambda x: pd.to_datetime(x,format=' %Y-%m-%d %H:%M:%S,%f')
                    )

# price change calculation
if len(info_df) > 1:
    price_diff = info_df['Price'].diff().iloc[-1]
    price_change = -1 * int(info_df['Price'].diff().iloc[-1]/info_df['Price'].iloc[-1] * 100)

    output_string = f"{price_diff},{price_change}"
    sys.exit(0)
else:
    output_string = f"{None},{None}"