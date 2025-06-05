import numpy as np

# Parameters
num_points = 1024
fs = 1024
t = np.arange(num_points) / fs

# Frequencies (in Hz)
f1 = 50
f2 = 100

# Generate sine waves
sine_wave1 = np.sin(2 * np.pi * f1 * t)
sine_wave2 = np.sin(2 * np.pi * f2 * t)

# Combined signal
combined_signal = sine_wave1 + sine_wave2 

# Format values as strings with 8 decimal places (string format not needed now, keep as floats)
signal_values = combined_signal.tolist()

# Write to .s file in RISC-V .float format
with open("generated_signal.s", "w") as f:
    f.write(".data\n")
    f.write("signal:\n")

    for i in range(0, len(signal_values), 10):
        line_values = signal_values[i:i+10]
        line = "    .float " + ", ".join(f"{val:.4f}" for val in line_values)
        f.write(line + "\n")

print("Assembly signal section written to 'generated_signal.s'")
