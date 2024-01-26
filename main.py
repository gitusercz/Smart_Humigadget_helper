import tkinter as tk
from tkinter import ttk, filedialog, messagebox
from datetime import datetime, timedelta
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
import functions

# ============= Defining variables for global use ===========
df_filled_gaps = []
just_started = 0
# ===========================================================

# Function to calculate and show timespan
def show_timespan():
    try:
        # Parse the start and end times
        start_time = datetime.strptime(start_time_entry.get(), '%Y-%m-%d %H:%M:%S')
        end_time = datetime.strptime(end_time_entry.get(), '%Y-%m-%d %H:%M:%S')

        # Calculate the timespan
        timespan = end_time - start_time
        timespan_seconds = timespan.total_seconds()

        # Update the result in the text field
        result_text.config(state=tk.NORMAL)  # Temporarily make it editable to change text
        result_text.delete('1.0', tk.END)  # Clear existing text
        result_text.insert(tk.END, f"The timespan is {timespan_seconds} seconds.")  # Insert new text
        result_text.config(state=tk.DISABLED)  # Make it non-editable again
    except ValueError:
        result_text.config(state=tk.NORMAL)
        result_text.delete('1.0', tk.END)
        result_text.insert(tk.END, "Invalid date format. Please use YYYY-MM-DD hh:mm:ss.")
        result_text.config(state=tk.DISABLED)

def plot_temperature_and_rh_graph():
    global df_filled_gaps

    try:
        # Parse the start and end times
        user_datetime = datetime.strptime(start_time_entry.get(), '%Y-%m-%d %H:%M:%S')

        hours, minutes, seconds = map(int, end_time_entry.get().split(':'))
        if hours < 0 or minutes < 0 or minutes >= 60 or seconds < 0 or seconds >= 60:
            raise ValueError
        user_timespan = timedelta(hours=hours, minutes=minutes, seconds=seconds)
        # user_timespan = datetime.strptime(end_time_entry.get(), '%H:%M:%S')
        # user_datetime = pd.Timestamp(user_datetime)
        # user_timespan = pd.Timedelta(user_timespan)
    except ValueError:
        result_text.config(state=tk.NORMAL)
        result_text.delete('1.0', tk.END)
        result_text.insert(tk.END, "Invalid date format. Please Check again.")
        result_text.config(state=tk.DISABLED)

    startife = functions.find_closest_index(df_filled_gaps, user_datetime)  # Start Index for Extract
    lastife = functions.find_index_after_timespan(df_filled_gaps,functions.find_closest_index(df_filled_gaps, user_datetime),user_timespan)  # Last index for Extract

    List_of_datestamps, List_of_T, List_of_RH = functions.extract_data_between_indices(df_filled_gaps, startife,
                                                                                       lastife)
    # Calculate the timespan of the data
    timespan = List_of_datestamps[-1] - List_of_datestamps[0]
    time_diff_secs = timespan.total_seconds()
    time_diff_in_mins = time_diff_secs / 60
    time_diff_in_hours = time_diff_secs / 3600

    # Determine x-axis scale based on the timespan
    if time_diff_secs < 100:
        x = np.linspace(0, time_diff_secs, len(List_of_T))
        plt.xlabel("Time [seconds]", fontsize=6)
    elif time_diff_in_hours < 4:
        x = np.linspace(0, time_diff_in_mins, len(List_of_T))
        plt.xlabel("Time [minutes]", fontsize=6)
    else:
        x = np.linspace(0, time_diff_in_hours, len(List_of_T))
        plt.xlabel("Time [hours]", fontsize=6)

    # Plot temperature data
    plt.plot(x, List_of_T, label='Temperature', color='blue')
    plt.ylabel("Temperature (T)", fontsize=6)

    # Setup axes, ticks, and grid lines
    ax = plt.gca()
    ax.xaxis.set_minor_locator(ticker.AutoMinorLocator())
    ax.yaxis.set_minor_locator(ticker.AutoMinorLocator())

    # Setup major and minor grid lines
    ax.grid(which='both', color='gray', linestyle=':', linewidth=0.5, alpha=0.5)
    ax.grid(which='major', color='black', alpha=0.7, linewidth=0.5)

    # Check if Relative Humidity is to be included
    if humidity_needed_var.get():
        # Create secondary y-axis for Relative Humidity
        ax2 = ax.twinx()
        ax2.plot(x, List_of_RH, label='Relative Humidity', color='green')
        ax2.set_ylabel("Relative Humidity [%]", fontsize=6)
        ax2.tick_params(axis='y')
        ax2.yaxis.set_minor_locator(ticker.AutoMinorLocator())

    # Customize the plot
    plt.title(title_entry.get())

    # Show the plot
    plt.show()

