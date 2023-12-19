# encoding: utf-8
import logging

import pandas as pd

import functions
from graph_fn import plot_temperature_graph

# ============= Logging setup ===========
logging.basicConfig(filename='app.log', filemode='a', format='%(asctime)s - %(levelname)s - %(message)s', level=logging.INFO)
log_file_path = "experiment.edf"  # Replace with the actual file path

print("  SENSIRION HUMIGADGET HELPER\n==============================\n")
df = functions.read_logfile(log_file_path)
earliest_datestamp = functions.get_earliest_datestamp(df)
print("Earliest Datestamp: ", earliest_datestamp)
latest_datestamp = functions.get_latest_datestamp(df)
print("Latest Datestamp:   ", latest_datestamp)
timespan = functions.calculate_timespan(df)
print("\nTimespan between Earliest and Latest Datestamps:", timespan)

measurement_interval = functions.calculate_measurement_interval(df)
# print("Average Measurement Interval:", measurement_interval)
estimated_meas_interval = functions.round_measurement_interval(measurement_interval)
print("Estimated Measurement interval: ", estimated_meas_interval)
#df_with_time_diffs = functions.add_time_diffs_column(df)



gap_indices = functions.find_time_gaps(df, max_time_diff=estimated_meas_interval)
# print("1st Indices with time gaps greater than 1 minute:", gap_indices)
df_filled_gaps = functions.fill_time_gaps(df, gap_indices)
#print(df_filled_gaps)
measurement_interval = functions.calculate_measurement_interval(df_filled_gaps)
# print("Average Measurement Interval after filling gaps:", measurement_interval)

export_result = functions.export_dataframe_to_file(df_filled_gaps)

user_datetime = functions.get_user_datetime_input()
user_timespan = functions.get_user_timespan_input()

# print(type(user_datetime), type(user_timespan))

# print(df_filled_gaps)
startife = functions.find_closest_index(df_filled_gaps, user_datetime) # Start Index for Extract
# print("Closest index to given datestamp: ",functions.find_closest_index(df_filled_gaps, user_datetime))
lastife = functions.find_index_after_timespan(df_filled_gaps, functions.find_closest_index(df_filled_gaps, user_datetime), user_timespan) # Last index for Extract
# print("Closing index: ",functions.find_index_after_timespan(df_filled_gaps, functions.find_closest_index(df_filled_gaps, user_datetime), user_timespan))

# print(startife, lastife)
List_of_datestamps, List_of_T, List_of_RH = functions.extract_data_between_indices(df_filled_gaps,startife, lastife)

# print(List_of_datestamps)
# print(List_of_T)
# print(List_of_RH)

plot_temperature_graph(List_of_datestamps, List_of_T, "First graph")