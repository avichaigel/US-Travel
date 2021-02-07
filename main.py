# import mysql.connector
from os.path import isfile
from mimetypes import guess_type
from pydantic import BaseModel
import uvicorn
from fastapi import FastAPI, Response


# todo change item to GET JSON
class Item(BaseModel):
    hotel: str
    city: str
    state: str
    airport: str


class Person(BaseModel):
    name: str
    password: int


# Enter to SQL server
# MY_DB = mysql.connector.connect(
#     host="localhost",
#     user="root",
#     password="Au206492746"
# )


# To connect
app = FastAPI()
# mycursor = MY_DB.cursor()


@app.get("/api/hello")
async def get():
    return {"Hello": "world"}


# parm: person
# ret: all the person table
# The user click on sign_up
@app.post('/api/sign_up')
def sigh_up(person: Person):
    # sql = "INSERT INTO `mydatabase`.`person` (`name`, `password`) VALUES ('" + person.name + "', '" + int(person.password) + "');"
    # mycursor.execute(sql)
    # MY_DB.commit()
    #
    # # return the line about the person
    # sql = "SELECT * FROM mydatabase.person WHERE name = '" + person.name + "';"
    # mycursor.execute(sql)
    # myresult = mycursor.fetchall()
    # return myresult


# parm: person
# ret: all the person table
# The user click on sign_in
@app.post('/api/sign_in')
# TODO: rung pass
def sigh_in(person: Person):
    # # return the line about the person
    # sql = "SELECT * FROM mydatabase.person WHERE name = '" + person.name + "';"
    # mycursor.execute(sql)
    # myresult = mycursor.fetchall()
    # return myresult


@app.delete('/api/delete')
def delete():
    return {}


# If you get any file
@app.get("/{filename}")
async def get_site(filename):
    filename = './site/' + filename

    if not isfile(filename):
        return Response(status_code=404)

    with open(filename) as f:
        content = f.read()

    content_type, _ = guess_type(filename)
    return Response(content, media_type=content_type)

# get index.html
@app.get("/")
async def get_site_default_filename():
    return await get_site('index.html')


if __name__ == '__main__':
    uvicorn.run(app, host="localhost", port=5555)

















