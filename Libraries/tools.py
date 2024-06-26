from datetime import datetime
import os
import platform
import time
import shutil
import zipfile
import random
import string
import subprocess
from typing import Union
from stat import S_ISDIR

import psutil
import GPUtil


def kill_process_by_name(name):
    # Iterate over all running processes
    response = []
    for proc in psutil.process_iter(['pid', 'name']):
        print("> proc: ", proc.info['name'])
        # Check if process name matches the target name
        if proc.info['name'] == name:
            try:
                proc.kill()  # Kill the process
                response.append(f"Process {proc.info['pid']} ({name}) killed.")
            except psutil.NoSuchProcess:
                response.append(f"No such process with name {proc.info['pid']} ({name}.")
            except psutil.AccessDenied:
                response.append(f"Access denied when trying to kill the process {proc.info['pid']} ({name}.")
    return response

def find_parent_pid_by_name(process_name):
    # List to hold parent PIDs
    parent_pids = []
    # Iterate over all running processes
    for proc in psutil.process_iter(['pid', 'name', 'ppid']):
        try:
            # Check if the process name matches the target name
            if proc.info['name'] == process_name:
                parent_pid = proc.info['ppid']
                parent_pids.append((proc.info['pid'], parent_pid))
        except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
            # Process has been terminated or access is denied
            continue

    return parent_pids


def get_gpu_info():
    gpus = GPUtil.getGPUs()
    gpu_info = []
    for gpu in gpus:
        info = {
            'GPU ID': gpu.id,
            'Load (%)': gpu.load * 100,
            'Memory Used (MB)': gpu.memoryUsed,
            'Memory Total (MB)': gpu.memoryTotal,
            'Memory Utilization (%)': gpu.memoryUtil * 100,
            'Temperature (C)': gpu.temperature
        }
        gpu_info.append(info)
    return gpu_info

def get_cpu_ram_info():
    cpu_usage = psutil.cpu_percent(interval=1)
    ram_usage = psutil.virtual_memory().percent
    return {
        'cpu': cpu_usage,
        'ram': ram_usage
    }


# Get OS and kernel information
def get_os_info():
    info = {
        'system': platform.system(),
        'node': platform.node(),
        'release': platform.release(),
        'version': platform.version(),
        'machine': platform.machine(),
        'processor': platform.processor()
    }
    return info


# Get detailed platform info
def get_platform_info():
    uname = platform.uname()
    return {
        'system': uname.system,
        'node': uname.node,
        'release': uname.release,
        'version': uname.version,
        'machine': uname.machine,
        'processor': uname.processor
    }


# Using the os module for environment details
def get_env_info():
    env_info = {
        'os_environment_variables': dict(os.environ),
        'current_working_directory': os.getcwd(),
        'current_user': os.getlogin()
    }
    return env_info


def isdir(st_mode):
    try:
        return S_ISDIR(st_mode)
    except IOError:
        # Path does not exist, so by definition not a directory
        return False


def command_run(
    command: Union[list[str], str],
    parse: bool = True,
    sudo_password: str = ""
) -> Union[subprocess.CompletedProcess[str], str]:
    if parse:
        if isinstance(command, str):
            command = command.split()
        elif not isinstance(command, list):
            raise ValueError("Command must be a list or a string.")

    if sudo_password:
        # Prepare the command string if a sudo password is provided
        command = ['sudo', '-S'] + command
        # Use Popen to securely input sudo password and run the command
        process = subprocess.Popen(
            command,
            stdin=subprocess.PIPE,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True
        )
        # Send sudo password followed by a newline to simulate Enter key
        stdout, stderr = process.communicate(input=f"{sudo_password}\n")
        if process.returncode != 0:
            return f"Command '{' '.join(command)}' failed with exit status {process.returncode}: {stderr}"
        else:
            return stdout
    else:
        # Run the command without sudo password
        try:
            command_response = subprocess.run(
                command,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True,
                check=True
            )
            return command_response.stdout
        except subprocess.CalledProcessError as error:
            return f"Command '{' '.join(command)}' failed with exit status {error.returncode}: {error.stderr}"
        except Exception as error:
            return f"Error Occurred '{' '.join(command)}': {error}"


def read_log_file(path, wait_thread=None):
    with open(path, 'r') as file:
        while True:
            line = file.readline().strip()
            if line:
                # print(line)
                yield f"data: {line}\n\n"  # Format for SSE (data: at the start and 2 new line characters at the end)

            time.sleep(1)  # Wait for new content

            if wait_thread is not None:
                if not wait_thread.is_alive():
                    break


def get_directory_info(directory_path, round_in_gb=3):
    if os.path.exists(directory_path) == False:
        return []
    # Belirtilen dizindeki tüm klasörleri listeleyelim
    all_items = os.listdir(directory_path)
    dirs = [item for item in all_items if os.path.isdir(os.path.join(directory_path, item))]

    dir_info = []

    for dir_name in dirs:
        full_path = os.path.join(directory_path, dir_name)

        # Klasörün boyutunu hesaplayalım (alt klasörler ve dosyalar dahil)
        total_size = 0
        for dirpath, dirnames, filenames in os.walk(full_path):
            for f in filenames:
                fp = os.path.join(dirpath, f)
                total_size += os.path.getsize(fp)
        total_size = round(total_size * 10**-9, round_in_gb)

        # Oluşturma tarihini alalım
        creation_timestamp = os.path.getctime(full_path)
        creation_date = datetime.fromtimestamp(creation_timestamp).strftime('%Y-%m-%d %H:%M:%S')

        dir_info.append({
            'name': dir_name,
            'size': total_size,
            'creation_date': creation_date
        })

    # Klasör bilgilerini tarih bilgisine göre sıralayalım
    sorted_dir_info = sorted(dir_info, key=lambda x: x['creation_date'], reverse=True)

    return sorted_dir_info



def list_dir(path):
    return os.listdir(path)


def delete_folder(path):
    response = "Deleted"

    if os.path.exists(path):
        try:
            shutil.rmtree(path)
        except OSError as e:
            response = f"Can not delete folder: {e.filename} - {e.strerror}."
    else:
        response = "No Log Collection Folder Found!"

    return response


def archive_directory(directory_to_compress:str, output_directory:str, archive_name:str, delete_exist:bool=True):
    output_archive_path = os.path.join(output_directory, archive_name)
    if delete_exist and os.path.exists(output_archive_path + ".zip"):
        os.remove(output_archive_path + ".zip")

    # print(f"Creating ZIP File: {output_archive_path}.zip to compress {directory_to_compress}")
    return shutil.make_archive(
        base_name=output_archive_path,
        format='zip',
        root_dir=directory_to_compress
    )


def archive_files(files:list[str], output_archive_path:str, delete_exist:bool=True):
    if delete_exist and os.path.exists(output_archive_path):
        os.remove(output_archive_path)

    # print(f"Creating ZIP File: {output_archive_path}")

    # Create ZIP
    with zipfile.ZipFile(output_archive_path, 'w') as zipper:
        for file in files:
            # print(f"Adding File: {file}")
            file_name_only = os.path.basename(file)
            zipper.write(file, arcname=file_name_only)

    # print(f"ZIP File Created: {output_archive_path}")
    return output_archive_path


def generate_unique_id(length:int=8, is_upper: bool=True) -> str:
    """Generate a random unique ID using alphabet and numbers."""
    if is_upper:
        ascii_letters = string.ascii_letters.upper()
    else:
        ascii_letters = string.ascii_letters
    characters = ascii_letters + string.digits  # Merge letters and digits
    unique_id = ''.join(random.choice(characters) for i in range(length))
    return unique_id