args = ["-c", "--c2"]
kwargs = {"metavar": "scheme://host:port", "help": "set the C2 server root url"}


def main(args, env):
    l = env["LOGGER"]
    env["C2_URL"] = args
    l.info(f"{__name__}: set C2 server root url to {args}")
