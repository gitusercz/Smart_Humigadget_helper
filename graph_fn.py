import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from datetime import timedelta

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


def plot_temperature_and_rh_graph(List_of_datestamps, List_of_T, List_of_RH, title, include_rh='N'):
    # Calculate the timespan of the data
    timespan = List_of_datestamps[-1] - List_of_datestamps[0]

    # Determine the appropriate time unit for the x-axis labels
    if timespan < timedelta(hours=2):
        time_unit = 'minutes'
    else:
        time_unit = 'hours'

    # Convert date stamps to numerical values for plotting on the x-axis
    time_values = mdates.date2num(List_of_datestamps)

    # Plot the graph with temperature values
    plt.figure(figsize=(10, 6))
    plt.plot(time_values - time_values[0], List_of_T, label='Temperature (T)', color='blue')

    # Customize the x-axis labels based on the time unit
    if time_unit == 'minutes':
        plt.gca().xaxis.set_major_formatter(mdates.DateFormatter('%M:%S'))
    else:
        plt.gca().xaxis.set_major_formatter(mdates.DateFormatter('%H:%M'))

    # Include RH values on a secondary Y-axis if include_rh is 'Y'
    if include_rh == 'Y':
        ax2 = plt.gca().twinx()
        ax2.plot(time_values - time_values[0], List_of_RH, label='Relative Humidity (RH)', color='green')
        ax2.set_ylabel('Relative Humidity (%)', color='green')
        ax2.tick_params(axis='y', labelcolor='green')
    else:
        pass

    plt.xlabel(f'Time ({time_unit})')
    # Customize the y-axis labels
    plt.ylabel('Temperature (°C)')

    # Add grid lines
    plt.grid(True, linestyle='--', alpha=0.5)

    # Customize the plot
    plt.title(title)

    # Show the plot
    plt.show()