# encoding: utf-8
import logging

import pandas as pd

import functions

# ============= Logging setup ===========
logging.basicConfig(filename='app.log', filemode='a', format='%(asctime)s - %(levelname)s - %(message)s', level=logging.INFO)

log_file_path = "Sensirion_MyAmbience_Smart_Humigadget_9CEC_2023-01-05T09-26-36.210951.edf"  # Replace with the actual file path



df = functions.read_logfile(log_file_path)
#print(df)
earliest_datestamp = functions.get_earliest_datestamp(df)
print("Earliest Datestamp:", earliest_datestamp)
latest_datestamp = functions.get_latest_datestamp(df)
print("Latest Datestamp:", latest_datestamp)
timespan = functions.calculate_timespan(df)
print("Timespan between Earliest and Latest Datestamps:", timespan)

measurement_interval = functions.calculate_measurement_interval(df)
print("Average Measurement Interval:", measurement_interval)

#df_with_time_diffs = functions.add_time_diffs_column(df)



gap_indices = functions.find_time_gaps(df, max_time_diff=pd.Timedelta(minutes=1))
print("1st Indices with time gaps greater than 1 minute:", gap_indices)
df_filled_gaps = functions.fill_time_gaps(df, gap_indices)
#print(df_filled_gaps)
measurement_interval = functions.calculate_measurement_interval(df_filled_gaps)
print("Average Measurement Interval after filling gaps:", measurement_interval)

export_result = functions.export_dataframe_to_file(df_filled_gaps)
