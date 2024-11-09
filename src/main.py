from datetime import datetime
from uuid import uuid4

from PIL import Image
from fastapi.security import OAuth2PasswordRequestForm
from replit.web import User
from starlette import status


from fastapi import Form, Depends, HTTPException
from fastapi.openapi.docs import get_swagger_ui_html
from fastapi_sqlalchemy import DBSessionMiddleware, db
from starlette.responses import JSONResponse


from .bd.models import Images as ModelImages
from .bd.models import User as ModelUser
from .bd.schema import Name as SchemaName
from .bd.schema import Id as SchemaId
from .bd.schema import Update as SchemaUpdate
from .bd.schema import UserAuth
from .bd.schema import TokenSchema

import logging
import sys

import os
from dotenv import load_dotenv

from fastapi import FastAPI, UploadFile

from .deps import get_current_user
from .utils import (get_hashed_password, verify_password, create_access_token,
                    create_refresh_token)

from .rabbitMQ.send import (input_rabbitMQ, post_rabbitMQ, del_rabbitMQ,
                            put_rabbitMQ)

from .config import DB_USER, DB_PASS, DB_HOST, DB_PORT, DB_NAME


BASE_DIR = os.path.dirname(__file__)

load_dotenv(os.path.join(BASE_DIR, '.env'))

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)
stream_handler = logging.StreamHandler(sys.stdout)
log_formatter = logging.Formatter(
    "%(asctime)s [%(processName)s: %(process)d] [%(threadName)s: %(thread)d] "
    "[%(levelname)s] %(name)s: %(message)s")
stream_handler.setFormatter(log_formatter)
logger.addHandler(stream_handler)

logger.info('API is starting up')

app = FastAPI()  # noqa: pylint=invalid-name

DATABASE_URL = f"postgresql://{DB_USER}:{DB_PASS}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
app.add_middleware(DBSessionMiddleware, db_url=DATABASE_URL)

@app.get("/docs")
def read_docs():
    return get_swagger_ui_html(openapi_url="/openapi.json")

@app.post('/signup', summary="Create new user")
async def create_user(data: UserAuth):
    # querying database to check if user already exist
    user = db.session.query(ModelUser).filter(ModelUser.email ==
                                              data.email).first()
    if user is not None:
            raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="User with this email already exist"
        )
    user = ModelUser(user_id=uuid4(), email=data.email, password =
    get_hashed_password(data.password))
    db.session.add(user)
    db.session.commit()
    return user


@app.post('/login', summary="Create access and refresh tokens for user",
          response_model=TokenSchema)
async def login(form_data: OAuth2PasswordRequestForm = Depends()):
    user = db.session.query(ModelUser).filter(ModelUser.email ==
                                              form_data.username).first()
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Incorrect email or password"
        )

    hashed_pass = user.password
    if not verify_password(form_data.password, hashed_pass):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Incorrect email or password"
        )
    return {
        "access_token": create_access_token(user.email),
        "refresh_token": create_refresh_token(user.email),
    }


def processing_image(file):
    data = {}
    now = datetime.now()
    dt_string = now.strftime("%d/%m/%Y %H:%M:%S")
    with Image.open(file.file) as img:
        image_file = img.convert('L')
        image_file = image_file.resize((500,500))
        image_file.save(f'images\\500x500{file.filename}')
        data[0] = [f"images\\500x500{file.filename}", dt_string,
                   file.filename.split('.')[1], "500x500"]

        image_file = image_file.resize((100,100))
        image_file.save(f'images\\100x100{file.filename}')
        data[1] = [f"images\\100x100{file.filename}", dt_string,
                   file.filename.split('.')[1], "100x100"]
    return data

@app.post("/image")
async def add_image(file: UploadFile, text: str = Form(...),
                    user: User = Depends(get_current_user)):
    try:
        if (file.filename.split('.')[1] == 'jpg' or
                file.filename.split('.')[1] == 'png'):
            data = processing_image(file)


            sh = SchemaName(name=text)

            db_book0 = ModelImages(name=sh.name, path=data[0][0],
                                   data=data[0][1], permission=data[0][2],
                                   size=data[0][3])
            db_book1 = ModelImages(name=sh.name, path=data[1][0],
                                   data=data[1][1], permission=data[1][2],
                                   size=data[1][3])
            db.session.add(db_book0)
            db.session.add(db_book1)
            db.session.commit()

            response = post_rabbitMQ(data)
            return {"message": "Photo saved successfully",
                    "data": response}
        else:
            return JSONResponse(status_code=400,
                                content={"message": "Photo saved error. "
                                                    "Incorrect image format"})
    except:
        return JSONResponse(status_code=400,
                            content={"message": "Photo saved error"})


@app.get("/image")
async def list_image(user: User = Depends(get_current_user)):
    # try:
    bd_data = db.session.query(ModelImages).all()
    response = {}
    for item in bd_data:
        response[item.id] = input_rabbitMQ(f"{item.name} {item.path} "
                                           f"{item.data} {item.permission} "
                                           f"{item.size}")

    return JSONResponse(response)
    # except:
    #    return JSONResponse(status_code=400, content={"message": "Incorrect Data"})

@app.get("/image/{id}")
async def show_image(id: int, user: User = Depends(get_current_user)):
    try:
        response = {}
        sh = SchemaId(id=id)
        bd_data = db.session.query(ModelImages).filter(ModelImages.id ==
                                                       sh.id).first()
        response[bd_data.id] = input_rabbitMQ(f"{bd_data.name} {bd_data.path} "
                                              f"{bd_data.data} {bd_data.permission} "
                                              f"{bd_data.size}")
        return JSONResponse(response)
    except AttributeError:
        return JSONResponse(status_code=400, content={"message": "Incorrect "
                                                                 "Data. This id is not in the database"})
    except:
        return JSONResponse(status_code=400, content={"message": "Incorrect Data. Error id"})



@app.delete("/image/{id}")
async def delete_image(id: int, user: User = Depends(get_current_user)):
    try:
        sh = SchemaId(id=id)
        db.session.query(ModelImages).filter(ModelImages.id ==
                                             sh.id).delete(synchronize_session=False)
        db.session.commit()

        response = del_rabbitMQ(f"{sh.id}")
        return {"message": "Photo delete successfully",
                "data": response}
    except:
        return JSONResponse(status_code=400, content={"message":
                                                          "Incorrect Data. Error id"})


@app.put("/image/{id}")
async def update_image(id: int, text: str,
                       user: User = Depends(get_current_user)):
    try:
        sh = SchemaUpdate(id=id, name=text)
        bd_data = db.session.query(ModelImages).filter(ModelImages.id ==
                                                       sh.id).first()
        bd_data.name = sh.name
        db.session.add(bd_data)
        db.session.commit()

        response = put_rabbitMQ(f"{sh.id} {sh.name}")
        return {"message": "Photo update successfully",
                "data": response}
    except:
        return JSONResponse(status_code=400, content={"message":
                                                          "Incorrect Data. Error id"})

