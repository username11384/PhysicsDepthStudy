import pandas as pd
import matplotlib.pyplot as plt
file_path = 'data.csv' 
data = pd.read_csv(file_path)
lap_data = data.iloc[1:,:5]
lap_data.columns = ['raceId', 'driver', 'lap', 'position', 'time']
lap_data = lap_data.dropna().reset_index(drop=True)
def time_to_seconds(lap_time):
    minutes, seconds = lap_time.split(':')
    return int(minutes) * 60 + float(seconds)
lap_data['time_seconds'] = lap_data['time'].apply(time_to_seconds)
lap_data['lap'] = lap_data['lap'].astype(int)
temperature_dict = {
    (1, 20): 26,
    (30, 40): 29,
    (50, 60): 31
}
def assign_temperature(lap):
    for lap_range, temp in temperature_dict.items():
        if lap_range[0] <= lap <= lap_range[1]:
            return temp
    return None
lap_data['temperature'] = lap_data['lap'].apply(assign_temperature)
filtered_lap_data = lap_data.dropna(subset=['temperature'])
average_lap_time = filtered_lap_data.groupby(['driver', 'temperature'])['time_seconds'].mean().reset_index()
plt.figure(figsize=(12, 6))
for driver in average_lap_time['driver'].unique():
    driver_data = average_lap_time[average_lap_time['driver'] == driver]
    plt.plot(driver_data['temperature'], driver_data['time_seconds'], marker='o', label=driver)
plt.title('Average Lap Time per Stint vs Track Temperature')
plt.xlabel('Track Temperature (°C)')
plt.ylabel('Average Lap Time (seconds)')
plt.legend()
plt.grid(True)
plt.show()