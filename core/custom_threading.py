"""Simplified threading module for basic threading functionality."""

import _thread
from time import monotonic as _time

# Core threading functionality
class Lock:
    """A simple lock implementation."""
    def __init__(self):
        self._lock = _thread.allocate_lock()

    def acquire(self, blocking=True, timeout=-1):
        """Acquire the lock."""
        return self._lock.acquire(blocking, timeout)

    def release(self):
        """Release the lock."""
        self._lock.release()

    def locked(self):
        """Check if the lock is currently held."""
        return self._lock.locked()

class Thread:
    """A simple thread implementation."""
    def __init__(self, target=None, args=(), kwargs=None, daemon=None):
        self._target = target
        self._args = args
        self._kwargs = kwargs or {}
        self._daemon = daemon
        self._started = False

    def start(self):
        """Start the thread."""
        if self._started:
            raise RuntimeError("Thread already started")
        self._started = True
        _thread.start_new_thread(self._run, ())

    def _run(self):
        """Run the target function."""
        if self._target:
            self._target(*self._args, **self._kwargs)

    def is_alive(self):
        """Check if the thread is alive."""
        return self._started

# Timer functionality
class Timer(Thread):
    """Call a function after a specified number of seconds."""
    def __init__(self, interval, function, args=None, kwargs=None):
        super().__init__(target=self._run)
        self.interval = interval
        self.function = function
        self.args = args or ()
        self.kwargs = kwargs or {}
        self.finished = Lock()

    def _run(self):
        _time.sleep(self.interval)
        if not self.finished.locked():
            self.function(*self.args, **self.kwargs)

    def cancel(self):
        """Stop the timer."""
        self.finished.acquire()

# Utility functions
def current_thread():
    """Return the current thread."""
    return _thread.get_ident()

def active_count():
    """Return the number of active threads."""
    return len(_thread._active)

if __name__ == "__main__":
    # Example usage of the Thread class
    def example_function():
        print("Thread is running")

    thread = Thread(target=example_function)
    thread.start()

    # Example usage of the Timer class
    def delayed_function():
        print("This is delayed")

    timer = Timer(5, delayed_function)  # Call after 5 seconds
    timer.start()
