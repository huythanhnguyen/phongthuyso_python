"""
Database Package

Package chứa các module kết nối và thao tác với cơ sở dữ liệu MongoDB.
"""

from .mongodb import get_database, db, close_connection

__all__ = ["get_database", "db", "close_connection"] 