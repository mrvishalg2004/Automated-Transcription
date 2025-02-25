import os
import json
from utils import get_supported_formats

class FileTracker:
    def __init__(self):
        self.tracked_files = {}
        self.tracking_file = "tracked_files.json"
        self.load_tracking_data()

    def load_tracking_data(self):
        """
        Load tracking data from JSON file
        """
        if os.path.exists(self.tracking_file):
            try:
                with open(self.tracking_file, 'r') as f:
                    self.tracked_files = json.load(f)
            except:
                self.tracked_files = {}

    def save_tracking_data(self):
        """
        Save tracking data to JSON file
        """
        with open(self.tracking_file, 'w') as f:
            json.dump(self.tracked_files, f)

    def add_single_file(self, file_path):
        """
        Add a single file to tracking
        """
        if os.path.exists(file_path):
            self.tracked_files[file_path] = {
                'size': os.path.getsize(file_path),
                'status': 'Pending'
            }
            self.save_tracking_data()

    def update_file_list(self, directory):
        """
        Update the list of files to be tracked
        """
        supported_formats = get_supported_formats()

        for root, _, files in os.walk(directory):
            for file in files:
                if any(file.lower().endswith(fmt) for fmt in supported_formats):
                    file_path = os.path.join(root, file)

                    # Add new file or update existing
                    if file_path not in self.tracked_files:
                        self.tracked_files[file_path] = {
                            'size': os.path.getsize(file_path),
                            'status': 'Pending'
                        }

        self.save_tracking_data()

    def update_file_status(self, file_path, status):
        """
        Update the status of a file
        """
        if file_path in self.tracked_files:
            self.tracked_files[file_path]['status'] = status
            self.save_tracking_data()

    def get_file_status(self, file_path):
        """
        Get the status of a file
        """
        return self.tracked_files.get(file_path, {}).get('status', 'Pending')

    def get_all_files(self):
        """
        Get all tracked files
        """
        return self.tracked_files