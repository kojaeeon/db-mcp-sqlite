from mcp.server import Server
from mcp.types import Resource, Tool, TextContent
from db_meta import DatabaseMetaService

class DBMetaServer:
    def __init__(self, db: DatabaseMetaService):
        self.db = db
        self.server = Server("db-meta-server")

    def setup_handlers(self):
        """MCP 핸들러 설정"""
        @self.server.list_resources()
        async def list_resources() -> list[Resource]:
            tables = await self.db.get_tables()
            return [
                Resource(
                    uri=f"table://{table['name']}",
                    name=table['name'],
                    mimeType="application/json",
                    description=f"Table: {table['name']}"
                )
                for table in tables
            ]

        @self.server.read_resource()
        async def read_resource(uri: str) -> str:
            table_name = uri.split("://")[-1]
            info = await self.db.get_table_info(table_name)
            indexes = await self.db.get_indexes(table_name)
            count = await self.db.get_table_count(table_name)
            
            result = {
                "table_name": table_name,
                "columns": info,
                "indexes": indexes,
                "record_count": count
            }
            import json
            return json.dumps(result, indent=2)

        @self.server.list_tools()
        async def list_tools() -> list[Tool]:
            return [
                Tool(
                    name="get_table_info",
                    description="테이블의 상세 정보를 조회합니다",
                    inputSchema={
                        "type": "object",
                        "properties": {
                            "table_name": {"type": "string"}
                        },
                        "required": ["table_name"]
                    }
                ),
                Tool(
                    name="get_table_count",
                    description="테이블의 레코드 수를 조회합니다",
                    inputSchema={
                        "type": "object",
                        "properties": {
                            "table_name": {"type": "string"}
                        },
                        "required": ["table_name"]
                    }
                )
            ]

        @self.server.call_tool()
        async def call_tool(name: str, arguments: dict) -> list[TextContent]:
            if name == "get_table_info":
                table_name = arguments["table_name"]
                info = await self.db.get_table_info(table_name)
                return [TextContent(
                    type="text",
                    text=f"테이블 '{table_name}'의 컬럼 정보:\n" + 
                         "\n".join([f"- {col['name']}: {col['type']}" for col in info])
                )]

            elif name == "get_table_count":
                table_name = arguments["table_name"]
                count = await self.db.get_table_count(table_name)
                return [TextContent(
                    type="text",
                    text=f"테이블 '{table_name}'의 레코드 수: {count}"
                )]

            raise ValueError(f"Unknown tool: {name}")

    async def run(self):
        """서버 실행"""
        from mcp.server.stdio import stdio_server
        self.setup_handlers()
        async with stdio_server() as (reader, writer):
            await self.server.run(reader, writer, initialization_options={})