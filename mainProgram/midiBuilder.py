import midi


class MidiBuilder:

    def __init__(self, resolution):
        self.resolution = resolution
        self.playing_notes = []
        self.curr_pat = None
        self.curr_track = None
        self.curr_tempo = 120
        self.last_ev_time = 0

    def set_resolution(self, new_resolution):
        self.resolution = new_resolution

    def create_midi(self):
        self.curr_pat = midi.Pattern(tracks=[], resolution=self.resolution, format=1, tick_relative=True)
        self.curr_track = midi.Track()
        self.curr_pat.append(self.curr_track)

    def end_midi(self, name):
        self.curr_track.append(midi.EndOfTrackEvent(tick=1))
        print(self.curr_pat)
        midi.write_midifile(name+".mid", self.curr_pat)

    def change_tempo(self, new_tempo, changed_tempo_time=0):
        self.curr_tempo = new_tempo
        temp_ev = midi.SetTempoEvent()
        temp_ev.set_bpm(self.curr_tempo)
        self.curr_track.append(temp_ev)
        self.last_ev_time += changed_tempo_time

    def play_note(self, on_time, off_time, pitch, pressure=100):
        secs_per_tick = 60 / self.curr_tempo / self.resolution
        on_tick = int((on_time - self.last_ev_time) / secs_per_tick)
        off_tick = int((off_time - on_time) / secs_per_tick)

        self.curr_track.append(midi.NoteOnEvent(tick=on_tick, velocity=pressure, pitch=pitch))
        self.curr_track.append(midi.NoteOffEvent(tick=off_tick, pitch=pitch))
        self.last_ev_time = off_time

# Muestro como usar
midi_filer = MidiBuilder(1000)
midi_filer.create_midi()
midi_filer.change_tempo(120)
midi_filer.play_note(on_time=2, off_time=3, pitch=midi.G_3)
midi_filer.play_note(on_time=4, off_time=6, pitch=midi.A_3)
midi_filer.end_midi('NuevoTrack')

