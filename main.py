from fastapi import FastAPI
from sqlalchemy import create_engine, DateTime, Integer, Float, String, MetaData, ForeignKey, select
from sqlalchemy.orm import Session, declarative_base, sessionmaker, Mapped, mapped_column
from datetime import datetime as dt
from uvicorn import run as uvirun
from pandas import read_sql
from typing import List

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

metadata = MetaData()
Base.metadata.create_all(engine)
session = sessionmaker(bind=engine)


app = FastAPI()

@app.get("/Stats/CPU")
async def cpu(pc_id: List[int], user_id: List[int], period_start: dt, period_end: dt):
    stat = session.query(Stats.cpu_usage).outerjoin(Computers, Stats.pc_id==Computers.pc_id).outerjoin(Users, Computers.user_id==Users.user_id) \
        .filter(Stats.pc_id in pc_id, Computers.user_id in user_id, Stats.timestamp >= period_start, Stats.timestamp <= period_end).statement
    stat = read_sql(stat, session.bind)     #converts to dataframe
    return stat

@app.get("/Stats/RAM")
async def ram(pc_id: List[int], user_id: List[int], period_start: dt, period_end: dt):
    stat = session.query(Stats.ram_total, Stats.ram_used).outerjoin(Computers, Stats.pc_id==Computers.pc_id).outerjoin(Users, Computers.user_id==Users.user_id) \
        .filter(Stats.pc_id in pc_id, Computers.user_id in user_id, Stats.timestamp >= period_start, Stats.timestamp <= period_end).statement
    stat = read_sql(stat, session.bind)     #converts to dataframe
    return stat

@app.get("/Stats/DISK")
async def disk(pc_id: List[int], user_id: List[int], period_start: dt, period_end: dt):
    stat = session.query(Stats.disk_read, Stats.disk_sent).outerjoin(Computers, Stats.pc_id==Computers.pc_id).outerjoin(Users, Computers.user_id==Users.user_id) \
        .filter(Stats.pc_id in pc_id, Computers.user_id in user_id, Stats.timestamp >= period_start, Stats.timestamp <= period_end).statement
    stat = read_sql(stat, session.bind)     #converts to dataframe
    return stat

@app.get("/Stats/NETWORK")
async def network(pc_id: List[int], user_id: List[int], period_start: dt, period_end: dt):
    stat = session.query(Stats.net_rciv, Stats.net_sent).outerjoin(Computers, Stats.pc_id==Computers.pc_id).outerjoin(Users, Computers.user_id==Users.user_id) \
        .filter(Stats.pc_id in pc_id, Computers.user_id in user_id, Stats.timestamp >= period_start, Stats.timestamp <= period_end).statement
    stat = read_sql(stat, session.bind)     #converts to dataframe
    return stat

if __name__ == "__main__":
    uvirun(app, host="127.0.0.1", port = 8000)