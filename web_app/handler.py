import pandas as pd
from fastapi import FastAPI
from pydantic import BaseModel
from typing import List

# dataset path
dataset = "rfm.csv" 

app = FastAPI()

def get_segment(params):
    """Read the dataset and return the id and segment of the input id

    Parameters:
    list: ids

    Returns:
    json: Return the customer id and the segment
    """

    # read the dataset
    rfm = pd.read_csv(dataset)
    
    # check if is only one id
    if len(params) == 1:
        segment = list(rfm[rfm['customer_id'] == params[0]]["segment"].values)
        return {'customer_id': params[0], 'segment': segment[0]}
    # more than one id
    else:
        ids = list(rfm[rfm['customer_id'].isin(params)]['customer_id'].values)
        segment = list(rfm[rfm['customer_id'].isin(params)]["segment"].values)
        return {'customer_id': ids, 'segment': segment}

class Customer(BaseModel):
    customer_id: List[float]


@app.get("/")
def read_root():
    """View root.

    Returns:
    json: {"Hello": "World"}
    
    """
    return {"Hello": "World"}

@app.post("/segments")
def create_id(customer: Customer):
    """ Return the customer id and his segment cluster

    Parameters:
    json: list of one or more ids
    
    Example
        {"customer_id": [1,2,3]}

    Returns:
    json: Return the customer id and the segment

    """
    response = get_segment(customer.customer_id)

    return response
