from fastapi import FastAPI, Request, Response
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse
import  pickle
import pandas as pd
from pydantic import BaseModel
import db_operations as dbo


app = FastAPI()
templates = Jinja2Templates(directory="templates")

@app.get("/", response_class=HTMLResponse)
async def home(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

@app.on_event("startup")
def startup_db_connection():
    global conn, cursor
    conn, cursor = dbo.create_database()
    dbo.create_tables(conn, cursor)

@app.on_event("shutdown")
def shutdown_db_connection():
    global conn, cursor
    if 'conn' in locals() and conn:
        conn.close()
        print("\nClosed Connection")

with open("health_risk_complete.pkl", "rb") as f:
    saved_data = pickle.load(f)
    model = saved_data['model']
    encoders = saved_data['encoders']
    scaler = saved_data['scaler']
    features = saved_data['all_features']


class FeaturesModel(BaseModel):
    age:int
    weight:int
    height:int
    exercise:str
    sleep:float
    sugar_intake:str
    smoking:str
    alcohol:str
    married:str
    profession:str
    bmi:float



@app.get("/test")
async def test():
    return Response("Hello, World!")
@app.post("/predict")
async def predict(data: FeaturesModel):
    input_data=pd.DataFrame([data.model_dump()])
    dbo.insert_df_to_db(conn, input_data, "Features")
    for col, mapping in encoders.items():
        if col not in ['target', 'profession']: #['exercise','sugar_intake', 'smoking','alcohol', 'married']
            input_data[col] = input_data[col].map(mapping)
    input_data = pd.get_dummies(input_data, columns=['profession'], drop_first=True)
    input_data = input_data.reindex(columns=features, fill_value=0)
    input_data_scaled = scaler.transform(input_data)
    prediction = model.predict(input_data_scaled)[0]
    prediction_df = pd.DataFrame([{'predict': str(prediction)}])
    dbo.insert_df_to_db(conn, prediction_df, "Predicts")
    print(f"prediction: {prediction}")
    return {"prediction": prediction}


