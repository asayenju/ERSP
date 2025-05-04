import numpy as np
import matplotlib.pyplot as plt

# Function to read the text file
def read_data(file_path):
    """
    Reads the text file containing sensor data.

    :param file_path: Path to the text file
    :return: NumPy array of data
    """
    data = np.loadtxt(file_path, delimiter=',')
    return data

# Function to plot amplitude vs time
def plot_amplitude_vs_time(data, sampling_rate, labels, title):
    """
    Plots amplitude vs time for each axis in the data.

    :param data: 2D array where each column is a signal axis
    :param sampling_rate: Sampling rate in Hz
    :param labels: List of labels for the axes (e.g., ['Ax', 'Ay', 'Az'])
    :param title: Title for the plot
    """
    num_samples = data.shape[0]
    time = np.linspace(0, num_samples / sampling_rate, num_samples)  # Generate time array

    plt.figure(figsize=(12, 6))
    for i in range(data.shape[1]):
        plt.plot(time, data[:, i], label=labels[i])
    
    plt.title(title)
    plt.xlabel('Time [s]')
    plt.ylabel('Amplitude')
    plt.legend()
    plt.grid()
    plt.show()

# Main script
if __name__ == "__main__":
    # Replace 'your_file.txt' with the path to your text file
    file_path = '.\sitting_still\sitting_still_1.txt'
    sampling_rate = 100  # Fixed sampling rate (100 Hz for 10 seconds)

    # Read data
    data = read_data(file_path)

    # Validate the shape
    if data.shape[1] != 6:
        raise ValueError(f"Expected 6 columns, got {data.shape[1]}")

    # Extract columns
    ax, ay, az = data[:, 0], data[:, 1], data[:, 2]
    gx, gy, gz = data[:, 3], data[:, 4], data[:, 5]

    # Plot amplitude vs time for acceleration components
    plot_amplitude_vs_time(np.column_stack((ax, ay, az)), sampling_rate, 
                           ['Ax', 'Ay', 'Az'], 'Amplitude vs Time (Acceleration) for sitting eyes open head side to side')

    # Plot amplitude vs time for gyroscope components
    plot_amplitude_vs_time(np.column_stack((gx, gy, gz)), sampling_rate, 
                           ['Gx', 'Gy', 'Gz'], 'Amplitude vs Time (Gyroscope) for sitting eyes open head side to side')
