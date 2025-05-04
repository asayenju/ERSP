import numpy as np
import scipy.signal as signal
import matplotlib.pyplot as plt

# Step 1: Load data from text file
def load_data(file_path):
    """
    Load data from a text file formatted as ax, ay, az, gx, gy, gz.
    """
    data = np.loadtxt(file_path, delimiter=',')
    return data

# Step 2: Apply bandpass filter
def apply_bandpass_filter(data, low_cutoff, high_cutoff, sampling_rate, filter_order=4):
    """
    Apply a Butterworth bandpass filter to the data.
    """
    # Normalize cutoff frequencies
    nyquist_frequency = 0.5 * sampling_rate
    low = low_cutoff / nyquist_frequency
    high = high_cutoff / nyquist_frequency

    # Design Butterworth bandpass filter
    b, a = signal.butter(filter_order, [low, high], btype='band')

    # Apply zero-phase filtering to avoid distortion
    filtered_data = signal.filtfilt(b, a, data)
    return filtered_data

# Step 3: Plot original and filtered data
def plot_data(t, original, filtered, title, ylabel):
    """
    Plot original and filtered data for a single axis.
    """
    plt.figure(figsize=(12, 6))
    plt.plot(t, original, label='Original', alpha=0.5)
    plt.plot(t, filtered, label='Filtered', linewidth=2)
    plt.xlabel('Time (s)')
    plt.ylabel(ylabel)
    plt.title(title)
    plt.legend()
    plt.grid()
    plt.show()

# Main function
def main():
    # File path to your data
    file_path = 'data\sitting_eyes_close.txt'  # Replace with your file path

    # Load data
    data = load_data(file_path)

    # Separate accelerometer and gyroscope data
    ax = data[:, 0]  # Accelerometer x-axis
    ay = data[:, 1]  # Accelerometer y-axis
    az = data[:, 2]  # Accelerometer z-axis
    gx = data[:, 3]  # Gyroscope x-axis
    gy = data[:, 4]  # Gyroscope y-axis
    gz = data[:, 5]  # Gyroscope z-axis

    # Define sampling rate (adjust if necessary)
    sampling_rate = 100  # Hz

    # Define cutoff frequencies for walking (0.5 Hz to 3 Hz)
    low_cutoff = 0.5  # Hz
    high_cutoff = 1 # Hz

    # Apply bandpass filter to accelerometer data
    ax_filtered = apply_bandpass_filter(ax, low_cutoff, high_cutoff, sampling_rate)
    ay_filtered = apply_bandpass_filter(ay, low_cutoff, high_cutoff, sampling_rate)
    az_filtered = apply_bandpass_filter(az, low_cutoff, high_cutoff, sampling_rate)

    # Apply bandpass filter to gyroscope data
    gx_filtered = apply_bandpass_filter(gx, low_cutoff, high_cutoff, sampling_rate)
    gy_filtered = apply_bandpass_filter(gy, low_cutoff, high_cutoff, sampling_rate)
    gz_filtered = apply_bandpass_filter(gz, low_cutoff, high_cutoff, sampling_rate)

    # Create time axis
    t = np.arange(len(ax)) / sampling_rate

    # Plot accelerometer data
    
    plot_data(t, ax, ax_filtered, 'Accelerometer X-Axis', 'Acceleration (m/s²)')
    plot_data(t, ay, ay_filtered, 'Accelerometer Y-Axis', 'Acceleration (m/s²)')
    plot_data(t, az, az_filtered, 'Accelerometer Z-Axis', 'Acceleration (m/s²)')

    # Plot gyroscope data
    plot_data(t, gx, gx_filtered, 'Gyroscope X-Axis', 'Angular Velocity (rad/s)')
    plot_data(t, gy, gy_filtered, 'Gyroscope Y-Axis', 'Angular Velocity (rad/s)')
    plot_data(t, gz, gz_filtered, 'Gyroscope Z-Axis', 'Angular Velocity (rad/s)')

    def plot_spectrogram(data, title, ylabel="Frequency"):
        plt.figure(figsize=(10, 6))
        plt.specgram(data, NFFT=256, Fs=100.0, cmap='viridis')  # NFFT=256 is the window size, Fs is the sampling frequency
        plt.colorbar(label="Intensity (dB)")
        plt.xlabel("Time")
        plt.ylabel(ylabel)
        plt.title(title)
        plt.show()
    plot_spectrogram(ax_filtered, "Spectrogram of ax (Acceleration X)")
    plot_spectrogram(ay_filtered, "Spectrogram of ay (Acceleration Y)")
    plot_spectrogram(az_filtered, "Spectrogram of az (Acceleration Z)")

    # Plot spectrograms for gyroscope components
    plot_spectrogram(gx_filtered, "Spectrogram of gx (Gyroscope X)")
    plot_spectrogram(gy_filtered, "Spectrogram of gy (Gyroscope Y)")
    plot_spectrogram(gz_filtered, "Spectrogram of gz (Gyroscope Z)")

    #step 4: Put the filtered data in a text file
    with open('filter_sitting_eyes_close/filtered_data_sitting_eyes_close.txt', 'w', encoding='utf-8') as file:
        for i in range(len(ax_filtered)):
            filtered = f"{ax_filtered[i]}, {ay_filtered[i]}, {az_filtered[i]}, {gx_filtered[i]}, {gy_filtered[i]}, {gz_filtered[i]}"
            file.write(filtered + "\n")
        

    
# Run the main function
if __name__ == "__main__":
    main()