from datetime import datetime

import psutil

from Model import PC, Data, CPU, RAM, Disk, Network

# extract to env
user_id = "LucasComputer"


def get_cpu_usage():
    return CPU(psutil.cpu_percent(interval=1))


def get_ram_usage():
    return RAM(psutil.virtual_memory().total, psutil.virtual_memory().used)


def get_disk_usage():
    return Disk(psutil.disk_io_counters().read_count, psutil.disk_io_counters().write_count)


def get_network_usage():
    return Network(psutil.net_io_counters().bytes_recv, psutil.net_io_counters().bytes_sent)


def entryFactory():
    return PC(
        pc_name="LucasComputer",
        pc_id="LucasComputer",
        timestamp=datetime.now().isoformat(),
        data=Data(
            cpu=get_cpu_usage(),
            ram=get_ram_usage(),
            disk=get_disk_usage(),
            network=get_network_usage()
        )
    ).to_json()
