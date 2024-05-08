import json
import subprocess
from dataclasses import asdict
from datetime import datetime
from time import sleep
import asyncio
import psutil
import platform
from Model import PC, Data, CPU, RAM, Disk, Network

# extract to env

async def get_cpu_usage():
    return CPU(psutil.cpu_percent(interval=1))


def get_ram_usage():
    return RAM(psutil.virtual_memory().total // 1000, psutil.virtual_memory().used // 1000)


def get_disk_usage():
    return Disk(psutil.disk_io_counters().read_bytes // 1000, psutil.disk_io_counters().write_bytes // 1000)

async def get_disk_io_delta():
    disk_io_start = get_disk_usage()
    await asyncio.sleep(1)
    disk_io_end = get_disk_usage()
    return Disk(disk_io_end.kilobytes_read - disk_io_start.kilobytes_read,
                disk_io_end.kilobytes_sent - disk_io_start.kilobytes_sent)


def get_network_usage():
    return Network(psutil.net_io_counters().bytes_recv // 1000, psutil.net_io_counters().bytes_sent // 1000)


async def get_network_delta():
    network_usage_start = get_network_usage()
    await asyncio.sleep(1)
    network_usage_end = get_network_usage()
    return Network(network_usage_end.kilobytes_recieved - network_usage_start.kilobytes_recieved,
                   network_usage_end.kilobytes_sent - network_usage_start.kilobytes_sent)


async def entry_factory() -> PC:
    user_id = "LucasComputer"

    disk_delta, network_delta, cpu_usage = await asyncio.gather(get_disk_io_delta(), get_network_delta(),
                                                                get_cpu_usage())
    time = datetime.now().isoformat()
    print(f"entry at {time} created!")
    return PC(
        pc_name=user_id,
        pc_id="1",
        timestamp=time,
        data=Data(
            cpu=cpu_usage,
            ram=get_ram_usage(),
            disk=disk_delta,
            network=network_delta
        )
    )


# This will be data recieved from clients, that will be forwarded to the server and saved to db
async def generate_data_recieved_by_server():
    data = []
    for i in range(50):
        data.append(await entry_factory())
    with open("mock_data.json", "w") as f:
        json.dump([asdict(d) for d in data], f, indent=4)


# Methods for mocking data for frontend before we have DB methods
def generate_mock_cpu():
    data = [{"timestamp": datetime.now().isoformat(), "usage": get_cpu_usage().usage} for i in range(50)]

    with open("resources/mock_cpu.json", "w") as f:
        json.dump(data, f, indent=4)


def generate_mock_ram():
    dt = []
    for i in range(50):
        ram = get_ram_usage()
        data = {
            "timestamp": datetime.now().isoformat(),
            "total": ram.total,
            "used": ram.used
        }
        dt.append(data)
        sleep(0.2)
    with open("resources/mock_ram.json", "w") as f:
        json.dump(dt, f, indent=4)


async def generate_mock_disk():
    dt = []
    for i in range(50):
        disk = await get_disk_io_delta()
        data = {
            "timestamp": datetime.now().isoformat(),
            "read": disk.kilobytes_read,
            "sent": disk.kilobytes_sent
        }
        dt.append(data)

    with open("resources/mock_disk.json", "w") as f:
        json.dump(dt, f, indent=4)


async def generate_mock_network():
    dt = []
    for i in range(50):
        network = await get_network_delta()
        data = {
            "timestamp": datetime.now().isoformat(),
            "recieved": network.kilobytes_recieved,
            "sent": network.kilobytes_sent
        }
        dt.append(data)

    with open("resources/mock_network.json", "w") as f:
        json.dump(dt, f, indent=4)


def get_system_info(os: str):
    command = {"windows": "wmic cpu get name", "linux": "lscpu"}

    cpu = subprocess.run(['cmd', '/c', command[os]], capture_output=True, text=True).stdout
    cpu_parsed = cpu.split('\n')[2].rstrip()
    return {
        "system": platform.system(),
        "node": platform.node(),
        "release": platform.release(),
        "version": platform.version(),
        "machine": platform.machine(),
        "processor": cpu_parsed,
        "physical_cores": psutil.cpu_count(),
        "logical_cores": psutil.cpu_count(logical=True),
        "cpu_freq": psutil.cpu_freq().max,
        "total_memory": psutil.virtual_memory().total // 1000000,
        "total_disk_size:": psutil.disk_usage('/').total // 1000000,
    }


#def get_mock_system_info():
#    with open("resources/mock_system_info.json", "w") as f:
#        json.dump(get_system_info('windows'), f, indent=4)


#get_mock_system_info()

# if __name__ == '__main__':
#     generate_mock_ram()
