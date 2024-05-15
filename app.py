from typing import Any
from fastapi import FastAPI, Request

from Libraries.logger_module import logger
from Libraries.network_tools import get_local_IP
from Libraries.tools import command_run, get_cpu_ram_info, get_gpu_info, get_os_info, kill_process_by_name



app = FastAPI(
    title="Commender App",
    description="Commender App to command the device",
    version="0.1.0"
)

RESPONSE_STRUCTURE: dict[str, Any] = {
    "status": "",
    "message": "",
}



@app.get("/")
def index():
    return RESPONSE_STRUCTURE


@app.get("/command/")
async def command_runner_endpoint(info: Request):
    logger.info(
        f"command_runner_endpoint Parameters -> info: {info}"
    )
    response_temp = RESPONSE_STRUCTURE.copy()

    try:
        req_info = await info.json()
    except Exception as error:
        logger.error(error)
        response_temp["status"] = "ERROR"
        response_temp["message"] = "Invalid JSON"
        return response_temp

    logger.info(f"req_info: {req_info}")

    command = req_info.get("command", "")
    password = req_info.get("pass", "")
    is_sudo = req_info.get("sudo", False)

    if password == "" or command == "":
        response_temp["status"] = "ERROR"
        response_temp["message"] = "No password or command provided"
        return response_temp

    if not is_sudo:
        password = ""

    command_result = command_run(
        command=command,
        sudo_password=password,
        parse=True
    )
    logger.info(f"command_result: {command_result}")

    response_temp["status"] = "SUCCESS"
    response_temp["message"] = command_result
    return response_temp


@app.get("/command/{password}/{command}/{is_sudo}")
async def command_runner_parameter_endpoint(command: str, password: str, is_sudo: bool = False):
    logger.info(
        f"command_runner_parameter_endpoint Parameters -> command: {command} | password: {password} | is_sudo: {is_sudo}"
    )
    response_temp = RESPONSE_STRUCTURE.copy()

    if password == "" or command == "":
        response_temp["status"] = "ERROR"
        response_temp["message"] = "No password or command provided"
        return response_temp

    if not is_sudo:
        password = ""

    command_result = command_run(
        command=command,
        sudo_password=password,
        parse=True
    )
    logger.info(f"command_result: {command_result}")

    response_temp["status"] = "SUCCESS"
    response_temp["message"] = command_result
    return response_temp


@app.get("/reboot")
async def reboot_endpoint():
# async def reboot_endpoint(info: Request):
    # logger.info(
    #     f"reboot_endpoint Parameters -> info: {info}"
    # )
    logger.info(
        f"reboot_endpoint called"
    )
    response_temp = RESPONSE_STRUCTURE.copy()

    # try:
    #     req_info = await info.json()
    # except Exception as error:
    #     logger.error(error)

    #     response_temp["status"] = "ERROR"
    #     response_temp["message"] = "Invalid JSON"
    #     return response_temp

    # logger.info(f"req_info: {req_info}")

    command = "reboot -h now"
    # password = req_info.get("pass", "")
    password = "sktek_1"

    # if password == "":
    #     response_temp["status"] = "ERROR"
    #     response_temp["message"] = "No password provided"
    #     return response_temp

    command_result = command_run(
        command=command,
        sudo_password=password,
        parse=True
    )
    logger.info(f"reboot_endpoint command_result: {command_result}")

    response_temp["status"] = "SUCCESS"
    response_temp["message"] = command_result
    return response_temp


@app.get("/info/{password}")
async def info_endpoint(password: str):

    logger.info(
        f"info_endpoint Parameters -> password: {password}"
    )
    response_temp = RESPONSE_STRUCTURE.copy()

    if password == "":
        response_temp["status"] = "ERROR"
        response_temp["message"] = "No password provided"
        return response_temp

    info_local_ip = get_local_IP()
    info_os = get_os_info()
    info_ram_cpu = get_cpu_ram_info()
    info_gpu = get_gpu_info()


    logger.info(f"info -> IP: {info_local_ip} | OS: {info_os} | RAM/CPU: {info_ram_cpu} | GPU: {info_gpu}")

    response_temp["status"] = "SUCCESS"
    response_temp["message"] = "200"
    response_temp["info_local_ip"] = info_local_ip
    response_temp["info_os"] = info_os
    response_temp["info_ram_cpu"] = info_ram_cpu
    response_temp["info_gpu"] = info_gpu
    return response_temp


@app.get("/restart_app/{password}/{process_name}")
async def restart_app(password: str, process_name: str):
    logger.info(
        f"info_endpoint Parameters -> password: {password} | process_name: {process_name}"
    )
    response_temp = RESPONSE_STRUCTURE.copy()

    if process_name == "":
        response_temp["status"] = "ERROR"
        response_temp["message"] = "No process name provided"
        return response_temp

    # parent_pid = find_parent_pid_by_name(process_name)
    # logger.info(f"parent_pid: {parent_pid}")
    response_command = kill_process_by_name(process_name)
    logger.info(f"response_command: {response_command}")

    response_temp["status"] = "SUCCESS"
    response_temp["message"] = response_command
    return response_temp


@app.get("/update")
async def update():
    command = "git pull origin master"

    logger.info(
        f"update called -> command: {command}"
    )
    response_temp = RESPONSE_STRUCTURE.copy()

    command_result = command_run(
        command=command,
        parse=True
    )

    response_temp["status"] = "SUCCESS"
    response_temp["message"] = command_result
    return response_temp

if __name__ == '__main__':
    import uvicorn
    import sys

    if len(sys.argv) < 2:
        print("Please provide the host (such as 0.0.0.0) and the port (such as 8000) as an argument")
        print("Example: python app.py 0.0.0.0 8000")
        print("Using default parameters;")
        print("\t |> Host: 0.0.0.0")
        print("\t |> Port: 8000")
        host = "0.0.0.0"
        port = 8000
    else:
        host = sys.argv[1]
        port = int(sys.argv[2])
        print("Using parameters;")
        print(f"\t |> Host: {host}")
        print(f"\t |> Port: {port}")

    uvicorn.run(app, port=port, host=host)
