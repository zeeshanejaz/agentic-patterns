"""Windows import shim: NOOA uses POSIX fcntl and SIGUSR2 at import time."""

from __future__ import annotations

import signal
import sys
import types


def install_windows_compat() -> None:
    if sys.platform != "win32":
        return
    if "fcntl" not in sys.modules:
        stub = types.ModuleType("fcntl")
        stub.LOCK_SH = 1
        stub.LOCK_EX = 2
        stub.LOCK_NB = 4
        stub.LOCK_UN = 8

        def flock(_fd: int, _op: int) -> None:
            return None

        stub.flock = flock
        sys.modules["fcntl"] = stub
    if not hasattr(signal, "SIGUSR2"):
        signal.SIGUSR2 = getattr(signal, "SIGBREAK", signal.SIGTERM)
