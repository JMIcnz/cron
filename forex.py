
from fastapi import FastAPI

app = FastAPI()

# serving on 127.0.0.1:8000

# set routing
@app.get("/getMessage")
async def hello(name: str):
  print("Congrats" + name + '! API endpoint has been created.')
  return {"Message": "Congrats" + name + "! API endpoint has been created."}
  # it return a python dictionary
  # in fastapi, it will be automatically converted to json response
  # so the browser, curl will get a json response


