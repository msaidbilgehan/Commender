from typing import Any
from fastapi import FastAPI, Request

from Libraries.logger_module import logger
from Libraries.network_tools import get_local_IP
from Libraries.tools import command_run, find_parent_pid_by_name, get_cpu_ram_info, get_gpu_info, get_os_info



app = FastAPI()

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
        parse=False
    )
    logger.info(f"command_result: {command_result}")

    response_temp["status"] = "SUCCESS"
    response_temp["message"] = command_result
    return response_temp


@app.get("/reboot/")
async def reboot_endpoint(info: Request):
    logger.info(
        f"reboot_endpoint Parameters -> info: {info}"
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

    command = "reboot -h now"
    password = req_info.get("pass", "")

    if password == "":
        response_temp["status"] = "ERROR"
        response_temp["message"] = "No password provided"
        return response_temp

    command_result = command_run(
        command=command,
        sudo_password=password,
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
    find_parent_pid_by_name()
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

    logger.info(
        f"info -> IP: {info_local_ip} | OS: {info_os} | RAM/CPU: {info_ram_cpu} | GPU: {info_gpu}")

    response_temp["status"] = "SUCCESS"
    response_temp["message"] = "200"
    response_temp["info_local_ip"] = info_local_ip
    response_temp["info_os"] = info_os
    response_temp["info_ram_cpu"] = info_ram_cpu
    response_temp["info_gpu"] = info_gpu
    return response_temp
