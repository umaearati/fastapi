from fastapi import FastAPI
from pydantic import BaseModel



class Book(BaseModel):
    id: int
    title: str
    author:str
    price:float
    description:str
    
    
    
    