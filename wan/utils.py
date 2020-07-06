import subprocess
from iterfzf import iterfzf


def iter_ps():
    res = subprocess.check_output('ps aux', shell=True)
    res = res.decode()
    return res.split('\n')


def get_pid_from_line(line):
    if line is not None:
        return int(line.split()[1])


def get_pid_via_fzf(exact=True):
    # TODO: make it can be selected with full match
    return get_pid_from_line(iterfzf(iter_ps(), multi=False, exact=exact))


if __name__ == "__main__":
    print(get_pid_via_fzf())
