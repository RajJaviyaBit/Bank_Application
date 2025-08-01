from fastapi import FastAPI,  HTTPException, status, responses, Depends
from validation import *
from loggerfile import log_func
from query import *

logger = log_func()

app = FastAPI()


@app.get("/")
def welcome() -> dict:
    return {"message": "welcome to Bank"}


@app.post("/create_acc" , status_code=status.HTTP_201_CREATED )
def acc_creation(acc : bankacc):
    """
    This function is for creating acc is accept Acc_no in Interger, first name, last name in string, Gender Male as "M", Female as "F" and Other as "O",
    balance as Integer and password as String.
    """

    try:
        result = fetch_acc(acc.acc_no)
        
        if result == None:
            create_acc(acc)
            logger.info("While hitting /create_acc API:  Acc created")
     
            return {"detail" :{"message" :  "Account Creation Successfully..."}}

        else:
            raise HTTPException(status_code = status.HTTP_409_CONFLICT, detail= {"error" : "Account no is already allocated..."})

    except HTTPException as e:
        logger.error(f"While hitting /create_acc API: {e}")
        return responses.JSONResponse(status_code=status.HTTP_409_CONFLICT, content={"error": "Account no is already allocated..."})
        
    
    except Exception as e:
        logger.error(f"While hitting /create_acc API: {e}")
        return responses.JSONResponse(status_code=500, content= {"error": "Error in server"})


#login
@app.post("/login")
def login(login_acc : login_acc) -> dict:
    try:
        result = fetch_acc(login_acc.acc_no)
        if result == None:
            raise HTTPException(status_code = status.HTTP_404_NOT_FOUND, detail = {"error": "Account is not Found..."})
        

        a = result
        if login_acc.password == a.password:
            res = {
                    "acc": a.acc_no,
                    "name" : a.fname,
                    "lastname": a.lname,
                    "gender": a.gender,
                    "Balance": a.balance
                    }
            logger.info(f"While hitting /login API :- Account no {a.acc_no} is logged in...")
            return res
        else:
            print("If wrong pass")
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail= {"error": "Wrong password"})
            
    except HTTPException as e:
        logger.error(f"While hitting /login API:- {str(e)}")
        return  responses.JSONResponse(status_code=e.status_code , content=str(e))

    except Exception as e:
        logger.error(f"While hitting /login API :- {str(e)}")
        return responses.JSONResponse(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, content={"error": str(e)})
     
        


@app.patch("/update")
def update_acc(a : Update) -> dict:   
    try:
        result = fetch_acc(a.acc_no)
        if result == None:
            raise HTTPException(status_code = status.HTTP_404_NOT_FOUND, detail = "Account is not Found...")
        
        update_Account(a)
       
        logger.info(f"While hitting /update API:- Account {a.acc_no} Updated...")
        return {"Message": "Table Updated Successfully..."}
    except HTTPException as e:
        logger.error(f"While hitting /update API:- {e}")
        return responses.JSONResponse(f"{e}", status_code= status.HTTP_404_NOT_FOUND)
    except Exception as e:
        logger.error(f"While hitting /update API:- {e}")
        return responses.JSONResponse(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, content=f"{e}")
        
            

@app.delete("/delete_acc")
def del_acc(acc_no : int) -> dict:
    try:

        result = fetch_acc(acc_no)
        if result == None:
            raise HTTPException(status_code = status.HTTP_404_NOT_FOUND, content = "Account is not Found...")

        else:
            delete_acc(acc_no=acc_no)
            logger.info(f"While hitting /delete API:- Account {result.acc_no} Deleted...")

            return {"message": "Your Account got deleted...."}
    except HTTPException as e:
        logger.error(f"While hitting /delete API:- {str(e)}")
        return responses.JSONResponse(status_code=status.HTTP_404_NOT_FOUND, content=f"{str(e)}")
    except Exception as e:
        logger.error(f"While hitting /delete API:- {str(e)}")
        return responses.JSONResponse(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, content=f"{str(e)}")



@app.patch("/deposit")
def account_deposite(dep : acc_deposite):
    try:
        result = fetch_acc(dep.acc_no)
        if result == None:
            raise HTTPException(status_code = status.HTTP_404_NOT_FOUND, detail= "Account is not Found...")
        
        a = deposit(dep)
        logger.info(f"While hitting /deposite API:- Account no {dep.acc_no} is deposited with {dep.amount}")
        return responses.JSONResponse(status_code=status.HTTP_200_OK, content= {"detail": a})

    except HTTPException as e:
        logger.error(f"While hitting /deposite API:- {e}")
        return responses.JSONResponse(status_code=status.HTTP_404_NOT_FOUND, content={"error" :str(e)})
  
    except Exception as e:
        logger.error(f"While hitting /deposite API:- {e}")
        return responses.JSONResponse(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, content={"error" :str(e)})
    
    

@app.patch("/withdraw")
def acc_withdraw(withdraw : acc_withdraw_validation) -> dict:
    try:
        result = fetch_acc(withdraw.acc_no)
        if result == None:
            raise HTTPException(status_code = status.HTTP_404_NOT_FOUND, detail = "Account is not Found...")
        else:
            a = withdraw_func(withdraw)         
            logger.info(f"While hitting /withdraw API:- {a}")
            return a
 
    except HTTPException as e:
        logger.error(f"While hitting /withdraw API:- {e}")
        return responses.JSONResponse(status_code=status.HTTP_404_NOT_FOUND, content={"error": str(e)})
  
    except Exception as e:
        logger.error(f"While hitting /withdraw API:- {e}")
        return responses.JSONResponse(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, content={"error" :str(e)})
    
@app.get("/show_balance")
def get_balance(acc_no :int):
    try:
        bal = balance_getter(acc_no)
        logger.info(f"balance getter api hitted success fully. {acc_no} has {bal}.")
        return responses.JSONResponse(status_code=status.HTTP_200_OK, content={"balance": bal})
    except Exception as e:
        logger.error(f"While hitting get_balance API:- {str(e)}")
        

@app.get("/tran_hist")
def transaction(acc : int):
    try:
        res = get_transaction_history(acc)
        logger.info(f"While hitting tran_hist API:- {acc}'s history fetched successfully.")
        return res
    except Exception as e:
        logger.error(f"While hitting tran_hist API:- {acc}'s tran history error :- {str(e)}")
