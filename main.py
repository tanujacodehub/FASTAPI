from fastapi import FastAPI, Request,Form
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from fastapi.responses import RedirectResponse
from model import User
from utils.json_helper import read_data, write_data
import os
import json

app = FastAPI()

templates = Jinja2Templates(directory="templates")

app.mount("/static", StaticFiles(directory="static"), name="static")

########## list user ##########
@app.get("/")
def home(request: Request):          
        users = read_data()
        if not users:      # JSON empty
          data = []
        else:
          data = users

        return templates.TemplateResponse(
            "index.html",
            {
                "request": request,
                "users": data
            }
        )
    
###### calling User form #######
@app.get("/add")
def add_page(request: Request):
    return templates.TemplateResponse(
        "add.html",
        {"request": request}
    )

######### save User in json ###########
@app.post("/saveUser")
def add_user(name: str = Form(...), email: str = Form(...)):

    data = read_data()      
    # create id using length
    new_id = len(data) + 1
    # create user object
    user = {
        "id": new_id,
        "name": name,
        "email": email
    }

    # append to list
    data.append(user)

    # save json   
    write_data(data)

    return RedirectResponse(
    url=f"/?message=User added&id={new_id}",
    status_code=303
    )
########## Delete User ###########3
@app.get("/delete/{index}")
def delete_user(index: int):

    data = read_data()
    # check index exists
    if index >= len(data):
        return RedirectResponse(
            url="/?message=User not found",
            status_code=303
        )
    # delete user
    data.pop(index)

    # save updated list
    write_data(data)

    return RedirectResponse(
        url="/?message=User deleted",
        status_code=303
    )

###### calling edit user #######
@app.get("/edit/{index}")
def edit_page(request: Request, index: int):
    data = read_data()
    user = data[index]
    return templates.TemplateResponse(
        "edit.html",
        {"request": request, "user": user, "index": index}
    )

##### Edit user as per index  ###########
@app.post("/updateUser")
def update_user(
    index: int = Form(...),
    name: str = Form(...),
    email: str = Form(...)
):

    data = read_data()

    # check index exists
    if index >= len(data):
        return RedirectResponse(
            url="/?message=User not found",
            status_code=303
        )

    # update user
    data[index]["name"] = name
    data[index]["email"] = email

    # save json
    write_data(data)

    return RedirectResponse(
        url="/?message=User updated successfully",
        status_code=303
    )


