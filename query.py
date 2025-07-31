from postgresconnector import connect
from bank_table import Accounts, Transaction
from validation import *
# import sqlalchemy


def fetch_all_acc():
    session = connect()
    result = session.query(Accounts).all()
    session.close()
    return result
    

def fetch_acc(acc: int):
    session = connect()
    result = session.query(Accounts).filter(Accounts.acc_no == acc).first()
    session.close()
    return result


def update_Account(b : Update):
    session = connect()
    if b.fname is not None:
        session.query(Accounts).filter(Accounts.acc_no == b.acc_no).update({Accounts.fname : b.fname})
      
    if b.lname is not None:
        session.query(Accounts).filter(Accounts.acc_no == b.acc_no).update({Accounts.lname : b.lname})
       
    if b.gender is not None:
        session.query(Accounts).filter(Accounts.acc_no == b.acc_no).update({Accounts.gender : b.gender})
   
    if b.password is not None:
        session.query(Accounts).filter(Accounts.acc_no == b.acc_no).update({Accounts.password : b.password})
    session.commit()
    session.close()


def create_acc(acc : bankacc):
    Acc = Accounts(acc.acc_no, acc.fname, acc.lname,acc.gender, acc.balance, acc.password)
    session = connect()
    session.add(Acc)
    session.commit()
    session.close()


def balance_getter(acc_no : int):
    db = connect()
    bal  = db.query(Accounts.balance).filter(Accounts.acc_no == acc_no).first()
    db.commit()
    db.close()
    return bal[0]


def final_acc_no():
    db = connect()
    last_acc_no = db.query(Accounts.acc_no).order_by(Accounts.acc_no.desc()).first()
    db.commit()
    db.close()
    return last_acc_no[0]


def delete_acc(acc_no):
    result = fetch_acc(acc_no)
    db = connect()
    r = db.query(Transaction).filter(Transaction.acc == acc_no).all()

    for i in r:
        db.delete(i)            
    db.commit()
    db.delete(result)
    db.commit()


def deposit(dep : acc_deposite):
    db =connect()
    t = Transaction(dep.acc_no)
    a = t.deposite(dep.amount)
    db.add(t)
    db.commit()
    db.close()
    return a


def withdraw_func(withdraw :acc_withdraw_validation):
    db = connect()
    t = Transaction(withdraw.acc_no)
    a = t.withdraw(withdraw.amount, withdraw.password)
    db.commit() 
    db.close()                 
    return a


def get_fname(acc_no: int):
    db = connect()
    a = db.query(Accounts.fname).filter(Accounts.acc_no == acc_no).first()
    db.close()
    return a[0]