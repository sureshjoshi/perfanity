# CACHE_BUSTING=
# ruff: noqa: E402

import time

print(f"SCRIPT_START: {time.time()}")

import os

import fastapi
import numpy
import pandas
import pydantic
import scipy
import sqlalchemy

MY_ID = "sj"
MY_ENV_ID = os.getenv("PERFANITY_ID", "env")


class Foo(pydantic.BaseModel):
    id: str


app = fastapi.FastAPI()


@app.get("/")
async def root():
    foo = Foo(id=MY_ID)
    bar = Foo(id=MY_ENV_ID)
    return {"message": f"Hello {foo} and {bar}"}


def square(x: int) -> int:
    return x**2


a = numpy.mean([1, 2, 3])
b = pandas.DataFrame()
c = scipy.integrate.quad(square, 0, 4)
d = sqlalchemy.true()

# if __name__ == "__main__":
#     uvicorn.run(app)

print(f"SCRIPT_END: {time.time()}")
