import streamlit as st
import duckdb

st.set_page_config(page_title="마당서점", layout="wide")

st.title("📚 마당서점 DuckDB Web App")
st.write("### 👤 만든 사람: 이태희")

# DuckDB in-memory
conn = duckdb.connect()

# CSV → Table (자동 생성)
conn.execute("CREATE TABLE Customer AS SELECT * FROM read_csv_auto('Customer_madang.csv')")
conn.execute("CREATE TABLE Book AS SELECT * FROM read_csv_auto('Book_madang.csv')")
conn.execute("CREATE TABLE Orders AS SELECT * FROM read_csv_auto('Orders_madang.csv')")

# 탭 생성
tab1, tab2 = st.tabs(["고객조회", "거래 입력"])

# -------------------------
# 1) 고객조회 탭
# -------------------------
with tab1:
    st.subheader("고객명으로 주문내역 조회하기")

    customer_name = st.text_input("고객명", placeholder="이윤행 등 입력")

    if st.button("조회하기"):
        if customer_name.strip() == "":
            st.warning("고객명을 입력하세요.")
        else:
            # 고객 존재 여부 확인
            customer_query = f"""
            SELECT * FROM Customer
            WHERE name = '{customer_name}'
            """
            customer_result = conn.execute(customer_query).df()

            if customer_result.empty:
                st.error("해당 고객이 존재하지 않습니다.")
            else:
                st.success(f"'{customer_name}' 고객이 조회되었습니다.")

                # 주문 내역 조회
                order_query = f"""
                SELECT o.orderid, o.custid, o.bookid, o.saleprice, o.orderdate, b.bookname
                FROM Orders o
                JOIN Book b ON o.bookid = b.bookid
                JOIN Customer c ON o.custid = c.custid
                WHERE c.name = '{customer_name}'
                """
                order_result = conn.execute(order_query).df()

                if order_result.empty:
                    st.info("해당 고객의 주문 내역이 없습니다.")
                else:
                    st.write("### 📦 주문 내역")
                    st.dataframe(order_result, use_container_width=True)

# -------------------------
# 2) 거래입력 탭 (기본 틀만 제공)
# -------------------------
with tab2:
    st.subheader("거래 입력 (구현 예정)")
    st.info("이 기능은 아직 준비 중입니다.")
