from typing import Union

from fastapi import FastAPI, Request

from Libraries.logger_module import logger
from Libraries.tools import command_run

app = FastAPI()


@app.get("/")
def index():
    return {"Hello": "World"}


@app.get("/command/")
async def command_runner_endpoint(info: Request):
    logger.info(
        f"command_runner_endpoint Parameters -> info: {info}"
    )

    try:
        req_info = await info.json()
    except Exception as error:
        logger.error(error)
        return {
            "status": "ERROR",
            "message": "Invalid JSON"
        }

    logger.info(f"req_info: {req_info}")

    command = req_info.get("command", "")
    password = req_info.get("pass", "")
    is_sudo = req_info.get("sudo", False)

    if password == "" or command == "":
        return {
            "status": "ERROR",
            "message": "No password or command provided"
        }

    if not is_sudo:
        password = ""

    command_result = command_run(
        command=command,
        sudo_password=password,
    )
    logger.info(f"command_result: {command_result}")

    return {
        "status": "SUCCESS",
        "data": command_result
    }


@app.get("/command/{command}/{password}/{is_sudo}")
async def command_runner_parameter_endpoint(command: str, password: str, is_sudo: bool = False):
    logger.info(
        f"command_runner_parameter_endpoint Parameters -> command: {command} | password: {password} | is_sudo: {is_sudo}"
    )

    if password == "" or command == "":
        return {
            "status": "ERROR",
            "message": "No password or command provided"
        }

    if not is_sudo:
        password = ""

    command_result = command_run(
        command=command,
        sudo_password=password,
    )
    logger.info(f"command_result: {command_result}")

    return {
        "status": "SUCCESS",
        "data": command_result
    }
