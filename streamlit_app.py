import streamlit as st
import datetime as dt
import time

st.set_page_config(layout="wide")

@st.dialog("だいあろぐ")
def show_dialog(input: str):
    st.text(input)


@st.fragment(run_every=1)
def clock():
    now = dt.datetime.now()
    st.write(now)


def render_sidebar():
    st.sidebar.title("さいどばー")
    input = st.sidebar.text_input("**input**")

    if st.sidebar.button("だいあろぐ"):
        show_dialog(input)



st.title("タイトル")
st.header("ヘッダー")

with st.empty():
    clock()

st.subheader("サブヘッダー")
st.write("hello streamlit")
st.code("""print('Hello world')""", "python")



render_sidebar()    








with st.empty():
    for seconds in range(10):
        st.write(f"⏳ {seconds} seconds have passed")
        time.sleep(1)
    st.write(":material/check: 10 seconds over!")
st.button("Rerun")
