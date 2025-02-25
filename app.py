import streamlit as st
import os
import tempfile
from transcription_manager import TranscriptionManager
from file_tracker import FileTracker
from utils import get_supported_formats, format_file_size

st.set_page_config(page_title="Audio/Video Transcription System",
                   page_icon="🎙️",
                   layout="wide")

# Initialize session state
if 'transcription_manager' not in st.session_state:
    st.session_state.transcription_manager = TranscriptionManager()
if 'file_tracker' not in st.session_state:
    st.session_state.file_tracker = FileTracker()
if 'selected_directory' not in st.session_state:
    st.session_state.selected_directory = None
if 'temp_dir' not in st.session_state:
    st.session_state.temp_dir = tempfile.mkdtemp()

# UI Components
st.title("🎙️ Audio/Video Transcription System")

# Sidebar
with st.sidebar:
    st.header("Upload or Select Directory")

    # File Upload
    supported_formats = get_supported_formats()
    format_str = ", ".join(["." + fmt for fmt in supported_formats])
    uploaded_file = st.file_uploader("Upload Audio/Video File",
                                     type=supported_formats,
                                     help=f"Supported formats: {format_str}")

    if uploaded_file:
        with st.spinner('Saving uploaded file...'):
            # Save uploaded file to temp directory
            temp_path = os.path.join(st.session_state.temp_dir,
                                     uploaded_file.name)
            with open(temp_path, "wb") as f:
                f.write(uploaded_file.getbuffer())

            # Add to tracker and start transcription
            st.session_state.file_tracker.add_single_file(temp_path)
            st.success(f"File uploaded: {uploaded_file.name}")

            # Start transcription automatically
            with st.spinner('Starting transcription...'):
                st.session_state.transcription_manager.transcribe_file(
                    temp_path)
                st.rerun()

    st.divider()

    # Directory input
    st.subheader("Or Choose Directory")
    directory = st.text_input("Enter Directory Path",
                              value=st.session_state.selected_directory
                              if st.session_state.selected_directory else "")

    if directory and os.path.isdir(directory):
        st.session_state.selected_directory = directory
        if st.button("Scan Directory"):
            st.session_state.file_tracker.update_file_list(directory)
            st.success("Directory scanned successfully!")
    elif directory:
        st.error("Please enter a valid directory path")

    # Manual refresh button
    if st.button("Refresh Status"):
        st.rerun()

# Main content
files = st.session_state.file_tracker.get_all_files()

if files:
    col1, col2 = st.columns([2, 1])

    with col1:
        st.subheader("Files")

        for file_path, file_info in files.items():
            with st.expander(os.path.basename(file_path)):
                col_a, col_b, col_c = st.columns([2, 1, 1])
                with col_a:
                    st.text(f"Size: {format_file_size(file_info['size'])}")
                with col_b:
                    status = file_info.get('status', 'Pending')
                    if status == 'Completed':
                        st.success('Completed')
                    elif status == 'In Progress':
                        st.info('In Progress')
                    elif status == 'Error':
                        st.error('Error')
                    else:
                        st.warning('Pending')
                with col_c:
                    if status != 'Completed' and status != 'In Progress':
                        if st.button('Transcribe', key=file_path):
                            with st.spinner('Starting transcription...'):
                                st.session_state.transcription_manager.transcribe_file(
                                    file_path)
                                st.rerun()

                if status == 'Completed':
                    transcript_path = file_path + '.txt'
                    if os.path.exists(transcript_path):
                        with open(transcript_path, 'r', encoding='utf-8') as f:
                            st.text_area("Transcript", f.read(), height=100)

    with col2:
        st.subheader("Statistics")
        total = len(files)
        completed = len(
            [f for f in files.values() if f.get('status') == 'Completed'])
        in_progress = len(
            [f for f in files.values() if f.get('status') == 'In Progress'])
        pending = total - completed - in_progress

        st.metric("Total Files", total)
        st.metric("Completed", completed)
        st.metric("In Progress", in_progress)
        st.metric("Pending", pending)

else:
    st.info("Upload a file or select a directory to begin transcription")

# Footer
st.markdown("---")
#st.markdown("Made with ❤️ using Streamlit and Faster Whisper")
