import streamlit as st
import requests
import json
import os
import time
from dotenv import load_dotenv
from query import *



load_dotenv()


def login(acc_no : int, password : str):
    r = requests.post(f"{base_url}/login", json={"acc_no" : acc_no, "password" : password})
    a = json.loads(r.text)
    if r.status_code == 200:
        if "logged_acc_no" not in st.session_state:           
            st.session_state["logged_acc_no"] = st.session_state["acc_no"]  
        if "fname" not in st.session_state:      
            st.session_state["fname"] =  a["name"]    
        if "lname" not in st.session_state:
            st.session_state["lname"] =  a["lastname"]  
        if "gender" not in st.session_state:  
            st.session_state["gender"] =  a["gender"]
        if "balance" not in st.session_state:
            st.session_state["balance"] =  a["Balance"]
        if "logged_password" not in st.session_state:
            st.session_state["logged_password"] = st.session_state["password"]
        st.session_state.logged_in = True
    elif r.status_code == 401:
        st.write("Wrong Password.")
        time.sleep(3)

    elif r.status_code == 404:
        st.error("Account Not found")
        time.sleep(3)
    else:
        st.error("Something went wrong")
        time.sleep(3)



def before_rerun():
    st.session_state["logged_acc_no"] = st.session_state["logged_acc_no"]        
    st.session_state["fname"] =  st.session_state["fname"]   
    st.session_state["lname"] =  st.session_state["lname"]    
    st.session_state["gender"] =  st.session_state["gender"]
    st.session_state["balance"] =  st.session_state["balance"]
    st.session_state["logged_password"] = st.session_state["logged_password"]
    st.session_state.logged_in = True
    st.rerun()


base_url = os.getenv("BASE_URL")
def logout():
    del st.session_state.logged_in
    del st.session_state.fname
    del st.session_state.lname
    del st.session_state.gender
    del st.session_state.balance
    del st.session_state.logged_password
    del st.session_state.logged_acc_no
    time.sleep(2)
    st.switch_page("home.py")


@st.dialog("Are you really want to delete your Account?")
def delete_acc(acc_no):
    st.write("To delete Account press Delete or cancel.")
    if st.button("delete"):
        d = requests.delete(f"{base_url}/delete_acc?acc_no={acc_no}")
        if d.status_code == 200:
            st.success("Your Account got deleted.")
            logout()
            time.sleep(5)
            st.switch_page("home.py")
        else:
            st.error(json.loads(d.text))
    if st.button("cancel"):
        before_rerun()


if "logged_in" not in st.session_state:
    st.session_state["logged_in"] = False

if st.session_state.logged_in :

    login(st.session_state.logged_acc_no, st.session_state.logged_password)

    st.write(f"Welcome {st.session_state.fname} {st.session_state.lname}!...")
    st.write(f"Your Account Number is  {st.session_state.logged_acc_no}")
    with st.expander("Check Your Balance"):
        bal = requests.get(f"{base_url}/show_balance?acc_no={st.session_state.logged_acc_no}")
        updated_balance = json.loads(bal.text)
        st.session_state.balance = updated_balance["balance"]
        st.success(f"Your Account Balance is {st.session_state.balance}")



    with st.expander("Update Account"):
        option = ["M", "F", "O"]
        match st.session_state.gender:
            case "M":
                ind = 0
            case "F":
                ind = 1
            case "O":
                ind = 2
        
        st.text_input("Enter new First name", value= st.session_state.fname, key= "new_fname")
        st.text_input("Enter new Last name", value= st.session_state.lname, key = "new_lname")
        st.radio("Gender", option , index= ind ,key= 'new_gender')
        # st.session_state.new_gender = st.session_state.gender
        st.text_input("Enter new Password", value= None, key="new_password", type="password")
        if st.button("Update"):
            payload = {"acc_no" : st.session_state["logged_acc_no"],
                        "fname" : st.session_state.new_fname,
                        "lname" : st.session_state.new_lname,
                        "gender" : st.session_state.new_gender,
                        "password" : st.session_state.new_password}
            r = requests.patch(f"{base_url}/update",json=payload)
            
            if r.status_code == 200:
                st.success("Details Update successfully...")
                st.write("login again")
                st.session_state.logged_in = False
                time.sleep(5)
                logout()
            

    with st.expander("Deposit"):
        st.number_input("Enter amount:- ", key = "deposit_amount")
        body = {
                "acc_no": st.session_state.logged_acc_no,
                "amount": st.session_state.deposit_amount
                }
        if st.button("Deposit"):
            p = requests.patch(f"{base_url}/deposit", json = body)
            
            if p.status_code == 200:
                st.success(json.loads(p.text)["detail"])
                time.sleep(3)
                before_rerun()
            else :
                res = json.loads(p.text)
                st.error(res["error"])

    with st.expander("Withdraw"):
        amount_withdraw =st.number_input("Enter amount:- ", key= "withdraw_amount")
        pass_withdraw = st.text_input("Enter your password.", key= "withdraw_password")
        # st.session_state.withdraw_amount = amount_withdraw
        # st.session_state.withdraw_password = pass_withdraw
        body = {"acc_no": st.session_state.logged_acc_no,
                "amount": st.session_state.withdraw_amount,
                "password": st.session_state.withdraw_password
                }
        
        but = st.button("withdraw")
        if but:
            p = requests.patch(f"{base_url}/withdraw", json= body)
            if p.status_code == 200:
                answer = json.loads(p.text)
                st.success(answer['detail'])
                time.sleep(3)
                before_rerun()
            else:
                answer = json.loads(p.text)
                st.error(answer['error'])
            
                
    with st.expander("Transaction History"):
        res = get_transaction_history(st.session_state.logged_acc_no)
        if len(res) == 0:
            st.write("No Transaction yet...")
        else:
            for i in res:
                st.write(i.tran_id, i.date, i.acc, i.amount, i.tran_type)



    with st.expander("Delete Account"):
        st.write(st.session_state.logged_acc_no)
        if st.button("Delete Account"):
            delete_acc(st.session_state.logged_acc_no)

                     

    log_out = st.button("Log out")
    if log_out:
        logout()
        

else:

    st.header("Login in bank")
    st.text_input("Enter Your Account no:-", key= "acc_no")
    st.text_input("Enter your password:-", type='password', key="password")

    
    if st.button("Login"):
        st.session_state.fname = get_fname(st.session_state.acc_no)

        login(st.session_state.acc_no, st.session_state.password)
        st.rerun()
        
        
        
