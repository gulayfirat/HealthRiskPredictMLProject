# app.py - FastAPI application for health risk prediction
from fastapi import FastAPI, Request           # FastAPI core and request object
from fastapi.templating import Jinja2Templates # For rendering HTML templates
from fastapi.responses import HTMLResponse     # For returning HTML responses
import pickle                                  # For loading ML model and preprocessors
import pandas as pd                            # For data manipulation
from pydantic import BaseModel                 # For request data validation
import db_operations as dbo                    # Custom module for DB operations

# Initialize FastAPI app and Jinja2 templates
app = FastAPI()
templates = Jinja2Templates(directory="templates")

# Home page endpoint, renders index.html
@app.get("/", response_class=HTMLResponse)
async def home(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

# Event handler: runs on app startup, sets up DB connection and tables
@app.on_event("startup")
def startup_db_connection():
    global conn, cursor
    try:
        conn, cursor = dbo.create_database()
        dbo.create_tables(conn, cursor)
    except Exception as e:
        print(f"ERROR(startup_db_connection): {e}")
        conn, cursor = None, None

# Event handler: runs on app shutdown, closes DB connection
@app.on_event("shutdown")
def shutdown_db_connection():
    global conn, cursor
    try:
        if 'conn' in locals() and conn:
            conn.close()
            print("\nClosed Connection")
    except Exception as e:
        print(f"ERROR(shutdown_db_connection): {e}")

# Load trained ML model and preprocessing objects from pickle file
with open("health_risk_complete.pkl", "rb") as f:
    saved_data = pickle.load(f)
    model = saved_data['model']           # Trained ML model (the model you can see on health_risk_prediction.ipynb file )
    encoders = saved_data['encoders']     # Encoders for categorical features
    scaler = saved_data['scaler']         # Scaler for feature normalization
    features = saved_data['all_features'] # List of all feature names

# Pydantic model for validating incoming feature data
class FeaturesModel(BaseModel):
    age: int
    weight: int
    height: int
    exercise: str
    sleep: float
    sugar_intake: str
    smoking: str
    alcohol: str
    married: str
    profession: str
    bmi: float

# Prediction endpoint: receives user data, processes, predicts, and stores in DB
@app.post("/predict")
async def predict(data: FeaturesModel):
    # Convert incoming request data to a pandas DataFrame
    input_data = pd.DataFrame([data.model_dump()])
    # Insert the raw input data into the 'Features' table in the database
    dbo.insert_df_to_db(conn, input_data, "Features")
    # Encode categorical columns using the loaded encoders (except 'target' and 'profession')
    for col, mapping in encoders.items():
        if col not in ['target', 'profession']:
            input_data[col] = input_data[col].map(mapping)
    # One-hot encode the 'profession' column
    input_data = pd.get_dummies(input_data, columns=['profession'], drop_first=True)
    # Reindex DataFrame columns to match the model's expected feature order, filling missing columns with 0
    input_data = input_data.reindex(columns=features, fill_value=0)
    # Scale the input features using the loaded scaler
    input_data_scaled = scaler.transform(input_data)
    # Make a prediction using the trained model
    prediction = model.predict(input_data_scaled)[0]
    # Prepare prediction result as a DataFrame and insert into 'Predicts' table in the database
    prediction_df = pd.DataFrame([{'predict': str(prediction)}])
    dbo.insert_df_to_db(conn, prediction_df, "Predicts")
    # Print prediction to the console (for debugging/logging)
    print(f"prediction: {prediction}")
    # Return the prediction as a JSON response
    return {"prediction": prediction}
