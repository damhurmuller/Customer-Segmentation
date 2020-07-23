import os
import pandas as pd
from fastapi import FastAPI
from typing import Optional
from pydantic import BaseModel
from typing import List
from fastapi.responses import Response

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_DIR = os.path.join(BASE_DIR, 'data')

dataset = os.path.join(DATA_DIR, 'rfm.csv')

app = FastAPI()

def get_segment(params):
    
    rfm = pd.read_csv(dataset)
    
    if len(params) == 1:
        segment = list(rfm[rfm['customer_id'] == params[0]]["segment"].values)
        return {'customer_id': params[0], 'segment': segment[0]}
    else:
        ids = list(rfm[rfm['customer_id'].isin(params)]['customer_id'].values)
        segment = list(rfm[rfm['customer_id'].isin(params)]["segment"].values)
        return {'customer_id': ids, 'segment': segment}

class Customer(BaseModel):
    customer_id: List[float]


@app.get("/")
def read_root():
    return {"Hello": "World"}

@app.post("/ids")
def create_id(customer: Customer): 
    response = get_segment(customer.customer_id)

    return response
