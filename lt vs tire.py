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
tire_compounds = {
    'ver': [(1, 13, 'soft'), (13, 36, 'hard'), (36, 53, 'hard'), (53, 57, 'soft')],
    'ham': [(1, 14, 'medium'), (14, 57, 'hard')]
}
def assign_compound(driver, lap):
    if driver == 'ver':
        for start, end, compound in tire_compounds['ver']:
            if start <= lap <= end:
                return compound
    elif driver == 'ham':
        for start, end, compound in tire_compounds['ham']:
            if start <= lap <= end:
                return compound
    return None
lap_data['compound'] = lap_data.apply(lambda row: assign_compound(row['driver'], row['lap']), axis=1)
filtered_lap_data_with_compound = lap_data.dropna(subset=['compound'])
average_lap_time_compound = filtered_lap_data_with_compound.groupby(['driver', 'compound'])['time_seconds'].mean().reset_index()
plt.figure(figsize=(12, 6))
for driver in average_lap_time_compound['driver'].unique():
    driver_data = average_lap_time_compound[average_lap_time_compound['driver'] == driver]
    plt.plot(driver_data['compound'], driver_data['time_seconds'], marker='o', linestyle='-', label=driver)
plt.title('Average Lap Time per Stint vs Tire Compound')
plt.xlabel('Tire Compound')
plt.ylabel('Average Lap Time (seconds)')
plt.legend()
plt.grid(True)
plt.show()
