from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import numpy as np
import pandas as pd

# Initialize FastAPI app
app = FastAPI()

# Enable CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allow all origins (for testing)
    allow_credentials=True,
    allow_methods=["GET", "POST", "OPTIONS"],  # Explicitly allow OPTIONS
    allow_headers=["*"],  # Allow all headers
)

class RiskEngine:
    def __init__(self, simulations=10000):
        self.simulations = simulations

    def monte_carlo_simulation(self, initial_investment, expected_return, volatility, time_horizon):
        np.random.seed(42) 
        results = []

        for _ in range(self.simulations):
            price = initial_investment
            for _ in range(time_horizon):
                annual_return = np.random.normal(expected_return, volatility)
                price *= (1 + annual_return)
            results.append(price)

        return pd.DataFrame(results, columns=["Final Value"])

    def risk_analysis(self, df):
        return {
            "Mean Final Value": df["Final Value"].mean(),
            "Median Final Value": df["Final Value"].median(),
            "5th Percentile (Worst Case)": np.percentile(df["Final Value"], 5),
            "95th Percentile (Best Case)": np.percentile(df["Final Value"], 95),
            "Standard Deviation": df["Final Value"].std()
        }

risk_engine = RiskEngine()

class RiskInput(BaseModel):
    initial_investment: float
    expected_return: float
    volatility: float
    time_horizon: int

@app.options("/calculate_risk/")
async def preflight():
    return {"message": "CORS preflight successful"}

@app.post("/calculate_risk/")
def calculate_risk(data: RiskInput):
    simulation_results = risk_engine.monte_carlo_simulation(
        initial_investment=data.initial_investment,
        expected_return=data.expected_return,
        volatility=data.volatility,
        time_horizon=data.time_horizon
    )
    
    risk_metrics = risk_engine.risk_analysis(simulation_results)
    
    return {
        "simulation_results": simulation_results.head(10).to_dict(orient="records"),
        "risk_metrics": risk_metrics
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)

