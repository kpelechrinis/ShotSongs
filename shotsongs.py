import pandas as pd   
from audiolazy import str2midi
from midiutil import MIDIFile
import numpy as np

shotClock_la = 12.4
min_shotClock = 11.6 # slow team
max_shotClock = 13.1 # fast team

df = pd.read_csv("shots.csv")

def map_value(value, min_value, max_value, min_result, max_result):
    '''maps value (or array of values) from one range to another'''
    
    result = min_result + (value - min_value)/(max_value - min_value)*(max_result - min_result)
    return result

bpm = 60 

df['t'] = [i for i in range(len(df))]

n_shots = len(df)

t = df['t'].values    #this is a numpy array (not a list), you can do mathematical operations directly on the object
shotClock = df['shotClock'].values
distance = df['distance'].values

bpm = map_value(np.mean(shotClock),min_shotClock,max_shotClock, 40, 150) # we map the tempo within a range of 40 to 300 bpm

times_shots = t
shots_per_beat = 2 #number of shots per beat 
t_data = times_shots/shots_per_beat #rescale time from Myrs to beats

# normalize shot clock data

y_data = map_value(shotClock, 0, 24, 0, 1) #normalize data, so it runs from 0 to 1 

y_scale = 0.5  

y_data = y_data**y_scale

note_names = ['C1','C2','G2',
             'C3','E3','G3','A3','B3',
             'D4','E4','G4','A4','B4',
             'D5','E5','G5','A5','B5',
             'D6','E6','F#6','G6','A6']

note_midis = [str2midi(n) for n in note_names] 
n_notes = len(note_midis)


midi_data = []
for i in range(n_shots):
    note_index = round(map_value(y_data[i], 0, 1, n_notes-1,0)) 
    midi_data.append(note_midis[note_index])


vel_min = 10
vel_max = 127  

y_data = map_value(distance, 0, 50, 0, 1) #normalize data, so it runs from 0 to 1 - we consider only shots up to 50 feet away
y_scale = 0.5 
y_data = y_data**y_scale

vel_data = []
for i in range(n_shots):
    note_velocity = round(map_value(y_data[i], 0, 1, vel_min, vel_max)) 
    vel_data.append(note_velocity)

my_midi_file = MIDIFile(1) 
my_midi_file.addTempo(track=0, time=0, tempo=bpm) 
filename = "shots"

for i in range(n_shots):
    my_midi_file.addNote(track=0, channel=0, pitch=midi_data[i], time=t_data[i], duration=2, volume=vel_data[i])

#create and save the midi file itself
with open(filename + '.mid', "wb") as f:
    my_midi_file.writeFile(f) 


