# LineMaster

LineMaster is a Django REST Framework project that provides a web service for file handling and text processing. It allows users to upload text files and perform various operations on the content.

## Features

1. **File Upload**: Upload one or multiple text files to the server.
2. **Random Line**: Retrieve a random line from a specified file.
3. **Random Line Backwards**: Retrieve a random line from a specified file in reverse order.
4. **Longest 100 Lines**: Get the 100 longest lines from all uploaded files.
5. **20 Longest Lines**: Get the 20 longest lines from a specific file.

## Project Structure

The project consists of a Django application called `file_handler`. Key files include:

- `views.py`: Contains the main logic for handling API requests.
- `utilities.py`: Contains helper functions for file operations and text processing.
- `Dockerfile`: Defines the Docker image for the application.
- `docker-compose.yml`: Defines the multi-container Docker application.
- `install_docker_and_memcached.yml`: Ansible playbook for setting up the environment.
- `settings.py`: Contains Django settings, including the mapper for handling different response formats (JSON, XML, plain text).
- `serializers.py`: Defines serializers for structuring API responses.
- `urls.py`: Defines the URL patterns for the application.

## Setup

### Using Docker (Recommended)

1. Clone the repository:
   ```
   git clone <repository-url>
   cd LineMaster
   ```
2. Run the Bash script to prepare your local environment for hosting, bash script will make sure that the docker/docker-compose is installed on you environment, trigger anisble for the installation process, trigger docker-compose for dockerizaiton
   ```
   chmod +x automation_steps.sh
   ./automation_steps.sh
   ```
3. Build and run the Docker containers:
   ```
   docker-compose up --build
   ```

   This will start the Django application and Memcached server.

### Manual Setup

1. Clone the repository:
   ```
   git clone <repository-url>
   cd LineMaster
   ```

2. Run the setup script to install Docker and Memcached:
   ```
   chmod +x automation_steps.sh
   ./automation_steps.sh
   ```

3. Create a virtual environment and activate it:
   ```
   python -m venv venv
   source venv/bin/activate  # On Windows, use `venv\Scripts\activate`
   ```

4. Install the required dependencies:
   ```
   pip install -r requirements.txt
   ```



6. Run migrations:
   ```
   python manage.py migrate
   ```

7. Start the development server:
   ```
   python manage.py runserver
   ```

## API Endpoints

1. **Upload File**
   - URL: `/file/upload/`
   - Method: POST
   - Content-Type: multipart/form-data

2. **Get Random Line**
   - URL: `/file/random-line/<filename>/`
   - Method: GET

3. **Get Random Line Backwards**
   - URL: `/file/random-line-backwards/<filename>/`
   - Method: GET

4. **Get 100 Longest Lines**
   - URL: `/file/longest-100-lines/`
   - Method: GET

5. **Get 20 Longest Lines from a Specific File**
   - URL: `/file/longest-20-lines/<filename>/`
   - Method: GET

## Usage

1. **Uploading a File**:
   Use a POST request to `/file/upload/` with the file in the request body.

2. **Retrieving a Random Line**:
   Send a GET request to `/file/random-line/<filename>/`. The response format (plain text, JSON, or XML) depends on the `Accept` header.

3. **Retrieving a Random Line Backwards**:
   Similar to the random line endpoint, but returns the line in reverse order.

4. **Getting the 100 Longest Lines**:
   Send a GET request to `/file/longest-100-lines/`.

5. **Getting the 20 Longest Lines from a File**:
   Send a GET request to `/file/longest-20-lines/<filename>/`.

## Performance Considerations

- The project uses Memcached for caching to improve performance for operations like retrieving the longest lines.
- File existence checks and content retrieval are handled by utility functions to ensure consistency and reduce code duplication.

## Error Handling

The API includes error handling for scenarios such as:
- File not found
- Empty files
- Invalid requests

## Future Improvements

- Implement user authentication and authorization.
- Add pagination for large result sets.
- Implement more robust error handling and logging.
- Add unit and integration tests for all endpoints.

## Contributing

Contributions to LineMaster are welcome! Please feel free to submit a Pull Request.

