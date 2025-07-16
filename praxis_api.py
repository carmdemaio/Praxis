from fastapi import FastAPI, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import numpy as np
import pandas as pd

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://127.0.0.1:5500", "http://localhost:5500"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)

class RiskInput(BaseModel):
    initial_investment: float
    expected_return: float
    volatility: float
    time_horizon: int

@app.post("/calculate_risk/")
def calculate_risk(data: RiskInput):
    num_simulations = 10000
    results = []

    for _ in range(num_simulations):
        final_value = data.initial_investment
        for _ in range(data.time_horizon):
            annual_return = np.random.normal(data.expected_return, data.volatility)
            final_value *= (1 + annual_return)
        results.append(final_value)

    mean_value = float(np.mean(results))
    median_value = float(np.median(results))
    std_deviation = float(np.std(results))
    percentile_5 = float(np.percentile(results, 5))
    percentile_95 = float(np.percentile(results, 95))

    return {
        "risk_metrics": {
            "Mean Final Value": mean_value,
            "Median Final Value": median_value,
            "Standard Deviation": std_deviation,
            "5th Percentile (Worst Case)": percentile_5,
            "95th Percentile (Best Case)": percentile_95,
        }
    }

@app.post("/upload_csv/")
async def upload_csv(file: UploadFile = File(...)):
    df = pd.read_csv(file.file)
    if "return" not in df.columns:
        return {"error": "CSV must contain a 'return' column."}
    daily_returns = df["return"].pct_change().dropna()
    calculated_volatility = float(np.std(daily_returns))
    return {"calculated_volatility": calculated_volatility}
