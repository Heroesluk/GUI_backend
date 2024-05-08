from asyncio import create_task
from datetime import datetime as dt

from fastapi import FastAPI
from uvicorn import run as uvirun

from Database import get_cpu_from_stats, get_ram_from_stats, get_disk_grouped_by_time, get_network_from_stats, save_entry, \
    get_total_disk_usage, get_total_network_usage, get_average_cpu_load, get_average_ram_usage, get_stats_snapshot

app = FastAPI()

from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

origins = [
    "http://localhost.tiangolo.com",
    "https://localhost.tiangolo.com",
    "http://localhost",
    "http://localhost:8080",
    "http://localhost:5173",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.on_event("startup")
async def startup_event():
    create_task(save_entry())


@app.get("/Stats/CPU")
async def cpu(user_id: int, pc_id: tuple[int] = (), period_start: str = dt(1999, 1, 1).isoformat(),
              period_end: str = dt(2030, 1, 1).isoformat()):
    return get_cpu_from_stats(user_id, pc_id, dt.fromisoformat(period_start), dt.fromisoformat(period_end))


@app.get("/Stats/RAM")
async def ram(user_id: int, pc_id: tuple[int] = (), period_start: str = dt(1999, 1, 1).isoformat(),
              period_end: str = dt(2030, 1, 1).isoformat()):
    return get_ram_from_stats(user_id, pc_id, dt.fromisoformat(period_start), dt.fromisoformat(period_end))


@app.get("/Stats/DISK")
async def disk(user_id: int, pc_id: tuple[int] = (), period_start: str = dt(1999, 1, 1).isoformat(),
               period_end: str = dt(2030, 1, 1).isoformat()):
    return get_total_disk_usage(user_id, pc_id, dt.fromisoformat(period_start), dt.fromisoformat(period_end))


@app.get("/Stats/NETWORK")
async def network(user_id: int, pc_id: tuple[int] = (), period_start: str = dt(1999, 1, 1).isoformat(),
                  period_end: str = dt(2030, 1, 1).isoformat()):
    return get_network_from_stats(user_id, pc_id, dt.fromisoformat(period_start), dt.fromisoformat(period_end))


@app.get("/Stats/SNAPSHOT")
async def totaldisk(user_id: int, pc_id: tuple[int] = (), period_start: str = dt(1999, 1, 1).isoformat(),
                    period_end: str = dt(2030, 1, 1).isoformat()):
    return get_stats_snapshot(user_id, pc_id, dt.fromisoformat(period_start), dt.fromisoformat(period_end))


@app.get("/Stats/DISK-GROUPED")
async def totaldisk(user_id: int, pc_id: tuple[int] = (), period_start: str = dt(1999, 1, 1).isoformat(),
                    period_end: str = dt(2030, 1, 1).isoformat()):
    return get_disk_grouped_by_time(user_id, pc_id, dt.fromisoformat(period_start), dt.fromisoformat(period_end))


if __name__ == "__main__":
    uvirun(app, host="127.0.0.1", port=8000)
