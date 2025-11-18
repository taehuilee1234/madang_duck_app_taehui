import streamlit as st
import duckdb

st.title("📚 마당서점 DuckDB Web App")

# DuckDB 메모리 DB 생성
conn = duckdb.connect()

# CSV → 테이블 자동 생성
conn.execute("CREATE TABLE Customer AS SELECT * FROM read_csv_auto('Customer_madang.csv')")
conn.execute("CREATE TABLE Book AS SELECT * FROM read_csv_auto('Book_madang.csv')")
conn.execute("CREATE TABLE Orders AS SELECT * FROM read_csv_auto('Orders_madang.csv')")

st.write("### SQL 쿼리를 입력하세요")

default_query = "SELECT * FROM Customer LIMIT 10"
query = st.text_area("", default_query, height=150)

if st.button("실행"):
    try:
        df = conn.execute(query).df()
        st.dataframe(df)
    except Exception as e:
        st.error(f"에러: {e}")
