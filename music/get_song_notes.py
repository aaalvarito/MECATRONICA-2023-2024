from music21 import converter, instrument, note, stream, chord

def midi_to_notes(file_path):
    midi = converter.parse(file_path)

    notes_to_parse = None

    try: # File has instrument parts
        s2 = instrument.partitionByInstrument(midi)
        notes_to_parse = s2.parts[0].recurse() 
    except: # File has notes in a flat structure
        notes_to_parse = midi.flat.notes

    notes = []
    for element in notes_to_parse:
        if isinstance(element, note.Note):
            notes.append(str(element.pitch))

    return notes

def convert_to_staff(notes):
    # Convert notes to the format of the treble clef staff
    staff_notes = []

    for n in notes:
        if len(n) > 2:  # Removing octave number from the note if it exists
            staff_notes.append(n[:-1])
        else:
            staff_notes.append(n)

    return staff_notes

# Example usage
file_path = 'las_cuatro_estaciones_primavera.mid'
notes = midi_to_notes(file_path)
staff_notes = convert_to_staff(notes)
print(staff_notes)
