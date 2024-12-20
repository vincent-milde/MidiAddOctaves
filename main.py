import tkinter as tk
import ttkbootstrap as ttk
import midi_handler  # Import the MIDI handler module
import mido

# Window setup
window = ttk.Window(themename='darkly')
window.title('MidiAddOctaves')
window.geometry('500x400')

# Title
title_label = ttk.Label(master=window, text='Midi To Octaves', font='Calibri 18 bold')
title_label.pack(pady=10)

# List of ports
portsIn = mido.get_input_names()
portsOut = mido.get_output_names()

# Variables to store selected ports
selected_portIn = tk.StringVar()
selected_portOut = tk.StringVar()

#Comboboxes
input_frame = ttk.Frame(master = window)
output_frame = ttk.Frame(master=window)

#Refresher function
def refresher():
    input_combo["values"] = mido.get_input_names()
    output_combo["values"] = mido.get_output_names()
# Create a Combobox for selecting the input port
input_label = ttk.Label(master= input_frame, text="MIDI Input", font='Calibri 12')
input_label.pack(pady=5)
input_combo = ttk.Combobox(master=input_frame, textvariable=selected_portIn, values=portsIn, state="readonly")
input_combo.set("Select Input Port")  # Placeholder text
refresh_input_button = ttk.Button(master = input_frame, text= "Refresh", command=refresher)
input_combo.pack(side=tk.LEFT, padx=5)
refresh_input_button.pack(side=tk.LEFT)
input_frame.pack(pady=5)

    
# Create a Combobox for selecting the output port
output_label = ttk.Label(master=output_frame, text="MIDI Output", font='Calibri 12')
output_label.pack(pady=5)
output_combo = ttk.Combobox(master=output_frame, textvariable=selected_portOut, values=portsOut, state="readonly")
output_combo.set("Select Output Port")  # Placeholder text
refresh_output_button = ttk.Button(master = output_frame, text= "Refresh", command=refresher)
output_combo.pack(side=tk.LEFT, padx=5)
refresh_output_button.pack(side=tk.LEFT)
output_frame.pack(pady=5)
# Button to confirm the selection and start the MIDI connection
def connect_midi():
    input_port_name = selected_portIn.get()
    output_port_name = selected_portOut.get()
    
    if midi_handler.open_ports(input_port_name, output_port_name):
        print("Ports opened successfully")
        midi_handler.start_listening()  # Start the listening thread

def disconnect_midi():
    midi_handler.close_ports()  # Close the ports and stop listening
# Connect and Disconnect buttons
connect_button = ttk.Button(window, text="Connect", command=connect_midi)
connect_button.pack(pady=10)

disconnect_button = ttk.Button(window, text="Disconnect", command=disconnect_midi)
disconnect_button.pack(pady=5)

#Label
credit = ttk.Label(master=window, text='Megumin :), BOOOOOO!', font='Euphemia 4')
credit.pack(side=tk.LEFT, padx=(20, 0), pady=20)
# Run the application
window.mainloop()