# coding: utf-8
from sqlalchemy import BigInteger, Boolean, Column, DateTime, Float, ForeignKey, Integer, Text, text
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()
metadata = Base.metadata


class AssetInfo(Base):
    __tablename__ = 'asset_info'

    id = Column(Integer, primary_key=True, server_default=text("nextval('asset_info_id_seq'::regclass)"))
    symbol = Column(Text)
    data_source = Column(Text)
    _class = Column('class', Text)
    sub_class = Column(Text)
    type = Column(Text)


class Entry(Base):
    __tablename__ = 'entry'

    id = Column(Integer, primary_key=True, server_default=text("nextval('entry_id_seq'::regclass)"))
    entry_date = Column(DateTime)
    symbol = Column(Text)
    cost = Column(Float(53))
    stop = Column(Float(53))
    trail = Column(Float(53))
    trail_amount = Column(Float(53))
    target = Column(Float(53))
    quantity = Column(Float(53))
    direction = Column(BigInteger)
    risk = Column(BigInteger)
    multiple = Column(BigInteger)
    fraction = Column(Float(53))
    is_relative = Column(Boolean)
    stock_id = Column(BigInteger)
    signal_age = Column(BigInteger)
    r_pct = Column(Float(53))


class Stock(Base):
    __tablename__ = 'stock'

    id = Column(Integer, primary_key=True, server_default=text("nextval('stock_id_seq'::regclass)"))
    symbol = Column(Text, nullable=False)
    is_relative = Column(Boolean, nullable=False)
    interval = Column(Text, nullable=False)
    data_source = Column(Text, nullable=False)
    market_index = Column(Text, nullable=False)
    sec_type = Column(Text, nullable=False)


class StockInfo(Base):
    __tablename__ = 'stock_info'

    id = Column(Integer, primary_key=True, server_default=text("nextval('stock_info_id_seq'::regclass)"))
    symbol = Column(Text)
    Security = Column(Text)
    GICS_Sector = Column('GICS Sector', Text)
    GICS_Sub_Industry = Column('GICS Sub-Industry', Text)
    Headquarters_Location = Column('Headquarters Location', Text)
    Date_added = Column('Date added', Text)
    CIK = Column(BigInteger)
    Founded = Column(Text)


class TimestampDatum(Base):
    __tablename__ = 'timestamp_data'

    bar_number = Column(Integer, primary_key=True, server_default=text("nextval('timestamp_data_bar_number_seq'::regclass)"))
    interval = Column(Text, nullable=False)
    timestamp = Column(DateTime, nullable=False)
    data_source = Column(Text, nullable=False)


class FloorCeiling(Base):
    __tablename__ = 'floor_ceiling'

    id = Column(Integer, primary_key=True, server_default=text("nextval('floor_ceiling_id_seq'::regclass)"))
    test = Column(Float(53), nullable=False)
    fc_val = Column(Float(53), nullable=False)
    fc_date = Column(ForeignKey('timestamp_data.bar_number'), nullable=False, server_default=text("nextval('floor_ceiling_fc_date_seq'::regclass)"))
    rg_ch_date = Column(ForeignKey('timestamp_data.bar_number'), nullable=False, server_default=text("nextval('floor_ceiling_rg_ch_date_seq'::regclass)"))
    rg_ch_val = Column(Float(53), nullable=False)
    type = Column(BigInteger, nullable=False)
    stock_id = Column(ForeignKey('stock.id'), nullable=False, server_default=text("nextval('floor_ceiling_stock_id_seq'::regclass)"))

    timestamp_datum = relationship('TimestampDatum', primaryjoin='FloorCeiling.fc_date == TimestampDatum.bar_number')
    timestamp_datum1 = relationship('TimestampDatum', primaryjoin='FloorCeiling.rg_ch_date == TimestampDatum.bar_number')
    stock = relationship('Stock')


class Peak(Base):
    __tablename__ = 'peak'

    id = Column(Integer, primary_key=True, server_default=text("nextval('peak_id_seq'::regclass)"))
    start = Column(ForeignKey('timestamp_data.bar_number'), nullable=False, server_default=text("nextval('peak_start_seq'::regclass)"))
    end = Column(ForeignKey('timestamp_data.bar_number'), nullable=False, server_default=text("nextval('peak_end_seq'::regclass)"))
    type = Column(BigInteger, nullable=False)
    lvl = Column(BigInteger, nullable=False)
    stock_id = Column(ForeignKey('stock.id'), nullable=False, server_default=text("nextval('peak_stock_id_seq'::regclass)"))

    timestamp_datum = relationship('TimestampDatum', primaryjoin='Peak.end == TimestampDatum.bar_number')
    timestamp_datum1 = relationship('TimestampDatum', primaryjoin='Peak.start == TimestampDatum.bar_number')
    stock = relationship('Stock')


class Regime(Base):
    __tablename__ = 'regime'

    id = Column(Integer, primary_key=True, server_default=text("nextval('regime_id_seq'::regclass)"))
    start = Column(ForeignKey('timestamp_data.bar_number'), nullable=False, server_default=text("nextval('regime_start_seq'::regclass)"))
    end = Column(ForeignKey('timestamp_data.bar_number'), nullable=False, server_default=text("nextval('regime_end_seq'::regclass)"))
    rg = Column(Float(53), nullable=False)
    type = Column(Text, nullable=False)
    stock_id = Column(ForeignKey('stock.id'), nullable=False, server_default=text("nextval('regime_stock_id_seq'::regclass)"))

    timestamp_datum = relationship('TimestampDatum', primaryjoin='Regime.end == TimestampDatum.bar_number')
    timestamp_datum1 = relationship('TimestampDatum', primaryjoin='Regime.start == TimestampDatum.bar_number')
    stock = relationship('Stock')


class StockDatum(Base):
    __tablename__ = 'stock_data'

    id = Column(Integer, primary_key=True, server_default=text("nextval('stock_data_id_seq'::regclass)"))
    bar_number = Column(ForeignKey('timestamp_data.bar_number'), nullable=False, server_default=text("nextval('stock_data_bar_number_seq'::regclass)"))
    close = Column(Float(53), nullable=False)
    stock_id = Column(ForeignKey('stock.id'), nullable=False)
    open = Column(Float(53), nullable=False)
    high = Column(Float(53), nullable=False)
    low = Column(Float(53), nullable=False)
    volume = Column(BigInteger, nullable=False)

    timestamp_datum = relationship('TimestampDatum')
    stock = relationship('Stock')
