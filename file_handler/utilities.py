import os

from collections import Counter
from django.conf import settings

FILE_STORAGE = settings.FILE_STORAGE  # Access FILE_STORAGE from settings


def ensure_file_storage_exists():
    """Ensure the FILE_STORAGE directory exists."""

    if not os.path.exists(FILE_STORAGE):
        os.makedirs(FILE_STORAGE)  # Create the directory if it does not exist


# Helper function to read file content
def get_file_content(file_path):
    """
    Reads the content of a file and returns the lines.

    Args:
    file_path (str): Path to the file.

    Returns:
    list: List of lines from the file.
    """
    with open(file_path, 'r') as f:
        lines = f.readlines()
    return lines


# Helper function to check if a file exists
def is_file_exist(file_path):
    """
    Checks if the file exists.

    Args:
    file_path (str): Path to the file.

    Returns:
    bool: True if file exists, False otherwise.
    """
    return os.path.exists(file_path)


def upload(file):
    file_path = os.path.join(FILE_STORAGE, file.name)
    with open(file_path, 'wb+') as destination:
        for chunk in file.chunks():
            destination.write(chunk)
    return file.name


def most_frequent_letter(line):
    """
    Returns the most frequent letter in a string, ignoring spaces and tabs.
    """
    cleaned_line = line.replace(' ', '').replace('\t', '')  # Remove spaces and tabs
    if not cleaned_line:
        return None  # In case the line is empty after removing spaces/tabs
    counter = Counter(cleaned_line)
    most_common_letter, _ = counter.most_common(1)[0]  # Get the most frequent letter
    return most_common_letter
