
import matplotlib.dates as mdates
from datetime import timedelta
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker

def plot_temperature_graph(List_of_datestamps, List_of_T, title):
    # Calculate the timespan of the data
    timespan = List_of_datestamps[-1] - List_of_datestamps[0]

    # Determine the appropriate time unit for the x-axis labels
    if timespan < timedelta(hours=2):
        time_unit = 'minutes'
    else:
        time_unit = 'hours'

    # Convert date stamps to numerical values for plotting on the x-axis
    time_values = mdates.date2num(List_of_datestamps)

    # Plot the graph
    plt.figure(figsize=(10, 6))
    plt.plot(time_values - time_values[0], List_of_T, label='Temperature (T)')

    # Customize the x-axis labels based on the time unit
    if time_unit == 'minutes':
        plt.gca().xaxis.set_major_formatter(mdates.DateFormatter('%M:%S'))
    else:
        plt.gca().xaxis.set_major_formatter(mdates.DateFormatter('%H:%M'))

    # Customize the plot
    plt.xlabel(f'Time ({time_unit})')
    plt.ylabel('Temperature (°C)')
    plt.title(title)
    plt.legend()

    # Show the plot
    plt.show()

# Az alábbi függyvényt a 24 órás megjelenítésre hegyeztem ki. DE nem működött jól 1-2 órás intervallumokon. Még nem akarom eldobni, kikommentezem.


def plot_temperature_and_rh_graph(List_of_datestamps, List_of_T, List_of_RH, title, include_rh='N'):
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
    if include_rh == 'Y':
        # Create secondary y-axis for Relative Humidity
        ax2 = ax.twinx()
        ax2.plot(x, List_of_RH, label='Relative Humidity', color='green')
        ax2.set_ylabel("Relative Humidity [%]", fontsize=6)
        ax2.tick_params(axis='y')
        ax2.yaxis.set_minor_locator(ticker.AutoMinorLocator())

    # Customize the plot
    plt.title(title)

    # Show the plot
    plt.show()



