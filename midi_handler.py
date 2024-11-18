# midi_handler.py
import mido
import threading

# Global variables for the MIDI ports and listening thread
inport = None
outport = None
listening_thread = None
running = False  # Flag to control the thread

def add_octave(msg):
    """Shift note up by one octave."""
    if msg.type == 'note_on' or msg.type == 'note_off':
        new_note = msg.note + 12
        if new_note > 127:
            new_note = 127
        elif new_note < 0:
            new_note = 0
        return mido.Message(msg.type, note=new_note, velocity=msg.velocity, channel=msg.channel, time=msg.time)
    return msg

def open_ports(input_port_name, output_port_name):
    """Open the specified input and output ports."""
    global inport, outport, running
    try:
        inport = mido.open_input(input_port_name)
        outport = mido.open_output(output_port_name)
        print(f"Listening on {input_port_name}, sending to {output_port_name} with octave shift.")
        running = True  # Set running flag to True
        return True
    except Exception as e:
        print(f"Failed to open ports: {e}")
        return False

def close_ports():
    """Close the MIDI ports and stop the listening thread."""
    global inport, outport, running
    running = False
    if inport:
        inport.close()
    if outport:
        outport.close()
    print("Ports closed.")

def listen_to_midi():
    """Listen for incoming MIDI messages and apply octave shift."""
    global inport, outport, running
    while running:
        try:
            for msg in inport:
                if not running:  # Stop listening if the flag is set to False
                    break
                print(f"Received: {msg}")
                outport.send(msg)  # Send original message
                shifted_msg = add_octave(msg)  # Shift by one octave
                print(f"Sent: {shifted_msg}")
                outport.send(shifted_msg)  # Send shifted message
        except Exception as e:
            print("Error in MIDI listening:", e)
            break
    close_ports()

def start_listening():
    """Start the listening thread."""
    global listening_thread
    listening_thread = threading.Thread(target=listen_to_midi, daemon=True)
    listening_thread.start()
