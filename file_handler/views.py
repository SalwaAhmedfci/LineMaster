from rest_framework.response import Response
from rest_framework.decorators import api_view
from urllib.parse import unquote
import os
import random
from django.conf import settings
from django.core.cache import cache
from .utilities import (
    upload,
    is_file_exist,
    get_file_content,
    most_frequent_letter,
    ensure_file_storage_exists
)

from .serializers import LineDataSerializer

FILE_STORAGE = settings.FILE_STORAGE  # Access FILE_STORAGE from settings
# Ensure the FILE_STORAGE directory exists
ensure_file_storage_exists()

@api_view(['POST'])
def upload_files(request):
    """
    Upload multiple files to the server.

    This function handles file uploads via HTTP POST, stores the files in the FILE_STORAGE directory,
    and returns a success or error response for each file.

    Args:
    request: The HTTP request object containing the files.

    Returns:
    Response: A JSON response indicating the success or failure of the upload for each file.
    """
    # Check if any files were uploaded
    if not request.FILES:
        return Response({"error": "No files provided"}, status=400)

    responses = []  # List to store individual file upload responses

    # Iterate over the uploaded files
    for file in request.FILES.getlist('file'):  # getlist() to handle multiple files
        try:
            upload(file)
        # Add a success response for this file
            responses.append(
                {"file": file.name, "status": "uploaded", "message": f"File '{file.name}' uploaded successfully"})
        except Exception as e:
            # Add an error response if something went wrong
            responses.append({"file": file.name, "status": "error", "message": str(e)})

    return Response({"results": responses}, status=201)





@api_view(['GET'])
def random_line(request, filename):
    """
    Returns a random line from the specified file, with additional metadata.

    Args:
    filename (str): The name of the file to read from.

    Returns:
    Response: Random line from the file with metadata in the requested format (JSON, XML, plain text).
    :param filename:
    :param request:
    """
    decoded_filename = unquote(filename)
    file_path = os.path.join(FILE_STORAGE, decoded_filename)

    if not is_file_exist(file_path):
        return Response({"error": "File not found"}, status=404)

    lines = get_file_content(file_path)

    if not lines:
        return Response({"error": "File is empty"}, status=400)

    random_index = random.randint(0, len(lines) - 1)  # Get a random line index
    random_line = lines[random_index].strip()  # Remove leading/trailing spaces
    most_frequent_char = most_frequent_letter(random_line)  # Get the most frequent letter

    response_data = {
        "line_number": random_index + 1,  # Line number (1-based)
        "file_name": decoded_filename,
        "random_line": random_line,
        "most_frequent_char": most_frequent_char
    }
    # Serialize the data using LineDataSerializer
    serializer = LineDataSerializer(response_data)

    if request.META.get('HTTP_ACCEPT') == 'text/plain':
        return Response(response_data['random_line'])
    return Response(serializer.data)  # The correct renderer will automatically format the response


@api_view(['GET'])
def random_line_backwards(request, filename):
    """
    Returns a random line from the specified file, but reversed, with additional metadata.

    Args:
    filename (str): The name of the file to read from.

    Returns:
    Response: Reversed random line from the file with metadata in the requested format (JSON, XML, plain text).
    :param filename:
    :param request:
    """
    decoded_filename = unquote(filename)
    file_path = os.path.join(FILE_STORAGE, decoded_filename)

    if not is_file_exist(file_path):
        return Response({"error": "File not found"}, status=404)

    lines = get_file_content(file_path)

    if not lines:
        return Response({"error": "File is empty"}, status=400)

    random_index = random.randint(0, len(lines) - 1)
    random_line = lines[random_index].strip()[::-1]  # Reverse the line and strip spaces
    most_frequent_char = most_frequent_letter(random_line)  # Get the most frequent letter

    response_data = {
        "line_number": random_index + 1,
        "file_name": decoded_filename,
        "random_line": random_line,
        "most_frequent_char": most_frequent_char
    }
    # Serialize the data using LineDataSerializer
    serializer = LineDataSerializer(response_data)

    if request.META.get('HTTP_ACCEPT') == 'text/plain':
        return Response(response_data['random_line'])
    return Response(serializer.data)  # The correct renderer will automatically format the response


@api_view(['GET'])
def longest_100_lines(request):
    """
    Returns the 100 longest lines from all uploaded files.
    """
    cache_key = 'longest_100_lines'  # Cache key for the longest lines
    longest_lines = ''
    # Check if the result is cached
    cached_lines = cache.get(cache_key)
    if cached_lines:
        longest_lines = cached_lines
    else:

        all_lines = []

        # Read all lines from all files
        for file_name in os.listdir(settings.FILE_STORAGE):
            file_path = os.path.join(settings.FILE_STORAGE, file_name)
            if is_file_exist(file_path):  # Ensure the file exists
                lines = get_file_content(file_path)  # Use utility to get file content
                all_lines.extend(lines)

        # Sort the lines by length and select the longest 100
        longest_lines = sorted(all_lines, key=len, reverse=True)[:100]

        # Cache the result
        cache.set(cache_key, longest_lines)

    if request.META.get('HTTP_ACCEPT') == 'text/plain':
        return Response("\n".join(longest_lines))

    return Response(longest_lines)

@api_view(['GET'])
def longest_20_lines(request, filename):
    """
    Returns the 20 longest lines from a specific file.
    """
    cache_key = f'longest_20_lines:{filename}'  # Cache key for the longest lines from a specific file
    longest_lines = ''
    # Check if the result is cached
    cached_lines = cache.get(cache_key)
    if cached_lines:
        longest_lines = cached_lines
    else:
        file_path = os.path.join(FILE_STORAGE, filename)

        if not is_file_exist(file_path):  # Use utility function to check file existence
            return Response({"error": f"File '{filename}' not found"}, status=404)

        lines = get_file_content(file_path)  # Use utility to get file content
        if not lines:
            return Response({"error": "File is empty"}, status=400)

        # Sort the lines by length and select the longest 20
        longest_lines = sorted(lines, key=len, reverse=True)[:20]

        # Cache the result
        cache.set(cache_key, longest_lines)

    if request.META.get('HTTP_ACCEPT') == 'text/plain':
        return Response("\n".join(longest_lines))

    return Response(longest_lines)