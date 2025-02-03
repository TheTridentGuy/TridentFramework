# TridentFramework
## A simple, cross-platform post-exploitation framework written in Python.
> ## DISCLAIMER:
> ### This software is for educational purposes only. I do not condone any illegal or unethical use. Use at your own risk. I am NOT responsible for any damages caused by this software.

## Features:
- Modular, each module is a simple python script, and declares it's own command line arguments.
- Includes several premade modules.
- Cross-platform
- Custom thread-safe `env` dict for communication across multiple threads.
- Simple C2 system coming soon

## Minimal Example Module:
```
# module-specific arguments, defines parameters for `argparser`
args = ["-a", "--args-here"]
kwargs = {"metavar": "args", "help": "do something"}


def main(args, env):
    pass
```
