from music21 import converter, instrument, note, stream, chord
import mido
import serial
import sys

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
            notes.append(element.pitch.nameWithOctave)
        elif isinstance(element, chord.Chord):
            notes.append('.'.join(n.pitch.nameWithOctave for n in element.notes))

    return notes

def convert_to_clave_de_sol(notes):
    # Convertir las notas a la notación de la clave de sol en español
    converted_notes = []
    notes_diccionary = {"C": "Do", "D": "Re", "E": "Mi", "F": "Fa", "G": "Sol", "A": "La", "B": "Si"}

    for n in notes:
        note, octave = n[:-1], n[-1] if n[-1].isdigit() else n[-2:]
        if note in notes_diccionary:
            converted_notes.append(notes_diccionary[note] + octave)

    return converted_notes

def convert_clave_sol_to_numbers(notes):
    # Asignar números a las notas en función de la tabla de equivalencia
    equivalence_table = {
        'Do0': 1,  'Do#0': 2,  'Re0': 3,  'Re#0': 4,  'Mi0': 5,  'Fa0': 6,  'Fa#0': 7,  'Sol0': 8,  'Sol#0': 9,  'La0': 10, 'La#0': 11, 'Si0': 12,
        'Do1': 13, 'Do#1': 14, 'Re1': 15, 'Re#1': 16, 'Mi1': 17, 'Fa1': 18, 'Fa#1': 19, 'Sol1': 20, 'Sol#1': 21, 'La1': 22, 'La#1': 23, 'Si1': 24,
        'Do2': 25, 'Do#2': 26, 'Re2': 27, 'Re#2': 28, 'Mi2': 29, 'Fa2': 30, 'Fa#2': 31, 'Sol2': 32, 'Sol#2': 33, 'La2': 34, 'La#2': 35, 'Si2': 36,
        'Do3': 37, 'Do#3': 38, 'Re3': 39, 'Re#3': 40, 'Mi3': 41, 'Fa3': 42, 'Fa#3': 43, 'Sol3': 44, 'Sol#3': 45, 'La3': 46, 'La#3': 47, 'Si3': 48,
        'Do4': 49, 'Do#4': 50, 'Re4': 51, 'Re#4': 52, 'Mi4': 53, 'Fa4': 54, 'Fa#4': 55, 'Sol4': 56, 'Sol#4': 57, 'La4': 58, 'La#4': 59, 'Si4': 60,
        'Do5': 61, 'Do#5': 62, 'Re5': 63, 'Re#5': 64, 'Mi5': 65, 'Fa5': 66, 'Fa#5': 67, 'Sol5': 68, 'Sol#5': 69, 'La5': 70, 'La#5': 71, 'Si5': 72,
        'Do6': 73, 'Do#6': 74, 'Re6': 75, 'Re#6': 76, 'Mi6': 77, 'Fa6': 78, 'Fa#6': 79, 'Sol6': 80, 'Sol#6': 81, 'La6': 82, 'La#6': 83, 'Si6': 84,
        'Do7': 85, 'Do#7': 86, 'Re7': 87, 'Re#7': 88, 'Mi7': 89, 'Fa7': 90, 'Fa#7': 91, 'Sol7': 92, 'Sol#7': 93, 'La7': 94, 'La#7': 95, 'Si7': 96,
        'Do8': 97, 'Do#8': 98, 'Re8': 99, 'Re#8': 100,'Mi8': 101,'Fa8': 102,'Fa#8': 103,'Sol8': 104,'Sol#8': 105,'La8': 106,'La#8': 107,'Si8': 108
    }
    
    converted_notes = []
    for note in notes:
        if note in equivalence_table:
            converted_notes.append(equivalence_table[note])
    return converted_notes

def extract_tempo(file_path):
    mid = mido.MidiFile(file_path)
    for track in mid.tracks:
        for msg in track:
            if msg.type == 'set_tempo':
                tempo = mido.tempo2bpm(msg.tempo)
                return tempo
    return None

def send_notes(notes):

    # Abre la conexión con el puerto serie
    ser = serial.Serial('COM3', 9600)  # Ajusta 'COM3' al puerto correcto de tu Arduino

    # Envía datos a Arduino
    ser.write(notes.encode())

    # Cierra la conexión
    ser.close()

def check_arg():
    # Lee los argumentos de la línea de comandos
    argument = sys.argv[1:]

    if len(argument) != 1:
        print("Error: only 1 song needed")
        sys.exit(1)
    else:
        return argument[0]

# Usage
file_path = check_arg()
notes = midi_to_notes(file_path)
notes_clave_sol = convert_to_clave_de_sol(notes)
print(notes_clave_sol)

notas_numeros = convert_clave_sol_to_numbers(notes_clave_sol)
print(notas_numeros)

tempo = extract_tempo(file_path)

if tempo:
    print(f"El tempo del archivo MIDI es: {tempo} BPM")
else:
    print("No se encontró información de tempo en el archivo MIDI.")
