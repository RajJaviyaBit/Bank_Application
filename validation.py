from pydantic import BaseModel, Field
from typing import Annotated, Literal, Optional

class bankacc(BaseModel):
    acc_no: Annotated[int, Field(..., descreption = " Account Number is Integer value", examples= [1001, 1002])]
    fname: Annotated[str, Field(..., descreption = " Enter Your First Name ", examples = ["John"])]
    lname: Annotated[str, Field(..., descreption = " Enter Your Last Name ", examples= ["Doe"])]
    gender: Annotated[Literal["M", "F", "O"], Field(..., descreption = " Enter Your Gender", examples= ["M", "F", "O"])]
    balance : Annotated[float, Field(..., descreption = " Enter Balance amount", examples= [10000, 20000])]
    password : Annotated[str, Field(..., descreption = " Enter Your password for transaction This can be str ", examples= ["PASSWORD"])]

class Account_No(BaseModel):
    acc_no : Annotated[int, Field(..., descreption = " Account Number is Integer value", examples= [1001, 1002])]

class Update(BaseModel):
    acc_no : Annotated[int, Field(..., descreption = " Account Number is Integer value", examples= [1001, 1002])]
    fname : Annotated[Optional[str] ,  Field( default = None  ,  descreption = " Enter Your First Name", examples = ["John"])]
    lname: Annotated[Optional[str] ,  Field( default = None  ,  descreption = " Enter Your Last Name", examples = ["Doe"])]
    gender: Annotated[Optional[Literal["M", "F", "O"]] ,  Field( default = None  ,  descreption = " Enter Your Gender", examples = ["M", "F"])]
    password: Annotated[Optional[str] ,  Field(default = None  ,  descreption = " Enter Your password", examples = ["John"])]

class deatil(BaseModel):
    acc_no : Annotated[int, Field(..., descreption = " Account Number is Integer value", examples= [1001, 1002])]
    fname : Annotated[str, Field(..., descreption = " Enter Your First Name ", examples = ["John"])]
    lname : Annotated[str, Field(..., descreption = " Enter Your Last Name ", examples= ["Doe"])]

class acc_deposite(BaseModel):
    acc_no :Annotated[int, Field(..., description="Enter Your Account No", examples= [1010, 1020])]
    amount : Annotated[int, Field(..., description="Enter Amount you wamt to deposite", examples= [1000, 2000])]
class acc_withdraw_validation(BaseModel):
    acc_no :Annotated[int, Field(..., description="Enter Your Account No", examples= [1010, 1020])]
    amount : Annotated[int, Field(..., description="Enter Amount you wamt to deposite", examples= [1000, 2000])]
    password: Annotated[str ,  Field(...,  descreption = " Enter Your password", examples = ["WITHDRAW"])]
class login_acc(BaseModel):
    acc_no :Annotated[int, Field(..., description="Enter Your Account No", examples= [1010, 1020])]
    password: Annotated[str ,  Field(...,  descreption = " Enter Your password", examples = ["LOGIN"])]