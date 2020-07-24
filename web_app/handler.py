import pandas as pd
from fastapi import FastAPI, Response
from typing import List, Optional
from fastapi.params import Query

# dataset path
dataset_path = "rfm.csv" 

app = FastAPI()

def load_dataset(path):
    df = pd.read_csv(path)
    
    return df

# @app.get("/")
# def read_root():
#     return {"Hello": "World"}


@app.get("/customers/")
def get_users(customer_id: Optional[List[int]] = Query(None)):
    
    rfm = load_dataset(dataset_path) 
    
    # ids = list(rfm[rfm['customer_id'].isin(customer_id)]['customer_id'].values)
    segments = list(rfm[rfm['customer_id'].isin(customer_id)]["segment"].values)

    response = {"customer_id": customer_id, "segment": segments}
    # response = {"ids": ids}
    
    return response

@app.get("/customers/{customer_id}")
def get_user(customer_id : int):
    rfm = load_dataset(dataset_path)

    if customer_id in rfm['customer_id'].values:
        segment = rfm[rfm['customer_id'] == customer_id]['segment'].values[0]
        response = {"customer_id": customer_id, "segment": segment}
        return response
    else:
        return Response('ID Not Avaiable', status_code=200) 
