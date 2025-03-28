import aiosqlite
from pathlib import Path
from typing import List, Dict, Any

class DatabaseMetaService:
    def __init__(self, db_path: str | Path):
        self.db_path = Path(db_path)

    async def get_tables(self) -> List[Dict[str, Any]]:
        """테이블 목록 조회"""
        async with aiosqlite.connect(self.db_path) as db:
            db.row_factory = aiosqlite.Row
            async with db.execute(
                """
                SELECT name, sql 
                FROM sqlite_master 
                WHERE type='table' AND name NOT LIKE 'sqlite_%'
                ORDER BY name
                """
            ) as cursor:
                return [dict(row) for row in await cursor.fetchall()]

    async def get_table_info(self, table_name: str) -> List[Dict[str, Any]]:
        """테이블 컬럼 정보 조회"""
        async with aiosqlite.connect(self.db_path) as db:
            db.row_factory = aiosqlite.Row
            async with db.execute(f"PRAGMA table_info({table_name})") as cursor:
                return [dict(row) for row in await cursor.fetchall()]

    async def get_indexes(self, table_name: str) -> List[Dict[str, Any]]:
        """테이블 인덱스 정보 조회"""
        async with aiosqlite.connect(self.db_path) as db:
            db.row_factory = aiosqlite.Row
            async with db.execute(
                """
                SELECT name, sql 
                FROM sqlite_master 
                WHERE type='index' 
                AND tbl_name=? 
                AND name NOT LIKE 'sqlite_%'
                """,
                (table_name,)
            ) as cursor:
                return [dict(row) for row in await cursor.fetchall()]

    async def get_table_count(self, table_name: str) -> int:
        """테이블 레코드 수 조회"""
        async with aiosqlite.connect(self.db_path) as db:
            async with db.execute(f"SELECT COUNT(*) as count FROM {table_name}") as cursor:
                row = await cursor.fetchone()
                return row[0] if row else 0