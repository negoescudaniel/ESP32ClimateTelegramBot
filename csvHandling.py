import pandas as pd
import csv
from datetime import datetime
import matplotlib.pyplot as plt

class CSV:
    CSV_FILE = "sensor_data.csv"
    COLUMNS = ["date", "temperature", "humidity"]
    FORMAT = "%Y-%m-%d %H:%M:%S"  # Updated format to match CSV file

    @classmethod
    def initialize_csv(cls):
        try:
            pd.read_csv(cls.CSV_FILE)
        except FileNotFoundError:
            df = pd.DataFrame(columns=cls.COLUMNS)  # Initialize with empty columns
            df.to_csv(cls.CSV_FILE, index=False)

    @classmethod
    def add_entry(cls, date, temperature, humidity):
        new_entry = {
            "date": date.strftime(cls.FORMAT),  # Format date with hour, minute, and seconds
            "temperature": temperature,
            "humidity": humidity
        }

        with open(cls.CSV_FILE, "a", newline="") as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=cls.COLUMNS)
            writer.writerow(new_entry)
        print("Entry added successfully")

    @classmethod
    
    def get_readings(cls, start_date_str, end_date_str):
        # Read the CSV file into a DataFrame
        try:
            df = pd.read_csv(cls.CSV_FILE)
            print("CSV file read successfully.")
        except Exception as e:
            print(f"Error reading CSV file: {e}")
            return None

        # Convert the 'date' column to datetime objects
        try:
            df["date"] = pd.to_datetime(df["date"], format=cls.FORMAT)
            print("Date column parsed successfully.")
        except Exception as e:
            print(f"Error parsing date column: {e}")
            return None

        # Parse the start and end dates from strings
        try:
            start_date = datetime.strptime(start_date_str, cls.FORMAT)
            end_date = datetime.strptime(end_date_str, cls.FORMAT)
            print(f"Start Date: {start_date}, End Date: {end_date}")
        except ValueError as e:
            print(f"Error parsing input dates: {e}")
            return None

        # Filter the DataFrame based on the date range
        try:
            mask = (df["date"] >= start_date) & (df["date"] <= end_date)
            filtered_df = df.loc[mask]
            print(f"Data filtered successfully, number of rows: {len(filtered_df)}")
        except Exception as e:
            print(f"Error filtering data: {e}")
            return None

        # Check if the filtered DataFrame is empty
        if filtered_df.empty:
            print("No readings found in the specified date range!")
            return None  # Return None if no data is found
        else:
            print(f"Readings from {start_date.strftime(cls.FORMAT)} to {end_date.strftime(cls.FORMAT)}:")
            print(filtered_df.to_string(index=False))  # Print the filtered DataFrame without index

        return filtered_df  # Return the filtered DataFrame for further processing


def plot_temperature_and_humidity_readings(df):
    # Ensure the 'date' column is in datetime format
    df['date'] = pd.to_datetime(df['date'], format="%Y-%m-%d %H:%M:%S")
    
    # Set the 'date' column as the index
    df.set_index("date", inplace=True)

    # Resample the data to daily averages (or use other resampling methods if needed)
    daily_avg = df.resample("D").mean()

    # Create the plot with dual y-axes
    fig, ax1 = plt.subplots(figsize=(10, 5))

    # Plot temperature on the first y-axis (ax1)
    ax1.plot(daily_avg.index, daily_avg["temperature"], label="Temperature", color='blue')
    ax1.set_xlabel("Date")
    ax1.set_ylabel("Temperature (°C)", color='blue')
    ax1.tick_params(axis='y', labelcolor='blue')

    # Create a second y-axis (ax2) sharing the same x-axis
    ax2 = ax1.twinx()
    ax2.plot(daily_avg.index, daily_avg["humidity"], label="Humidity", color='green')
    ax2.set_ylabel("Humidity (%)", color='green')
    ax2.tick_params(axis='y', labelcolor='green')

    # Add titles and grid
    plt.title("Daily Average Temperature and Humidity Over Time")
    ax1.grid(True)
    plt.legend()

    # Save the plot as an image file
    plot_path = 'temperature_humidity_plot.png'
    plt.tight_layout()
    plt.savefig(plot_path)
    plt.close()  # Close the plot to free up memory
    return plot_path  # Return the path of the saved plot
    # Show the plot
    #plt.show()

#def main():
 #   print("JEE")
  #  df = CSV.get_readings('2023-09-01 00:30:00', '2023-09-17 04:00:00')  # Adjust the date format
   # print("zeeee")
   # if df is not None:
    #    plot_temperature_and_humidity_readings(df)

#main()
