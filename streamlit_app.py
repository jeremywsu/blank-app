import streamlit as st
from music21 import converter, instrument, note, stream

# Define a Node for the linked list with a counter
class Node:
    def __init__(self, data):
        self.data = data  # The drum pad being played (MIDI pitch)
        self.count = 1  # Counter to track the number of times this note repeats
        self.next = None  # Pointer to the next node

# Define a LinkedList for the measure
class LinkedList:
    def __init__(self):
        self.head = None  # Start of the linked list
    
    def append(self, data):
        """Add a node to the end of the linked list, allowing duplicates and tracking the count."""
        print(f"Appending data: {data}")  # Debug print
        new_node = Node(data)
        
        if not self.head:  # If the list is empty
            self.head = new_node
            print(f"Head node created with data: {data}")  # Debug print
        else:
            current = self.head
            found = False
            while current:  # Traverse the list to check for duplicates
                print(f"Traversing node with data: {current.data} (count: {current.count})")  # Debug print
                if current.data == data:  # If the note already exists, increment the count
                    current.count += 1
                    print(f"Found duplicate note {data}. Incrementing count to {current.count}")  # Debug print
                    found = True
                    break
                if not current.next:  # If we reach the end of the list
                    break
                current = current.next

            if not found:  # If the note wasn't found, add a new node
                current.next = new_node
                print(f"New node added with data: {data}")  # Debug print
    
    def print_list(self):
        """Print the entire linked list with drum names and counts."""
        current = self.head
        nodes = []
        while current:
            drum_name = self.get_drum_name(current.data)
            nodes.append(f"{drum_name} ({current.data}) x{current.count}")
            current = current.next
        print(f"Linked List: {' -> '.join(nodes)}")
    
    def __str__(self):
        """Return a string representation of the linked list with drum names and counts."""
        nodes = []
        current = self.head
        while current:
            drum_name = self.get_drum_name(current.data)
            nodes.append(f"{drum_name} ({current.data}) x{current.count}")
            current = current.next
        return " -> ".join(nodes)
    
    def get_drum_name(self, midi_pitch):
        """Return the name of the drum for a given MIDI pitch."""
        drum_map = {
            36: "Bass Drum 1",
            37: "Bass Drum 2",
            38: "Snare Drum 1",
            39: "Snare Drum 2",
            40: "Tom-Tom 1",
            41: "Tom-Tom 2",
            42: "Hi-hat Closed",
            43: "Hi-hat Pedal",
            44: "Hi-hat Open",
            45: "Crash Cymbal 1",
            46: "Crash Cymbal 2",
            47: "Ride Cymbal 1",
            48: "Ride Cymbal 2",
            # Add more drum mappings as needed
        }
        return drum_map.get(midi_pitch, f"Unknown ({midi_pitch})")

def extract_drum_tracks(score):
    """Extract drum tracks and return a list of linked lists for measures."""
    drum_tracks = []
    for part in score.parts:
        print(f"Checking part: {part.partName}")  # Debug print
        # Check if the part is a drum/percussion part
        if part.getInstrument(returnDefault=True).percussion:
            print(f"Drum part detected: {part.partName}")  # Debug print
            drum_tracks.append(part)
    
    measures_data = []
    for drum_part in drum_tracks:
        print(f"Processing drum part: {drum_part.partName}")  # Debug print
        for measure in drum_part.measures(1, None):  # Iterate through all measures
            print(f"Processing measure: {measure}")  # Debug print
            measure_ll = LinkedList()
            for n in measure.notes:
                print(f"Processing note: {n}")  # Debug print
                if isinstance(n, note.Note):
                    pitch = n.pitch.midi  # Get MIDI pitch of the drum
                    print(f"Note is a drum pad with MIDI pitch: {pitch}")  # Debug print
                    measure_ll.append(pitch)
            measures_data.append(measure_ll)
            print(f"Linked list created for measure: {measure_ll}")  # Debug print
    return measures_data

def display_drum_measures_linked_lists(measures_data):
    """Formats and displays measures as linked lists."""
    for i, measure_ll in enumerate(measures_data, start=1):
        print(f"Displaying measure {i}: {measure_ll}")  # Debug print
        st.write(f"**Measure {i}:** {measure_ll}")

# Streamlit App
st.title("MusicXML Drum Track Analyzer with Linked Lists and Duplicate Counting")
st.write("Upload a MusicXML file to analyze drum tracks and display each measure as a linked list with note counts.")

uploaded_file = st.file_uploader("Upload MusicXML File", type=["musicxml", "xml"])

if uploaded_file:
    # Parse MusicXML files
    st.write("Processing file...")
    print("Uploading MusicXML file...")  # Debug print
    score = converter.parse(uploaded_file)
    print("MusicXML file parsed successfully.")  # Debug print
    
    # Extract drum tracks and their measures as linked lists
    drum_measures = extract_drum_tracks(score)
    print("Drum tracks and measures extracted.")  # Debug print
    
    # Display results
    if drum_measures:
        st.write("### Drum Track Measures as Linked Lists:")
        display_drum_measures_linked_lists(drum_measures)
        
        # Print each linked list to the console with drum names and counts
        print("\n=== Final Linked Lists for Each Measure ===")
        for i, measure_ll in enumerate(drum_measures, start=1):
            print(f"Measure {i}:")
            measure_ll.print_list()
    else:
        print("No drum tracks found in the uploaded file.")  # Debug print
        st.write("No drum tracks found in the uploaded file.")