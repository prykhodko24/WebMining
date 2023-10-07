import pandas as pd
import matplotlib.pyplot as plt

# Sample DataFrame
data = {
    "singer": ["Artist 1", "Artist 2", "Artist 3", "Artist 4", "Artist 5"],
    "song_rating": [3, 4, 5, 2, 4]
}

df = pd.DataFrame(data)

# Select the column for which you want to create a histogram
column_to_plot = "song_rating"

# Create a histogram
plt.figure(figsize=(8, 5))  # Set the figure size
plt.hist(df[column_to_plot], bins=5, edgecolor='black', alpha=0.7)

# Add labels and a title
plt.xlabel(column_to_plot)
plt.ylabel("Frequency")
plt.title(f"Histogram of {column_to_plot}")

# Show the plot
plt.show()
