# -*- coding: utf-8 -*-
from sqlalchemy import create_engine, Column, Integer, String, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.engine.url import URL
import settings
DeclarativeBase = declarative_base()
def db_connect():
    """
    Performs database connection using database settings from settings.py.
    Returns sqlalchemy engine instance
    """
    return create_engine(URL(**settings.DATABASE))
def create_deals_table(engine):
    """"""

    DeclarativeBase.metadata.create_all(engine)
class Deals(DeclarativeBase):
    """Sqlalchemy deals model"""
    __tablename__ = "allitbooks"
    id = Column(Integer, primary_key = True)
    title = Column('title',String) # 书名
    author = Column('author',String) # 作者
    image = Column('image',String) # 封面
    url = Column('url',String) # 跳转链接
    isbn = Column('isbn',String) # isbn号
    year = Column('year',String) # 出版日期
    pages = Column('pages',String) # 页码数
    file_size = Column('file_size',String) # 文件大小
    category = Column('category',String) # 所属分类
    category_url = Column('category_url',String) # 分类链接
    description = Column('description',String) # 简述
    download = Column('download',String) # 下载链接