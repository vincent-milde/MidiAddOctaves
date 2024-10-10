import mido

# List all available input and output MIDI devices
print("Input devices:", mido.get_input_names())
print("Output devices:", mido.get_output_names())
#
inport_name = '2- Digital Piano-1 0'  # From mido.get_input_names()
outport_name = 'loopMIDI Port 2'  # From mido.get_output_names() or loopMIDI

#open the port
inport = mido.open_input(inport_name)
outport = mido.open_output(outport_name)

def add_octave(msg):
    if msg.type == 'note_on' or msg.type == 'note_off':
        new_note = msg.note + 12
        if new_note > 127:
            new_note = 127
        elif new_note < 0:
            new_note = 0
        return mido.Message(msg.type, note=new_note, velocity=msg.velocity, channel=msg.channel, time=msg.time)
    return msg

print(f"Listening to input on {inport_name}, sending to {outport_name} with octave shift.")

try:
    # Listen for incoming messages
    for msg in inport:
        print(f"Received: {msg}")
        outport.send(msg)  # Send original message
        shifted_msg = add_octave(msg)  # Shift by one octave
        print(f"Sent: {shifted_msg}")
        outport.send(shifted_msg)  # Send shifted message
except KeyboardInterrupt:
    print("Exiting...")
finally:
    inport.close()
    outport.close()
