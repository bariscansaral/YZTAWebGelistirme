from fastapi import FastAPI, Body, Path, Query, HTTPException
from typing import Optional
from pydantic import BaseModel, Field
from starlette import status

app = FastAPI()