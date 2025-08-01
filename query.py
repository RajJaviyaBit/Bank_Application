from postgresconnector import connect
from bank_table import Accounts, Transaction
from validation import *
from datetime import datetime
from fastapi.responses import JSONResponse
from fastapi import HTTPException
session = connect()


def fetch_all_acc():
    result = session.query(Accounts).all()
    return result
    

def fetch_acc(acc: int):
    result = session.query(Accounts).filter(Accounts.acc_no == acc).first()
    return result


def update_Account(b : Update):
    
    if b.fname is not None:
        session.query(Accounts).filter(Accounts.acc_no == b.acc_no).update({Accounts.fname : b.fname})
        session.commit()
      
    if b.lname is not None:
        session.query(Accounts).filter(Accounts.acc_no == b.acc_no).update({Accounts.lname : b.lname})
        session.commit()
       
    if b.gender is not None:
        session.query(Accounts).filter(Accounts.acc_no == b.acc_no).update({Accounts.gender : b.gender})
        session.commit()
   
    if b.password is not None:
        session.query(Accounts).filter(Accounts.acc_no == b.acc_no).update({Accounts.password : b.password})
        session.commit()
    
    
def create_acc(acc : bankacc):
    Acc = Accounts(acc.acc_no, acc.fname, acc.lname,acc.gender, acc.balance, acc.password)
    session.add(Acc)
    session.commit()
    


def balance_getter(acc_no : int):
    bal  = session.query(Accounts.balance).filter(Accounts.acc_no == acc_no).first()
    return bal[0]


def final_acc_no():
    last_acc_no = session.query(Accounts.acc_no).order_by(Accounts.acc_no.desc()).first()
    return last_acc_no[0]


def delete_acc(acc_no):
    result = fetch_acc(acc_no)
    r = session.query(Transaction).filter(Transaction.acc == acc_no).all()
    for i in r:
        session.delete(i)
        session.commit()            
    session.delete(result)
    session.commit()



def deposit(dep : acc_deposite):

    """
    Deposite Method is for Deposite of Amount that is varible,
    amount is deposited in Account that object on which this method is called.
    It expect Interger as amount parameter.
    It stores Transaction Type, Transaction Date time, Transaction ID and Update balance in database.        
    
    After calling this method make sure to close session.
    """
    t = Transaction(dep.acc_no)
    t.tran_type = "deposit"
    t.date = datetime.now()
    t.amount = dep.amount
    result = fetch_acc(dep.acc_no)
    t.balance = result.balance + t.amount
    session.query(Accounts).filter(Accounts.acc_no == t.acc).update({Accounts.balance : t.balance})
    session.add(t)
    session.commit()

    return f"{t.amount} is deposited, Your balance is {t.balance}"

    

def withdraw_func(withdraw :acc_withdraw_validation):
    """
        withdraw Method is for withdrawal of Amount that is varible,
        amount will widrawal from the Account that object on which this method is called.

        It expect Interger as amount parameter.

        If withdrawal amount is lesser then balance then It will ask for password of the account.

        If the password is correct then withdrawal will be successful.

        On successful withdrawal, It stores Transaction Type, Transaction Date time, Transaction ID and Update balance in database.        
        
        After calling this method make sure to close session.
        """
        
    t = Transaction(withdraw.acc_no)
    result = fetch_acc(withdraw.acc_no)
    t.date = datetime.now()
    t.amount = withdraw.amount
    if withdraw.amount < result.balance:           
        if withdraw.password == result.password:
            t.tran_type = "withdraw"
            t.balance = result.balance - t.amount
            
            session.query(Accounts).filter(Accounts.acc_no == t.acc).update({Accounts.balance : t.balance})
            session.add(t)
            session.commit()
            
            return JSONResponse(content={"detail": f"{t.amount} withdraw successfully, Your balance is {t.balance}."}, status_code=200)
        else:
            t.tran_type = "unsuccessfull as wrong password"
            t.balance = result.balance 
            session.add(t)
            session.commit()
            raise HTTPException(status_code=401, detail= "wrong password" )
            
    else: 
        t.tran_type = "unsuccessful as amount is more than bal."
        t.balance = result.balance 
        session.add(t)
        session.commit()
       
        raise HTTPException(status_code=406, detail="Withdrawal amount is more than balance...")

        


def get_fname(acc_no: int):
    a = session.query(Accounts.fname).filter(Accounts.acc_no == acc_no).first()
    return a[0]


def get_transaction_history(acc_no : int):
    result = session.query(Transaction).filter(Transaction.acc == acc_no).all()
    return result

session.close()