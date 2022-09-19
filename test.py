import magenta
import note_seq
from note_seq.protobuf import music_pb2

seed = music_pb2.NoteSequence()  # NoteSequence

# notesにnoteを追加
seed.notes.add(pitch=80, start_time=0.0, end_time=0.4, velocity=80)
seed.notes.add(pitch=80, start_time=0.4, end_time=0.8, velocity=80)
seed.notes.add(pitch=87, start_time=0.8, end_time=1.2, velocity=80)
seed.notes.add(pitch=87, start_time=1.2, end_time=1.6, velocity=80)
seed.notes.add(pitch=89, start_time=1.6, end_time=2.0, velocity=80)
seed.notes.add(pitch=89, start_time=2.0, end_time=2.4, velocity=80)
seed.notes.add(pitch=87, start_time=2.4, end_time=3.2, velocity=80)

seed.total_time = 3.2  # 所要時間
seed.tempos.add(qpm=75);  # 曲のテンポを指定

print(note_seq.plot_sequence(seed))  # NoteSequenceの可視化
print(note_seq.play_sequence(seed, synth=note_seq.fluidsynth))  # NoteSequenceの再生