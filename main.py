# encoding: utf-8
import logging

import pandas as pd

import functions

# ============= Logging setup ===========
logging.basicConfig(filename='app.log', filemode='a', format='%(asctime)s - %(levelname)s - %(message)s', level=logging.INFO)

log_file_path = "experiment.edf"  # Replace with the actual file path



df = functions.read_logfile(log_file_path)
print(df)
earliest_datestamp = functions.get_earliest_datestamp(df)
print("Earliest Datestamp:", earliest_datestamp)
latest_datestamp = functions.get_latest_datestamp(df)
print("Latest Datestamp:", latest_datestamp)
timespan = functions.calculate_timespan(df)
print("Timespan between Earliest and Latest Datestamps:", timespan)

measurement_interval = functions.calculate_measurement_interval(df)
print("Average Measurement Interval:", measurement_interval)

df_with_time_diffs = functions.add_time_diffs_column(df)

export_result = functions.export_dataframe_to_file(df_with_time_diffs)

gap_indices = functions.find_time_gaps(df_with_time_diffs, max_time_diff=pd.Timedelta(minutes=1))
print("1st Indices with time gaps greater than 1 minute:", gap_indices)

df_filled_gaps = functions.fill_time_gaps(df_with_time_diffs, [gap_indices[0]])

# Assuming gap_indices is a Pandas Index object
gap_indices_list = gap_indices.tolist()  # Convert to list
first_element = gap_indices_list.pop(0)  # Pop the first element
gap_indices = pd.Index(gap_indices_list)  # Convert back to Pandas Index

gap_indices = functions.find_time_gaps(df_filled_gaps, max_time_diff=pd.Timedelta(minutes=1))
print("2nd Indices with time gaps greater than 1 minute:", gap_indices)

df_filled_gaps = functions.fill_time_gaps(df_filled_gaps, [gap_indices[0]])


#df_filled_gaps = functions.fill_time_gaps(df_with_time_diffs, gap_indices)
#df_filled_gaps = functions.fill_time_gaps(df_with_time_diffs, [gap_indices[0]])



# Display the DataFrame with filled time gaps
print(df_filled_gaps)
