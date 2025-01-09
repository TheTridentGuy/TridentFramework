import threading


def spawn_thread(target, args=(), kwargs={}, daemon=True):
    thread = threading.Thread(target=target, args=args, kwargs=kwargs)
    thread.daemon = daemon
    thread.start()
    return thread
