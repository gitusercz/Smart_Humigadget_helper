from io import StringIO

import pandas as pd


def read_logfile(file_path):
    # Read the entire file content
    with open(file_path, 'r') as file:
        content = file.read()

    # Find the index where the header starts (line number 10 in this case)
    header_start = content.find('Epoch_UTC')

    # Extract the header and data
    header_line = content[header_start:].split('\n')[0]
    data = content[header_start:].split('\n')[1:]

    # Create a DataFrame with the correct column names, excluding the first column (Epoch)
    df = pd.read_csv(StringIO('\n'.join(data)), sep='\t', header=None, names=header_line.split('\t'), usecols=range(1, len(header_line.split('\t'))))

    return df


def get_earliest_datestamp(df):
    # Check if 'Local_Date_Time' column exists
    if 'Local_Date_Time' in df.columns:
        # Convert 'Local_Date_Time' to datetime if it's not already
        if df['Local_Date_Time'].dtype != 'datetime64[ns]':
            df['Local_Date_Time'] = pd.to_datetime(df['Local_Date_Time'])

        # Find the row with the earliest datestamp
        earliest_row = df.loc[df['Local_Date_Time'].idxmin()]

        # Extract and return the earliest datestamp
        earliest_datestamp = earliest_row['Local_Date_Time']
        return earliest_datestamp
    else:
        return "Column 'Local_Date_Time' not found in the DataFrame."

def get_latest_datestamp(df):
    # Check if 'Local_Date_Time' column exists
    if 'Local_Date_Time' in df.columns:
        # Convert 'Local_Date_Time' to datetime if it's not already
        if df['Local_Date_Time'].dtype != 'datetime64[ns]':
            df['Local_Date_Time'] = pd.to_datetime(df['Local_Date_Time'])

        # Find the row with the latest datestamp
        latest_row = df.loc[df['Local_Date_Time'].idxmax()]

        # Extract and return the latest datestamp
        latest_datestamp = latest_row['Local_Date_Time']
        return latest_datestamp
    else:
        return "Column 'Local_Date_Time' not found in the DataFrame."
def calculate_timespan(df):
    # Check if 'Local_Date_Time' column exists
    if 'Local_Date_Time' in df.columns:
        # Convert 'Local_Date_Time' to datetime if it's not already
        if df['Local_Date_Time'].dtype != 'datetime64[ns]':
            df['Local_Date_Time'] = pd.to_datetime(df['Local_Date_Time'])

        # Find the earliest and latest datestamps
        earliest_datestamp = df['Local_Date_Time'].min()
        latest_datestamp = df['Local_Date_Time'].max()

        # Calculate the timespan
        timespan = latest_datestamp - earliest_datestamp

        return timespan
    else:
        return "Column 'Local_Date_Time' not found in the DataFrame."

def calculate_measurement_interval(df):
    # Check if 'Local_Date_Time' column exists
    if 'Local_Date_Time' in df.columns:
        # Convert 'Local_Date_Time' to datetime if it's not already
        if df['Local_Date_Time'].dtype != 'datetime64[ns]':
            df['Local_Date_Time'] = pd.to_datetime(df['Local_Date_Time'])

        # Calculate the time differences between consecutive timestamps
        time_diffs = df['Local_Date_Time'].diff()

        # Calculate the average measurement interval
        avg_measurement_interval = time_diffs.mean()

        return avg_measurement_interval
    else:
        return "Column 'Local_Date_Time' not found in the DataFrame."

def add_time_diffs_column(df):
    # Check if 'Local_Date_Time' column exists
    if 'Local_Date_Time' in df.columns:
        # Convert 'Local_Date_Time' to datetime if it's not already
        if df['Local_Date_Time'].dtype != 'datetime64[ns]':
            df['Local_Date_Time'] = pd.to_datetime(df['Local_Date_Time'])

        # Calculate the time differences between consecutive timestamps
        time_diffs = df['Local_Date_Time'].diff()

        # Add the 'Time_diffs' column to the DataFrame
        df['Time_diffs'] = time_diffs
        df.at[0, 'Time_diffs'] = pd.Timedelta(seconds=0)  # Set the first value to 0

        return df
    else:
        return "Column 'Local_Date_Time' not found in the DataFrame."

