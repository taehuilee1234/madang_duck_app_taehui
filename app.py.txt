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
# 1) 고객조회 탭 (텍스트 입력 방식)
# =================================================
with tab1:
    st.subheader("고객명 입력하여 주문내역 조회")

    # 고객명 직접 입력
    input_name = st.text_input("고객명을 입력하세요", placeholder="예: 이태희")

    # 조회 버튼 클릭
    if st.button("조회하기"):
        if input_name.strip() == "":
            st.warning("고객명을 입력해주세요.")
        else:
            # 고객 존재 여부 확인
            customer_query = f"""
            SELECT * FROM Customer
            WHERE name = '{input_name}'
            """
            customer_result = conn.execute(customer_query).df()

            if customer_result.empty:
                st.error("해당 고객이 존재하지 않습니다.")
            else:
                st.success(f"'{input_name}' 고객 조회 결과")

                # 주문내역 조회
                order_query = f"""
                SELECT c.custid, c.name, b.bookname, o.orderdate, o.saleprice
                FROM Orders o
                JOIN Customer c ON o.custid = c.custid
                JOIN Book b ON o.bookid = b.bookid
                WHERE c.name = '{input_name}'
                ORDER BY o.orderdate DESC;
                """
                order_result = conn.execute(order_query).df()

                if order_result.empty:
                    st.info("해당 고객의 주문 내역이 없습니다.")
                else:
                    st.dataframe(order_result, use_container_width=True)

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

