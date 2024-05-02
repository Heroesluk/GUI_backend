from datetime import datetime as dt

from fastapi import FastAPI
from uvicorn import run as uvirun

from Database import get_cpu_from_stats, get_ram_from_stats

app = FastAPI()


@app.get("/Stats/CPU")
async def cpu(user_id: int, pc_id: tuple[int] = (), period_start: str = dt(1999, 1, 1).isoformat(),
              period_end: str = dt.now().isoformat()):
    return get_cpu_from_stats(user_id, pc_id, dt.fromisoformat(period_start), dt.fromisoformat(period_end))


@app.get("/Stats/RAM")
async def ram(user_id: int, pc_id: tuple[int] = (), period_start: str = dt(1999, 1, 1).isoformat(),
              period_end: str = dt.now().isoformat()):
    return get_ram_from_stats(user_id, pc_id, dt.fromisoformat(period_start), dt.fromisoformat(period_end))


@app.get("/Stats/DISK")
async def disk(user_id: int, pc_id: tuple[int] = (), period_start: str = dt(1999, 1, 1).isoformat(),
               period_end: str = dt.now().isoformat()):
    return get_ram_from_stats(user_id, pc_id, dt.fromisoformat(period_start), dt.fromisoformat(period_end))


@app.get("/Stats/NETWORK")
async def network(user_id: int, pc_id: tuple[int] = (), period_start: str = dt(1999, 1, 1).isoformat(),
                  period_end: str = dt.now().isoformat()):
    return get_ram_from_stats(user_id, pc_id, dt.fromisoformat(period_start), dt.fromisoformat(period_end))


if __name__ == "__main__":
    uvirun(app, host="127.0.0.1", port=8000)
