import datetime
import json
from datetime import datetime as dt
from typing import List

from fastapi import FastAPI
from pandas import read_sql
from sqlalchemy import create_engine, DateTime, Integer, Float, String, MetaData, ForeignKey
from sqlalchemy.orm import declarative_base, sessionmaker, Mapped, mapped_column
from uvicorn import run as uvirun

engine = create_engine('sqlite:///:memory:')

Base = declarative_base()


class Users(Base):
    __tablename__ = "users"
    user_id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    username: Mapped[str] = mapped_column(String(30))
    password: Mapped[str] = mapped_column(String(100))
    email: Mapped[str] = mapped_column(String(320))


class Computers(Base):
    __tablename__ = "computers"
    pc_id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    pc_name: Mapped[str] = mapped_column(String(30))
    user_id = mapped_column(ForeignKey("users.user_id"))


class Stats(Base):
    __tablename__ = "stats"
    log_id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    pc_name: Mapped[str] = mapped_column(String(30))
    pc_id = mapped_column(ForeignKey("computers.pc_id"))
    timestamp: Mapped[str] = mapped_column(DateTime)
    cpu_usage: Mapped[float] = mapped_column(Float)
    ram_total: Mapped[int] = mapped_column(Integer)
    ram_used: Mapped[int] = mapped_column(Integer)
    disk_read: Mapped[int] = mapped_column(Integer)
    disk_sent: Mapped[int] = mapped_column(Integer)
    net_rciv: Mapped[int] = mapped_column(Integer)
    net_sent: Mapped[int] = mapped_column(Integer)

    def __init__(self, data):
        self.pc_name = data['pc_name']
        self.pc_id = data['pc_id']
        self.timestamp = data['timestamp']
        self.cpu_usage = data['data']['cpu']['usage']
        self.ram_total = data['data']['ram']['total']
        self.ram_used = data['data']['ram']['used']
        self.disk_read = data['data']['disk']['kilobytes_read']
        self.disk_sent = data['data']['disk']['kilobytes_sent']
        self.net_rciv = data['data']['network']['kilobytes_recieved']
        self.net_sent = data['data']['network']['kilobytes_sent']


SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

metadata = MetaData()
Base.metadata.create_all(engine)


def save_mock_data():
    with open("mock_data.json", "r") as f:
        data = json.load(f)

        for entry in data:
            with SessionLocal() as session:
                session.add(Stats(entry))
                session.commit()

    session.close()


def print_stats():
    session = SessionLocal()

    stats = session.query(Stats).all()

    for stat in stats:
        print(
            f"PC Name: {stat.pc_name}, PC ID: {stat.pc_id}, Timestamp: {stat.timestamp}, CPU Usage: {stat.cpu_usage}, RAM Total: {stat.ram_total}, RAM Used: {stat.ram_used}, Disk Read: {stat.disk_read}, Disk Sent: {stat.disk_sent}, Network Received: {stat.net_rciv}, Network Sent: {stat.net_sent}")
    session.close()


save_mock_data()
print_stats()
app = FastAPI()
session = SessionLocal()







@app.get("/Stats/CPU")
async def cpu(pc_id: List[int], user_id: List[int], period_start: dt, period_end: dt):
    stat = (session.query(Stats.cpu_usage)
            .outerjoin(Computers, Stats.pc_id == Computers.pc_id).outerjoin(Users, Computers.user_id == Users.user_id)
            .filter(Stats.pc_id in pc_id, Computers.user_id in user_id, Stats.timestamp >= period_start,
                    Stats.timestamp <= period_end).statement)
    stat = read_sql(stat, session.bind)  # converts to dataframe
    return stat


@app.get("/Stats/RAM")
async def ram(pc_id: List[int], user_id: List[int], period_start: dt, period_end: dt):
    stat = (session.query(Stats.ram_total, Stats.ram_used)
            .outerjoin(Computers, Stats.pc_id == Computers.pc_id).outerjoin(Users, Computers.user_id == Users.user_id)
            .filter(Stats.pc_id in pc_id, Computers.user_id in user_id, Stats.timestamp >= period_start,
                    Stats.timestamp <= period_end).statement)
    stat = read_sql(stat, session.bind)  # converts to dataframe
    return stat


@app.get("/Stats/DISK")
async def disk(pc_id: List[int], user_id: List[int], period_start: dt, period_end: dt):
    stat = (session.query(Stats.disk_read, Stats.disk_sent)
            .outerjoin(Computers, Stats.pc_id == Computers.pc_id)
            .outerjoin(Users, Computers.user_id == Users.user_id)
            .filter(Stats.pc_id in pc_id, Computers.user_id in user_id, Stats.timestamp >= period_start,
                    Stats.timestamp <= period_end).statement)
    stat = read_sql(stat, session.bind)  # converts to dataframe
    return stat


@app.get("/Stats/NETWORK")
async def network(pc_id: List[int], user_id: List[int], period_start: dt, period_end: dt):
    stat = (session.query(Stats.net_rciv, Stats.net_sent)
            .outerjoin(Computers, Stats.pc_id == Computers.pc_id)
            .outerjoin(Users, Computers.user_id == Users.user_id)
            .filter(Stats.pc_id in pc_id, Computers.user_id in user_id, Stats.timestamp >= period_start,
                    Stats.timestamp <= period_end).statement)
    stat = read_sql(stat, session.bind)  # converts to dataframe
    return stat


if __name__ == "__main__":
    uvirun(app, host="127.0.0.1", port=8000)
