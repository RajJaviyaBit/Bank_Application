import streamlit as st
import requests
import time
from dotenv import load_dotenv
from query import final_acc_no
import os

load_dotenv()
def acc_created():
    # st.rerun()
    st.switch_page("pages/03_Login_Acc.py")
    st.rerun()

base_url = os.getenv("BASE_URL")

st.write("Bank Application")
st.header("Create Account")
final_account_no = final_acc_no() + 1
st.write(f"Your Account Number:- {final_account_no}.")
# st.number_input("Enter Your Account number", min_value= final_account_no, key = "acc_no" )

st.text_input(label = "Enter your First name" , key= "fname")

st.text_input("Enter Your last name", key = "lname")

st.radio("Gender", ["M", "F", "O"], key= 'gender')

st.number_input("Enter Intial balance", min_value=1000, key = "balance" )

st.text_input("Enter your password", type = "password", key = "password")

# st.write(f"Account no is {st.session_state.acc_no}, Firstname is {st.session_state.fname}, lastname is {st.session_state.lname}, Gender is {st.session_state.gender}, balance is {st.session_state.balance}, password is {st.session_state.password}.")


a = st.button("Submit")
if a:
    r = requests.post(f"{base_url}/create_acc", json={"acc_no" : final_account_no, "fname" : st.session_state.fname, "lname" : st.session_state.lname, "gender" : st.session_state.gender, "balance" : st.session_state.balance, "password" : st.session_state.password})
    st.write(r.status_code)
    # st.write(r.text)
    if r.status_code == 201:
        st.success("your account is created, you can login now.")
        st.write("you will be redirected to login")
        time.sleep(5)
        acc_created()
        