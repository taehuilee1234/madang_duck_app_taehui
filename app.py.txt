import streamlit as st
import pymysql
import pandas as pd

# DB 연결
dbConn = pymysql.connect(
    user='root', passwd='1234', host='localhost',
    db='madang', charset='utf8'
)
cursor = dbConn.cursor(pymysql.cursors.DictCursor)

st.title("고객 조회 & 거래 내역 시스템")

tab1, tab2 = st.tabs(["고객조회", "거래 입력"])

# ---------------------------
#  고객명 목록 불러오기
# ---------------------------
cursor.execute("SELECT name FROM Customer")
name_list = [row['name'] for row in cursor.fetchall()]

# 기본값을 첫 번째 고객으로 설정
selected_name = tab1.selectbox("고객명", name_list)

# ---------------------------
#  고객 거래 내역 조회
# ---------------------------
if selected_name:
    sql = """
        SELECT c.custid, c.name, b.bookname, o.orderdate, o.saleprice
        FROM Customer c, Book b, Orders o
        WHERE c.custid = o.custid
          AND o.bookid = b.bookid
          AND c.name = %s;
    """
    cursor.execute(sql, (selected_name,))
    result = cursor.fetchall()

    df = pd.DataFrame(result)
    if df.empty:
        tab1.write("해당 고객의 주문 내역이 없습니다.")
    else:
        tab1.dataframe(df)
