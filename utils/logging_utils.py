import sys
from multiprocessing import Lock
from enum import Enum

# Lock to synchronize prints between processes
print_lock = Lock()

# For debug. Save original stdout reference at import time
_original_stdout = sys.__stdout__
class OutputTarget(Enum):
    """Enum per specificare dove stampare"""
    TERMINAL_ONLY = "terminal"
    FILE_ONLY = "file"
    BOTH = "both"

class TeeOutput:
    """Writes simultaneously to stdout and to a file"""
    def __init__(self, log_file):
        self.terminal = sys.stdout
        self.log_file = open(log_file, 'w', encoding='utf-8')

    def write(self, message):
        self.terminal.write(message)
        self.log_file.write(message)

    def flush(self):
        self.terminal.flush()
        self.log_file.flush()

    def close(self):
        try:
            self.log_file.close()
        except Exception:
            pass

def synchronized_print(*args, target: OutputTarget = OutputTarget.BOTH, **kwargs):
    """Atomic and synchronized print to avoid mixing output between processes
    Writes to both terminal AND current stdout (which may be redirected to a buffer
    E.g.:
        synchronized_print("Hello")             # Prints to both (default)
        synchronized_print("Debug info", target=OutputTarget.TERMINAL_ONLY)
        synchronized_print("Log entry", target=OutputTarget.FILE_ONLY)
    """
    with print_lock:
        # Print to terminal if requested
        if target in (OutputTarget.TERMINAL_ONLY, OutputTarget.BOTH):
            print(*args, **kwargs, file=_original_stdout)
            _original_stdout.flush()
        
        # Print to file if requested and stdout is different from terminal
        if target in (OutputTarget.FILE_ONLY, OutputTarget.BOTH):
            if sys.stdout != _original_stdout:
                print(*args, **kwargs, file=sys.stdout)
                sys.stdout.flush()


def setup_logging(log_file: str = "log.txt"):
    """Setup logging to both console and file"""
    tee = TeeOutput(log_file)
    sys.stdout = tee
    return tee