# Function to enable or disable UI elements
def toggle_ui(state):
    title_entry.config(state=state)
    humidity_checkbox.config(state=state)
    start_time_entry.config(state=state)
    end_time_entry.config(state=state)
    show_graph_button.config(state=state)

# Function to handle file selection
def on_file_select():
    global df_filled_gaps

    log_file_path = filedialog.askopenfilename()
    if log_file_path:
        if log_file_path.lower().endswith(('.zip', '.edf')):
            toggle_ui('normal')
        else:
            messagebox.showwarning("Warning", "Incorrect file selected!")
            toggle_ui('disabled')
    df = functions.read_logfile(log_file_path)
    earliest_datestamp = functions.get_earliest_datestamp(df)
    latest_datestamp = functions.get_latest_datestamp(df)
    timespan = functions.calculate_timespan(df)
    measurement_interval = functions.calculate_measurement_interval(df)
    estimated_meas_interval = functions.round_measurement_interval(measurement_interval)

    result_text.config(state=tk.NORMAL)  # Temporarily make it editable to change text
    result_text.delete('1.0', tk.END)  # Clear existing text
    result_text.insert(tk.END,
                       f"Logfile loaded. Processing. Please wait...")  # Insert new text
    result_text.config(state=tk.DISABLED)  # Make it non-editable again

    gap_indices = functions.find_time_gaps(df, max_time_diff=estimated_meas_interval)
    df_filled_gaps = functions.fill_time_gaps(df, gap_indices)

    result_text.config(state=tk.NORMAL)  # Temporarily make it editable to change text
    result_text.delete('1.0', tk.END)  # Clear existing text
    result_text.insert(tk.END,
                       f"Logfile loaded.\nEarliest measurement: {earliest_datestamp}\nLast measurement: {latest_datestamp}\nTimespan of measurment: {timespan}\n\nEstimated measurement interval: {estimated_meas_interval}")  # Insert new text
    result_text.config(state=tk.DISABLED)  # Make it non-editable again


# Create the main window
root = tk.Tk()
root.title("Sensirion helper")

style = ttk.Style(root)
style.theme_use('vista')  # Using the 'vista' theme

# File selection button
file_select_button = ttk.Button(root, text="Select file", command=on_file_select)
file_select_button.pack(padx=10, pady=10)



# Non-editable text field for displaying results
result_text = tk.Text(root, height=7, width=70, state=tk.DISABLED)
result_text.pack(pady=20)

# Title input field
title_label = ttk.Label(root, text="Title:")
title_label.pack()
title_entry = ttk.Entry(root, width=40)
title_entry.pack()

# Humidity needed checkbox
humidity_label = ttk.Label(root, text="Humidity needed?")
humidity_label.pack()
humidity_needed_var = tk.BooleanVar()
humidity_checkbox = ttk.Checkbutton(root, text="", variable=humidity_needed_var)
humidity_checkbox.pack()

# Start time and End time input fields
start_time_label = ttk.Label(root, text="Start time (YYYY-MM-DD hh:mm:ss):")
start_time_label.pack()
start_time_entry = ttk.Entry(root, width=40)
start_time_entry.pack()

end_time_label = ttk.Label(root, text="Timespan: (hh:mm:ss):")
end_time_label.pack()
end_time_entry = ttk.Entry(root, width=40)
end_time_entry.pack()

# Show graph button
show_graph_button = ttk.Button(root, text="Show graph", command=plot_temperature_and_rh_graph)
show_graph_button.pack(pady=10)

# Disable UI elements initially
toggle_ui('disabled')

# Start the main loop
root.mainloop()
