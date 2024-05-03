# Commender

## Description

This project leverages FastAPI to expose several system and network utilities through a web interface. It provides endpoints for executing system commands, managing files and processes, and handling network interactions.

## Installation

To install the necessary dependencies, run:

```bash
pip install -r requirements.txt
```

## Usage

### Starting the Server

Run one of the following commands to start the server:

```bash
uvicorn app:app
```

```bash
uvicorn app:app --host 0.0.0.0 --port 8000
```

```bash
fastapi run
```

This will start a local server, typically accessible via `http://127.0.0.1:8000`.

Uvicorn and others support a --reload option that is useful during development. The --reload option consumes much more resources, is more unstable, etc. It helps a lot during development, but you shouldn't use it in production. Check the official [FastAPI documentation](https://fastapi.tiangolo.com/deployment/manually/) for more details.


### Available Endpoints

- **/command/**: Run specified system command.
- **/info/{password}**: Get system information such as IP, OS details, RAM, and CPU usage.
- **/reboot/**: Reboot the system.
- **/restart_app/{password}/{process_name}**: Restart a specified application.
- **/update**: Update the application by pulling the latest changes from the master branch in Git.

### Example

To fetch system information, you can use:

```http
GET /info/{password}
```

## Modules

### `app.py`

Main FastAPI application setup and route definitions .

### `paths.py`

Defines the paths used across the application for logging and file management .

### `logger_module.py`

Configures logging for the application, including file and console handlers .

### `network_tools.py`

Contains functions for network operations like sending/receiving files via SSH, IP management, and executing commands on remote machines .

### `tools.py`

Utility functions for file management, process handling, and system information retrieval .

## License

This project is licensed under the [LICENSE](LICENSE).

## Contributing

Contributions to this project are welcome. Please ensure to update tests as appropriate.

## Acknowledgements

Thanks to all the contributors who have invested their time in improving this project.

---

Ensure all paths and placeholders are adjusted as per your actual setup. This README is designed to give a clear overview of your application's structure and usage.
