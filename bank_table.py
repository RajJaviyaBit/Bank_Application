from sqlalchemy import ForeignKey, Column, String, Integer, CHAR, DateTime, Float
from sqlalchemy.ext.declarative import declarative_base

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
        



class Transaction(Base):
    __tablename__ = "transasction"

    tran_id = Column("transacton_id", Integer, primary_key= True, autoincrement= True)
    date = Column("date_of_transaction", DateTime)
    acc = Column("acc_no", Integer, ForeignKey(Accounts.acc_no))
    amount = Column("amount", Float)
    tran_type = Column("tran_type", String)
    balance = Column("balance", Float)
    
    
    def __init__(self, acc: int) -> None:
        self.acc = acc
