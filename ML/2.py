# Write a program to implement different feature scaling techniques using Python.

# Importing the necessary libraries
import numpy as np
import matplotlib.pyplot as plt

# Define the data
x = np.arange(0, 20, 2)
y1 = np.array([2, 103, 8, -90, 0, -6, 15, 66, 0, 92])
y2 = np.array([204, -3, -6, 4, 32, 0, 12, 540, 10, 10])

# Plot the data
plt.plot(x, y1, 'red')
plt.plot(x, y2, 'blue')

# a) Absolute Maximum Scaling

# Scaling the data
y1_new = y1 / max(y1)
y2_new = y2 / max(y2)

# Plotting
plt.plot(x, y1_new, 'red')
plt.plot(x, y2_new, 'blue')

# b) Min Max Scaling

# Scaling the data
y1_new = (y1 - min(y1)) / (max(y1) - min(y1))
y2_new = (y2 - min(y2)) / (max(y2) - min(y2))

# Plotting
plt.plot(x, y1_new, 'red')
plt.plot(x, y2_new, 'blue')

# c) Normalization

# Scaling the data
y1_new = (y1 - np.mean(y1)) / (max(y1) - min(y1))
y2_new = (y2 - np.mean(y2)) / (max(y2) - min(y2))

# Plotting
plt.plot(x, y1_new, 'red')
plt.plot(x, y2_new, 'blue')

# d) Standardization

# Scaling the data
y1_new = (y1 - np.mean(y1)) / np.std(y1)
y2_new = (y2 - np.mean(y2)) / np.std(y2)

# Plot
plt.plot(x, y1_new, 'red')
plt.plot(x, y2_new, 'blue')