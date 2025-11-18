import streamlit as st
import duckdb
import pandas as pd

st.set_page_config(page_title="마당서점 시스템", layout="wide")

st.title("📚 마당서점 고객조회 & 거래내역")
st.write("### 👤 만든 사람: 이태희")

# DuckDB 메모리 DB 연결
conn = duckdb.connect()

# CSV 로드 → 테이블 생성
conn.execute("CREATE TABLE Customer AS SELECT * FROM read_csv_auto('Customer_madang.csv')")
conn.execute("CREATE TABLE Book AS SELECT * FROM read_csv_auto('Book_madang.csv')")
conn.execute("CREATE TABLE Orders AS SELECT * FROM read_csv_auto('Orders_madang.csv')")

# 탭 UI
tab1, tab2 = st.tabs(["고객조회", "거래 내역"])


# =================================================
# 1) 고객조회 탭
# =================================================
with tab1:
    st.subheader("고객명으로 주문 내역 조회")

    # 고객명 목록 불러오기
    name_list = conn.execute("SELECT DISTINCT name FROM Customer").df()["name"].tolist()

    # 기본 선택값 = '이태희' (너 요청)
    default_name = "이태희" if "이태희" in name_list else name_list[0]

    selected_name = st.selectbox("고객명", name_list, index=name_list.index(default_name))

    # 버튼
    if st.button("조회하기"):
        query = f"""
        SELECT c.custid, c.name, b.bookname, o.orderdate, o.saleprice
        FROM Orders o
        JOIN Customer c ON o.custid = c.custid
        JOIN Book b ON o.bookid = b.bookid
        WHERE c.name = '{selected_name}'
        ORDER BY o.orderdate DESC;
        """
        result = conn.execute(query).df()

        if result.empty:
            st.info("해당 고객의 주문 내역이 없습니다.")
        else:
            st.dataframe(result, use_container_width=True)


# =================================================
# 2) 거래 내역 탭
# =================================================
with tab2:
    st.subheader("전체 거래 내역 조회")

    full_query = """
    SELECT o.orderid, c.name AS 고객명, b.bookname AS 도서명, 
           o.saleprice AS 판매가, o.orderdate AS 주문일
    FROM Orders o
    JOIN Customer c ON o.custid = c.custid
    JOIN Book b ON b.bookid = o.bookid
    ORDER BY o.orderid DESC;
    """

    df_full = conn.execute(full_query).df()

    st.dataframe(df_full, use_container_width=True)

