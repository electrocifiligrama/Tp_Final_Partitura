from mingus import midi
from mingus.extra import lilypond

lilypond.to_png(lilypond.from_Composition(midi.midi_file_in.MIDI_to_Composition('punteoSongPiano.mid')), 'score')
