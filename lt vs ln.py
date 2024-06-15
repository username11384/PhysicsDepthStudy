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
plt.figure(figsize=(12, 6))
for driver in lap_data['driver'].unique():
    driver_data = lap_data[lap_data['driver'] == driver]
    plt.plot(driver_data['lap'], driver_data['time_seconds'], label=driver)
plt.title('Lap Time vs Lap Number within a Stint')
plt.xlabel('Lap Number')
plt.ylabel('Lap Time (seconds)')
plt.legend()
plt.grid(True)
plt.show()