def export_time_diffs_to_file(df, output_file_path='time_diffs.log'):
    # Check if 'Time_diffs' column exists
    if 'Time_diffs' in df.columns:
        # Extract the 'Time_diffs' column
        time_diffs_column = df['Time_diffs']

        # Export the 'Time_diffs' column to a file
        time_diffs_column.to_csv(output_file_path, header=True, index=False, sep='\t')

        return f"Time_diffs column exported to {output_file_path}"
    else:
        return "Column 'Time_diffs' not found in the DataFrame."

def export_dataframe_to_file(df, output_file_path='output_dataframe.log'):
    # Export the DataFrame to a file
    df.to_csv(output_file_path, header=True, index=False, sep='\t')

    return f"DataFrame exported to {output_file_path}"

def fill_time_gaps(df):
    # Check if 'Local_Date_Time' column exists
    if 'Local_Date_Time' in df.columns:
        # Convert 'Local_Date_Time' to datetime if it's not already
        if df['Local_Date_Time'].dtype != 'datetime64[ns]':
            df['Local_Date_Time'] = pd.to_datetime(df['Local_Date_Time'])

        # Calculate the time differences between consecutive timestamps
        time_diffs = df['Local_Date_Time'].diff()

        # Identify indices where the time difference is higher than 1 minute
        gap_indices = time_diffs[time_diffs > pd.Timedelta(minutes=1)].index

        # Iterate through gap indices and insert rows to fill the gap
        for gap_index in gap_indices:
            start_time = df.at[gap_index - 1, 'Local_Date_Time']
            end_time = df.at[gap_index, 'Local_Date_Time']
            num_inserts = int((end_time - start_time) / pd.Timedelta(minutes=1)) - 1

            for i in range(1, num_inserts + 1):
                new_time = start_time + pd.Timedelta(minutes=i)
                new_row = pd.DataFrame([[new_time] + df.iloc[gap_index - 1, 1:].tolist()], columns=df.columns)
                df = pd.concat([df.iloc[:gap_index + i - 1], new_row, df.iloc[gap_index + i - 1:]]).reset_index(drop=True)

        return df
    else:
        return "Column 'Local_Date_Time' not found in the DataFrame."

def find_time_gaps(df, max_time_diff=pd.Timedelta(minutes=1)):
    # Check if 'Local_Date_Time' column exists
    if 'Local_Date_Time' in df.columns:
        # Convert 'Local_Date_Time' to datetime if it's not already
        if df['Local_Date_Time'].dtype != 'datetime64[ns]':
            df['Local_Date_Time'] = pd.to_datetime(df['Local_Date_Time'])

        # Calculate the time differences between consecutive timestamps
        time_diffs = df['Local_Date_Time'].diff()

        # Identify indices where the time difference is greater than max_time_diff
        gap_indices = time_diffs[time_diffs > max_time_diff].index

        return gap_indices
    else:
        return "Column 'Local_Date_Time' not found in the DataFrame."

def fill_time_gaps(df, gap_indices):
    # Check if 'Local_Date_Time' column exists
    if 'Local_Date_Time' in df.columns:
        # Convert 'Local_Date_Time' to datetime if it's not already
        if df['Local_Date_Time'].dtype != 'datetime64[ns]':
            df['Local_Date_Time'] = pd.to_datetime(df['Local_Date_Time'])

        # Iterate through gap indices in reverse order and insert rows to fill the gap
        for gap_index in reversed(gap_indices):
            start_time = df.at[gap_index - 1, 'Local_Date_Time']
            end_time = df.at[gap_index, 'Local_Date_Time']
            num_inserts = int((end_time - start_time) / pd.Timedelta(minutes=1)) - 1

            for i in range(1, num_inserts + 1):
                new_time = start_time + pd.Timedelta(minutes=i)
                new_row = pd.DataFrame([[new_time] + df.iloc[gap_index - 1, 1:].tolist()], columns=df.columns)
                df = pd.concat([df.iloc[:gap_index + i - 1], new_row, df.iloc[gap_index + i - 1:]]).reset_index(drop=True)

        return df
    else:
        return "Column 'Local_Date_Time' not found in the DataFrame."