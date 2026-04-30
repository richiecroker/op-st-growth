import streamlit as st
import duckdb

DB_PATH = "data.duckdb"
CSV_PATH = "prescribing.csv"
TABLE_NAME = "prescribing"


def db_needs_init(con):
    result = con.execute(
        f"SELECT COUNT(*) FROM information_schema.tables WHERE table_name = '{TABLE_NAME}'"
    ).fetchone()
    return result[0] == 0


def init_db(con):
    con.execute(f"""
        CREATE TABLE {TABLE_NAME} AS
        SELECT * FROM read_csv_auto('{CSV_PATH}')
    """)


@st.cache_resource
def get_connection():
    con = duckdb.connect(DB_PATH)
    if db_needs_init(con):
        init_db(con)
    return con


con = get_connection()

# Guard for when the cache survives but the DB file was wiped
if db_needs_init(con):
    init_db(con)
