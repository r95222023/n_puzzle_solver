import os


def memory_usage_psutil():
    # return the memory usage in MB
    import psutil
    process = psutil.Process(os.getpid())
    mem = process.memory_info().rss / float(2 ** 10)
    return mem


def memory_usage_ps():
    import subprocess
    out = subprocess.Popen(['ps', 'v', '-p', str(os.getpid())],
    stdout=subprocess.PIPE).communicate()[0].split(b'\n')
    vsz_index = out[0].split().index(b'RSS')
    mem = float(out[1].split()[vsz_index]) / 1024
    return mem
