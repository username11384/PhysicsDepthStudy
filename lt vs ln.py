import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.patheffects as path_effects
file_path = 'data.csv'
data = pd.read_csv(file_path)
lap_data = data.iloc[1:, :5]
lap_data.columns = ['raceId', 'driver', 'lap', 'position', 'time']
lap_data = lap_data.dropna().reset_index(drop=True)
def time_to_seconds(lap_time):
    minutes, seconds = lap_time.split(':')
    return int(minutes) * 60 + float(seconds)
lap_data['time_seconds'] = lap_data['time'].apply(time_to_seconds)
lap_data['lap'] = lap_data['lap'].astype(int)
tire_compounds = {
    'ver': [(1, 13, 'soft'), (13, 36, 'hard'), (36, 53, 'newhard'), (53, 58, 'newsoft')],
    'ham': [(1, 14, 'medium'), (14, 58, 'hard')]
}
pit_stops = {
    'ver': [13, 36, 53],
    'ham': [14]
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
plt.figure(figsize=(12, 6))
compound_colors_ver = {'soft': 'red', 'newhard': 'brown', 'hard': 'black', 'newsoft': 'purple'}
compound_colors_ham = {'soft': 'blue', 'medium': 'green', 'hard': 'orange'}
for driver in lap_data['driver'].unique():
    driver_data = lap_data[lap_data['driver'] == driver]
    if driver == 'ver':
        for compound, color in compound_colors_ver.items():
            compound_data = driver_data[driver_data['compound'] == compound]
            plt.plot(compound_data['lap'], compound_data['time_seconds'], marker='o', linestyle='-', color=color, label=f'Verstappen - {compound}')
    elif driver == 'ham':
        for compound, color in compound_colors_ham.items():
            compound_data = driver_data[driver_data['compound'] == compound]
            plt.plot(compound_data['lap'], compound_data['time_seconds'], marker='o', linestyle='-', color=color, label=f'Hamilton - {compound}')
    for i, pit_stop in enumerate(pit_stops[driver]):
        pit_lap_data = driver_data[driver_data['lap'] == pit_stop]
        if driver == 'ver':
            plt.scatter(pit_lap_data['lap'], pit_lap_data['time_seconds'], color='red', s=100, zorder=5, edgecolors='white')
            text_label = f"V PIT ({pit_stop})"  
        elif driver == 'ham':
            plt.scatter(pit_lap_data['lap'], pit_lap_data['time_seconds'], color='green', s=100, zorder=5, edgecolors='white')
            text_label = f"H PIT ({pit_stop})"  
        for j in range(len(pit_lap_data)):
            y_offset = 3 if driver == 'ver' and i == 0 else 0  
            text = plt.text(
                pit_lap_data.iloc[j]['lap'], 
                pit_lap_data.iloc[j]['time_seconds'] + y_offset,  
                text_label, 
                fontsize=12, 
                fontweight='bold', 
                color='black', 
                ha='center', 
                va='center', 
                zorder=6
            )
            text.set_path_effects([path_effects.Stroke(linewidth=3, foreground='white'), path_effects.Normal()])
plt.title('Lap Time vs Lap Number within a Stint (Color-Coded by Tire Compound) with Pit Stops')
plt.xlabel('Lap Number')
plt.ylabel('Lap Time (seconds)')
plt.xlim(1, 60)
plt.legend()
plt.grid(True)
plt.show()
