import numpy as np
import matplotlib.pyplot as plt

# Step 1: Load the data from the text file
filename = "sitting_eyes_close.txt"  # Replace with your text file name

# Load the data (assuming it has 6 columns: ax, ay, az, gx, gy, gz)
data = np.loadtxt(filename, delimiter=',')  # Adjust delimiter if necessary

# Step 2: Separate the columns
ax = data[:, 0]  # First column: ax
ay = data[:, 1]  # Second column: ay
az = data[:, 2]  # Third column: az
gx = data[:, 3]  # Fourth column: gx
gy = data[:, 4]  # Fifth column: gy
gz = data[:, 5]  # Sixth column: gz

# Step 3: Generate spectrograms for each component
def plot_spectrogram(data, title, ylabel="Frequency"):
    plt.figure(figsize=(10, 6))
    plt.specgram(data, NFFT=256, Fs=100.0, cmap='viridis')  # NFFT=256 is the window size, Fs is the sampling frequency
    plt.colorbar(label="Intensity (dB)")
    plt.xlabel("Time")
    plt.ylabel(ylabel)
    plt.title(title)
    plt.show()

# Plot spectrograms for acceleration components
plot_spectrogram(ax, "Spectrogram of ax (Acceleration X)")
plot_spectrogram(ay, "Spectrogram of ay (Acceleration Y)")
plot_spectrogram(az, "Spectrogram of az (Acceleration Z)")

# Plot spectrograms for gyroscope components
plot_spectrogram(gx, "Spectrogram of gx (Gyroscope X)")
plot_spectrogram(gy, "Spectrogram of gy (Gyroscope Y)")
plot_spectrogram(gz, "Spectrogram of gz (Gyroscope Z)")