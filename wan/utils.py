import subprocess
from iterfzf import iterfzf
from loguru import logger


def iter_ps():
    res = subprocess.check_output('ps aux', shell=True)
    res = res.decode()
    return res.split('\n')


def get_pid_from_line(line):
    if line is not None:
        return int(line.split()[1])


def get_pid_via_fzf(exact=True):
    try:
        selected_line = iterfzf(iter_ps(), multi=False, exact=exact)
    except PermissionError as e:
        logger.error(f'Please make {e.filename} executable(e.g  `chmod a+x {e.filename}`).')
        return None
    return get_pid_from_line(selected_line)


if __name__ == "__main__":
    print(get_pid_via_fzf())
