# SQLite Database Metadata MCP Server

MCP(Model Context Protocol)를 사용하여 SQLite 데이터베이스의 메타데이터를 조회할 수 있는 서버입니다.

## 기능

- 테이블 목록 조회
- 테이블 컬럼 정보 조회
- 테이블 인덱스 정보 조회
- 테이블 레코드 수 조회

## 설치

```bash
# 기본 의존성 설치
pip install -r requirements.txt

# 웹 서버 의존성 설치 (선택사항)
pip install -r web_requirements.txt
```

## 실행

### MCP 서버 실행
```bash
python main.py
```

### 샘플 데이터 추가
```bash
python insert_sample_data.py
```

### 웹 문서 서버 실행 (선택사항)
```bash
python web_server.py
```
웹 서버 실행 후 http://localhost:8080 에서 문서를 확인할 수 있습니다.

## MCP 도구

1. `get_table_info`: 테이블의 상세 정보 조회
2. `get_table_count`: 테이블의 레코드 수 조회

## 예제 사용법

```
테이블 정보를 조회해주세요.
> get_table_info table_name=users

테이블의 레코드 수를 알려주세요.
> get_table_count table_name=users
```

## 라이선스

MIT License