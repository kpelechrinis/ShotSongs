import pandas as pd   #import library for loading data, https://pypi.org/project/pandas/
from audiolazy import str2midi
from midiutil import MIDIFile

df = pd.read_csv("shots_phx.csv")

def map_value(value, min_value, max_value, min_result, max_result):
    '''maps value (or array of values) from one range to another'''
    
    result = min_result + (value - min_value)/(max_value - min_value)*(max_result - min_result)
    return result

bpm = 60 

df['t'] = [i for i in range(len(df))]

n_shots = len(df)

t = df['t'].values    #this is a numpy array (not a list), you can do mathematical operations directly on the object
shotClock = df['dribblesBefore'].values
distance = df['distance'].values

times_shots = t

shots_per_beat = 2  #number of Myrs for each beat of music 

t_data = times_shots/shots_per_beat #rescale time from Myrs to beats

# normalize shot clock data

y_data = map_value(shotClock, min(shotClock), max(shotClock), 0, 1) #normalize data, so it runs from 0 to 1 

y_scale = 0.5  #lower than 1 to spread out more evenly

y_data = y_data**y_scale

note_names = ['C1','C2','G2',
             'C3','E3','G3','A3','B3',
             'D4','E4','G4','A4','B4',
             'D5','E5','G5','A5','B5',
             'D6','E6','F#6','G6','A6']

note_midis = [str2midi(n) for n in note_names] #make a list of midi note numbers 
n_notes = len(note_midis)


midi_data = []
for i in range(n_shots):
    note_index = round(map_value(y_data[i], 0, 1, n_notes-1,0)) 
    midi_data.append(note_midis[note_index])


vel_min = 35
vel_max = 127  

y_data = map_value(distance, min(distance), max(distance), 0, 1) #normalize data, so it runs from 0 to 1 
y_scale = 0.5 
y_data = y_data**y_scale

vel_data = []
for i in range(n_shots):
    note_velocity = round(map_value(y_data[i], 0, 1, vel_min, vel_max)) 
    vel_data.append(note_velocity)

my_midi_file = MIDIFile(1) #one track 
my_midi_file.addTempo(track=0, time=0, tempo=bpm) 
filename = "shots_phx"
#add midi notes
for i in range(n_shots):
    my_midi_file.addNote(track=0, channel=0, pitch=midi_data[i], time=t_data[i], duration=2, volume=vel_data[i])

#create and save the midi file itself
with open(filename + '.mid', "wb") as f:
    my_midi_file.writeFile(f) 


