from sqlalchemy import ForeignKey, Column, String, Integer, CHAR, DateTime, Float
from sqlalchemy.ext.declarative import declarative_base
from datetime import datetime
from postgresconnector import connect
from fastapi.responses import JSONResponse
from fastapi import  HTTPException

Base = declarative_base()


class Accounts(Base):
    __tablename__ = "accounts"

    acc_no = Column("acc_no", Integer, primary_key =True )
    fname = Column( "firstname", String)
    lname = Column("lastname", String)
    gender = Column("gender", CHAR)
    balance = Column("balance", Float)
    password = Column("password", String , nullable= False)

    def __init__(self, acc_no: int, fname: str, lname : str, gender: str , balance: int,password: str) -> None:
        """
        Intialise method to store variable for object.
        variable acc_no is for storing Account No,
        variable fname is for storing First name of customer,
        variable lname is for storng last name of customer,
        varible gender is for storing GENDER of the Customer like "M" for Male, "F" for Female, "O" for OTHER.
        varible balance is for storing balance of customer,
        variable password is storing Password for the account of the customer               
        """
        self.acc_no = acc_no 
        self.fname = fname
        self.lname = lname
        self.gender = gender
        self.balance = balance
        self.password = password
        
    def show_balance(self) -> int:

        """
        This method is getter method for balance.
        
        It returns the balance of the object that 
        
        """
        return self.balance



class Transaction(Base):
    __tablename__ = "transasction"

    tran_id = Column("transacton_id", Integer, primary_key= True, autoincrement= True)
    date = Column("date_of_transaction", DateTime)
    acc = Column("acc_no", Integer, ForeignKey(Accounts.acc_no))
    amount = Column("amount", Float)
    tran_type = Column("tran_type", String)
    
    
    def __init__(self, acc: int) -> None:
        self.acc = acc

    def deposite(self, amount: int) -> str:

        """
        Deposite Method is for Deposite of Amount that is varible,
        amount is deposited in Account that object on which this method is called.

        It expect Interger as amount parameter.

        It stores Transaction Type, Transaction Date time, Transaction ID and Update balance in database.        
        
        After calling this method make sure to close session.
        """
        session = connect()
        self.tran_type = "deposit"
        self.date = datetime.now()
        self.amount = amount
        result = session.query(Accounts).filter(Accounts.acc_no == self.acc)
        self.balance = result[0].balance + self.amount
        session.query(Accounts).filter(Accounts.acc_no == self.acc).update({Accounts.balance : self.balance})
        session.commit()

        return f"{amount} is deposited, Your balance is {self.balance}"

    def withdraw(self, amount : int, password : str) -> str:
        """
        withdraw Method is for withdrawal of Amount that is varible,
        amount will widrawal from the Account that object on which this method is called.

        It expect Interger as amount parameter.

        If withdrawal amount is lesser then balance then It will ask for password of the account.

        If the password is correct then withdrawal will be successful.

        On successful withdrawal, It stores Transaction Type, Transaction Date time, Transaction ID and Update balance in database.        
        
        After calling this method make sure to close session.
        """
        session = connect()
        result = session.query(Accounts).filter(Accounts.acc_no == self.acc)
        self.date = datetime.now()
        self.amount = amount
        if amount < result[0].balance:           
            if password == result[0].password:
                self.tran_type = "withdraw"
                self.balance = result[0].balance - self.amount
                session.query(Accounts).filter(Accounts.acc_no == self.acc).update({Accounts.balance : self.balance})
                session.add(self)
                session.commit()
                session.close()
                return JSONResponse(content={"detail": f"{amount} withdraw successfully, Your balance is {self.balance}."}, status_code=200)
            else:
                self.tran_type = "unsuccessfull as wrong password"
                raise HTTPException(status_code=401, detail= "wrong password" )
                
        else: 
            self.tran_type = "unsuccessful as amount is more than bal."
            raise HTTPException(status_code=406, detail="Withdrawal amount is more than balance...")
            # return JSONResponse(content={"detail":"Withdrawal amount is more than balance..." }, status_code=406)
        