import subprocess
from iterfzf import iterfzf
import psutil
from loguru import logger
import os
import stat


def iter_ps():
    res = subprocess.check_output("ps aux", shell=True)
    res = res.decode()
    return res.split("\n")


def get_pid_from_line(line):
    if line is not None:
        return int(line.split()[1])


def get_pid_via_fzf(exact=True):
    try:
        # FIXME: This is a bug from iterfzf. The fzf may not be executable
        selected_line = iterfzf(iter_ps(), multi=False, exact=exact)
    except PermissionError as e:
        try:
            os.chmod(e.filename, os.stat(e.filename).st_mode | stat.S_IEXEC)
        except PermissionError:
            logger.error(f"Please make {e.filename} executable(e.g  `chmod a+x {e.filename}`).")
            return None
        else:
            selected_line = iterfzf(iter_ps(), multi=False, exact=exact)
    return get_pid_from_line(selected_line)


def is_buzy(proc: psutil.Process) -> bool:
    """is_buzy.

    Parameters
    ----------
    proc : psutil.Process
        process

    Returns
    -------
    bool
        if the process or its subprocess buzy
    """
    try:
        p_status = proc.status()
        logger.debug(f"cmd: {proc.cmdline()}, status: {p_status}")
        if p_status in {psutil.STATUS_RUNNING, psutil.STATUS_DISK_SLEEP}:
            return True
        for ch_proc in proc.children():
            if is_buzy(ch_proc):
                return True
        return False
    except psutil.NoSuchProcess:
        return False


if __name__ == "__main__":
    print(get_pid_via_fzf())
