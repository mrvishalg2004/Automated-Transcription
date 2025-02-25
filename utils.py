def get_supported_formats():
    """
    Return list of supported audio/video formats
    """
    return [
        'mp3', 'wav', 'mp4', 'mkv',
        'mov', 'flv', 'aac', 'm4a'
    ]

def format_file_size(size_in_bytes):
    """
    Format file size in human readable format
    """
    for unit in ['B', 'KB', 'MB', 'GB']:
        if size_in_bytes < 1024:
            return f"{size_in_bytes:.2f} {unit}"
        size_in_bytes /= 1024
    return f"{size_in_bytes:.2f} TB"
