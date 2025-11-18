import streamlit as st
import duckdb
import pandas as pd

st.title("📚 마당서점 DuckDB Web App")

# DuckDB 연결 (동일 폴더에 madang.db 있어야 함)
conn = duckdb.connect("madang.db", read_only=True)

default_query = "SELECT * FROM Customer LIMIT 10"

query = st.text_area("SQL 쿼리를 입력하세요", default_query, height=150)

if st.button("실행"):
    try:
        df = conn.sql(query).df()
        st.success("쿼리 성공!")
        st.dataframe(df)
    except Exception as e:
        st.error(f"에러 발생: {e}")
