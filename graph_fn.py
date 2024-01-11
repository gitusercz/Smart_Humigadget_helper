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
    elif timespan == timedelta(hours=23, minutes=59, seconds=59):
        time_unit = 'day'
    else:
        time_unit = 'hours'

    # Convert date stamps to numerical values for plotting on the x-axis
    time_values = mdates.date2num(List_of_datestamps)

    # Plot the graph with temperature values
    fig, ax1 = plt.subplots(figsize=(10, 6))
    ax1.plot(time_values - time_values[0], List_of_T, label='Temperature (T)', color='blue')

    # Customize the x-axis labels based on the time unit
    if time_unit == 'minutes':
        ax1.xaxis.set_major_formatter(mdates.DateFormatter('%M'))
    if time_unit == 'day':
        ax1.xaxis.set_major_locator(plt.MultipleLocator(2))  # Set major ticks every 2 units (hours)
    else:
        ax1.xaxis.set_major_formatter(mdates.DateFormatter('%H'))

    # Include RH values on a secondary Y-axis if include_rh is 'Y'
    if include_rh == 'Y':
        ax2 = ax1.twinx()
        ax2.plot(time_values - time_values[0], List_of_RH, label='Relative Humidity (RH)', color='green')
        ax2.set_ylabel('Relative Humidity (%)', color='green')
        ax2.tick_params(axis='y', labelcolor='green')
    else:
        pass

    ax1.set_xlabel(f'Time ({time_unit})')
    # Customize the y-axis labels
    ax1.set_ylabel('Temperature (°C)')

    # Add both major and minor grid lines
    ax1.grid(True, linestyle='--', alpha=0.5, which='both', color='black', linewidth=0.5)

    # This is a good one to over specify how often minor gridlines show up:
    # ax1.xaxis.set_minor_locator(mdates.MinuteLocator(interval=1))  # Add minor grid lines every minute

    # Set the number of minor gridlines to half the number of major gridlines
    # major_ticks = len(ax1.xaxis.get_major_locator()())
    # ax1.xaxis.set_minor_locator(mdates.MinuteLocator(interval=int(major_ticks / 2)))


    # Customize the plot
    ax1.set_title(title)

    # Show the plot
    plt.show()
