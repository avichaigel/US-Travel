import mysql.connector
from os.path import isfile
from mimetypes import guess_type
from fastapi import FastAPI, Response

# Enter to SQL server
MY_DB = mysql.connector.connect(
    host="localhost",
    user="root",
    password="Au206492746"
)

# To connect
app = FastAPI()
mycursor = MY_DB.cursor()

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