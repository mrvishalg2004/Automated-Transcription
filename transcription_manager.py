import os
import threading
from faster_whisper import WhisperModel
from file_tracker import FileTracker

class TranscriptionManager:
    def __init__(self):
        # Initialize with a smaller, CPU-friendly model
        self.model = WhisperModel("base", device="cpu", compute_type="int8")
        self.file_tracker = FileTracker()
        self.lock = threading.Lock()

    def transcribe_file(self, file_path):
        """
        Transcribe a single file using Whisper
        """
        if not os.path.exists(file_path):
            return False

        # Update file status to In Progress
        self.file_tracker.update_file_status(file_path, "In Progress")

        try:
            # Perform transcription
            segments, _ = self.model.transcribe(file_path, beam_size=1)

            # Combine all segments
            transcript = " ".join([segment.text for segment in segments])

            # Save transcription
            output_path = file_path + '.txt'
            with open(output_path, 'w', encoding='utf-8') as f:
                f.write(transcript)

            # Update status to Completed
            self.file_tracker.update_file_status(file_path, "Completed")
            return True

        except Exception as e:
            print(f"Error transcribing {file_path}: {str(e)}")
            self.file_tracker.update_file_status(file_path, "Error")
            return False

    def get_transcription_status(self, file_path):
        """
        Get the transcription status of a file
        """
        return self.file_tracker.get_file_status(file_path)