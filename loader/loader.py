import argparse
import platform
import os
import sys
import logging
import importlib.util
from pathlib import Path
from envdict import EnvDict
import threading


LOG_LEVEL = logging.DEBUG
STARTUP_MESSAGE = "trident agent v1.0"
MODULE_DIR = Path(__file__).parent.resolve() / "modules"


l = logging.getLogger(__name__)
formatter = logging.Formatter("[%(levelname)s]\t%(message)s")
stdout_handler = logging.StreamHandler(sys.stdout)
stdout_handler.setFormatter(formatter)
l.addHandler(stdout_handler)
l.setLevel(LOG_LEVEL)
l.debug("logger initialized")
l.info(STARTUP_MESSAGE)


modules = {}
args = argparse.ArgumentParser()
for module in MODULE_DIR.iterdir():
    if module.is_file() and module.suffix == ".py":
        module_name = module.stem
        module_path = MODULE_DIR / module
        l.debug(f"staging module: {module_name} ({module_path})")
        try:
            spec = importlib.util.spec_from_file_location(module_name, module)
            module = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(module)
            modules[module_name] = module
            args.add_argument(*module.args, **module.kwargs)
        except Exception as e:
            l.error(f"failed to stage module: {module_name} ({module_path}) due to {e}")
l.debug(f"available modules: {modules.keys()}")
args = args.parse_args()


env = EnvDict()
env["LOGGER"] = l


platform_uname = platform.uname()
l.debug(f"platform info: {platform_uname}")
env["PLATFORM_UNAME"] = platform_uname
platform_system = platform_uname.system.lower()
env["PLATFORM_SYSTEM"] = platform_system
platform_release = platform_uname.release
env["PLATFORM_RELEASE"] = platform_release
platform_machine = platform_uname.machine
env["PLATFORM_MACHINE"] = platform_machine
platform_hostname = platform_uname.node
env["PLATFORM_HOSTNAME"] = platform_hostname
platform_user = os.getlogin()
env["PLATFORM_USER"] = platform_user
l.info(f"detected platform: {platform_system} {platform_release} {platform_machine} ({platform_hostname})")
l.info(f"detected user: {platform_user}@{platform_hostname}")


threads = []
for module_name, module in modules.items():
    if not args.__dict__.get(module_name):
        l.debug(f"skipping module: {module_name}...")
        continue
    try:
        l.debug(f"loading module: {module_name}...")
        t = threading.Thread(target=module.main, args=(args.__dict__.get(module_name), env))
        l.info(f"loaded module: {module_name}")
        t.start()
        threads.append(t)
    except Exception as e:
        l.error(f"failed to load module: {module_name} due to {e}")
