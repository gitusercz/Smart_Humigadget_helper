import matplotlib.pyplot as plt
import matplotlib.dates as mdates


def plot_temperature_graph(List_of_datestamps, List_of_T, title):
    # Convert date stamps to numerical values for plotting on the x-axis
    time_values = mdates.date2num(List_of_datestamps)

    # Plot the graph
    plt.figure(figsize=(10, 6))
    plt.plot(time_values - time_values[0], List_of_T, label='Temperature (T)')

    # Customize the plot
    plt.xlabel('Time (hours)')
    plt.ylabel('Temperature (°C)')
    plt.title(title)
    plt.legend()

    # Show the plot
    plt.show()