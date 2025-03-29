import json
import streamlit as st
from mysql.mysql import MySQLClient
from config import *


def main():
    st.title("Check Data in Database")
    client = MySQLClient()

    rows = st.number_input("select rows", min_value=1, value=5, step=1)
    if st.button(label=":dvd: Select from Database"):
        st.header("Result")
        res = client.select(rows)
        for r in res:
            if r["created_at"] is not None:
                r["created_at"] = r["created_at"].strftime("%Y-%m-%d %H:%M:%S.%f")
        # st.write(res)
        with open("index.json", "w", encoding="utf-8") as f:
            json.dump(res, f, indent=4, ensure_ascii=False)

    st.write("You can select tables from below")
    st.write(TABLES)

    query = st.text_area("input query here", placeholder="select * from lcc limit 1")
    if st.button(":dvd: Select by query"):
        st.header("Result")
        st.write(client.select_with_query(query))


if __name__ == "__main__":
    main()
