import asyncio
import json
from dataclasses import dataclass

from sqlalchemy import create_engine, DateTime, Integer, Float, String, MetaData, ForeignKey, select
from sqlalchemy.orm import declarative_base, sessionmaker, Mapped, mapped_column
from datetime import datetime

from utils import entry_factory

engine = create_engine('sqlite:///:memory:')

Base = declarative_base()


@dataclass
class Users(Base):
    __tablename__ = "users"
    user_id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    username: Mapped[str] = mapped_column(String(30))
    password: Mapped[str] = mapped_column(String(100))
    email: Mapped[str] = mapped_column(String(320))

    def __init__(self, user_id, username, password, email):
        self.user_id = user_id
        self.username = username
        self.password = password
        self.email = email


@dataclass
class Computers(Base):
    __tablename__ = "computers"
    pc_id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    pc_name: Mapped[str] = mapped_column(String(30))
    user_id = mapped_column(ForeignKey("users.user_id"))

    def __init__(self, pc_id, pc_name, user_id):
        self.pc_id = pc_id
        self.pc_name = pc_name
        self.user_id = user_id


@dataclass
class Stats(Base):
    __tablename__ = "stats"
    log_id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    pc_name: Mapped[str] = mapped_column(String(30))
    timestamp: Mapped[datetime] = mapped_column(DateTime)
    cpu_usage: Mapped[float] = mapped_column(Float)
    ram_total: Mapped[int] = mapped_column(Integer)
    ram_used: Mapped[int] = mapped_column(Integer)
    disk_read: Mapped[int] = mapped_column(Integer)
    disk_sent: Mapped[int] = mapped_column(Integer)
    net_rciv: Mapped[int] = mapped_column(Integer)
    net_sent: Mapped[int] = mapped_column(Integer)

    def __init__(self, data):
        self.pc_name = data['pc_name']
        self.timestamp = datetime.fromisoformat(data['timestamp'])
        self.cpu_usage = data['data']['cpu']['usage']
        self.ram_total = data['data']['ram']['total']
        self.ram_used = data['data']['ram']['used']
        self.disk_read = data['data']['disk']['kilobytes_read']
        self.disk_sent = data['data']['disk']['kilobytes_sent']
        self.net_rciv = data['data']['network']['kilobytes_recieved']
        self.net_sent = data['data']['network']['kilobytes_sent']

    def __str__(self):
        return f"PC Name: {self.pc_name}, Timestamp: {self.timestamp.isoformat()}, CPU Usage: {self.cpu_usage}, RAM Total: {self.ram_total}, RAM Used: {self.ram_used}, Disk Read: {self.disk_read}, Disk Sent: {self.disk_sent}, Network Received: {self.net_rciv}, Network Sent: {self.net_sent}"


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

    with SessionLocal() as session:
        session.add(Users(username="Lucas", password="123", email="", user_id=1))
        session.commit()

    with SessionLocal() as session:
        session.add(Computers(pc_name="LucasComputer", pc_id=1, user_id=1))
        session.commit()


def print_stats():
    session = SessionLocal()

    stats = session.query(Stats).all()

    for stat in stats:
        print(
            f"PC Name: {stat.pc_name}, Timestamp: {stat.timestamp}, CPU Usage: {stat.cpu_usage}, RAM Total: {stat.ram_total}, RAM Used: {stat.ram_used}, Disk Read: {stat.disk_read}, Disk Sent: {stat.disk_sent}, Network Received: {stat.net_rciv}, Network Sent: {stat.net_sent}")
    session.close()


def get_cpu_from_stats(user_id: int, pc_id: tuple[int] = (), period_start: datetime = datetime(1999, 1, 1),
                       period_end: datetime = None):
    if period_end is None:
        period_end = datetime.now()
        print("dupa")
    else:
        print("no dupa")
        print(type(period_end))

    session = SessionLocal()
    debug()
    print(period_end.isoformat())

    stat = (select(Stats.timestamp, Stats.cpu_usage)
            .join(Computers, Stats.pc_name == Computers.pc_name)
            .join(Users, Computers.user_id == Users.user_id)
            .where(Users.user_id == user_id)
            .where(Stats.timestamp.between(period_start, period_end)))

    if len(pc_id) != 0:
        stat = stat.where(Computers.pc_id.in_(pc_id))

    data = session.execute(stat).fetchall()
    return [{"timestamp": k.isoformat(), "usage": v} for k, v in data]


def get_ram_from_stats(user_id: int, pc_id: tuple[int] = (), period_start: datetime = datetime(1999, 1, 1),
                       period_end: datetime = datetime.now()):
    session = SessionLocal()

    stat = (select(Stats.timestamp, Stats.ram_used, Stats.ram_total)
            .join(Computers, Stats.pc_name == Computers.pc_name)
            .join(Users, Computers.user_id == Users.user_id)
            .where(user_id == Users.user_id)
            .where(Stats.timestamp.between(period_start, period_end)))

    if len(pc_id) != 0:
        stat = stat.where(Computers.pc_id.in_(pc_id))

    data = session.execute(stat).fetchall()
    return [{"timestamp": k.isoformat(), "total": total, "used": used} for k, used, total in data]


def get_disk_from_stats(user_id: int, pc_id: tuple[int] = (), period_start: datetime = datetime(1999, 1, 1),
                        period_end: datetime = datetime.now()):
    session = SessionLocal()

    stat = (select(Stats.timestamp, Stats.disk_sent, Stats.disk_read)
            .join(Computers, Stats.pc_name == Computers.pc_name)
            .join(Users, Computers.user_id == Users.user_id)
            .where(user_id == Users.user_id)
            .where(Stats.timestamp.between(period_start, period_end)))

    if len(pc_id) != 0:
        stat = stat.where(Computers.pc_id.in_(pc_id))

    data = session.execute(stat).fetchall()
    return [{"timestamp": k.isoformat(), "sent": sent, "read": read} for k, sent, read in data]


def debug():
    session = SessionLocal()

    print([str(i) for i in session.execute(select(Stats)).fetchall()])
    print(session.execute(select(Computers)).fetchall())
    print(session.execute(select(Users)).fetchall())


def get_network_from_stats(user_id: int, pc_id: tuple[int] = (), period_start: datetime = datetime(1999, 1, 1),
                           period_end: datetime = datetime.now()):
    session = SessionLocal()

    stat = (select(Stats.timestamp, Stats.net_sent, Stats.net_rciv)
            .join(Computers, Stats.pc_name == Computers.pc_name)
            .join(Users, Computers.user_id == Users.user_id)
            .where(user_id == Users.user_id)
            .where(Stats.timestamp.between(period_start, period_end)))

    if len(pc_id) != 0:
        stat = stat.where(Computers.pc_id.in_(pc_id))

    data = session.execute(stat).fetchall()
    return [{"timestamp": k.isoformat(), "sent": sent, "recieved": recieved} for k, sent, recieved in data]


async def save_entry():
    with SessionLocal() as session:
        session.add(Users(username="Lucas", password="123", email="", user_id=1))
        session.commit()

    with SessionLocal() as session:
        session.add(Computers(pc_name="LucasComputer", pc_id=1, user_id=1))
        session.commit()

    while True:
        data = json.loads(((await entry_factory()).to_json()))
        with SessionLocal() as session:
            session.add(Stats(data))
            session.commit()
