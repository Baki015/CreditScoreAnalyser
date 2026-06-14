from io import BytesIO

import pandas as pd
from fastapi import FastAPI, File, HTTPException, UploadFile
from fastapi.middleware.cors import CORSMiddleware

from .ml_model import model_metrics, predict_risk
from .schemas import CompanyInput
from .scoring import analyze_company

app = FastAPI(title="Digitalni kreditni službenik")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

REQUIRED_COLUMNS = [
    "company_name",
    "working_capital",
    "total_assets",
    "retained_earnings",
    "ebit",
    "market_value_equity",
    "total_liabilities",
    "sales",
]


@app.get("/")
def home():
    return {"status": "ok", "message": "Digitalni kreditni službenik API radi."}


@app.get("/api/health")
def health():
    return {"status": "active"}


@app.get("/api/model")
def model_info():
    return model_metrics()


@app.post("/api/analyze")
def analyze(company: CompanyInput):
    data = company.model_dump()
    return analyze_company(data, predict_risk)


@app.post("/api/upload")
async def upload(file: UploadFile = File(...)):
    content = await file.read()
    name = file.filename.lower()

    try:
        if name.endswith(".csv"):
            df = pd.read_csv(BytesIO(content))
        elif name.endswith(".xlsx"):
            df = pd.read_excel(BytesIO(content))
        else:
            raise HTTPException(status_code=400, detail="Dozvoljeni su CSV i XLSX fajlovi.")
    except Exception as exc:
        raise HTTPException(status_code=400, detail="Fajl nije moguće učitati.") from exc

    missing = [column for column in REQUIRED_COLUMNS if column not in df.columns]
    if missing:
        raise HTTPException(status_code=400, detail=f"Nedostaju kolone: {', '.join(missing)}")

    results = []
    for _, row in df[REQUIRED_COLUMNS].iterrows():
        data = row.to_dict()
        for column in REQUIRED_COLUMNS[1:]:
            data[column] = float(data[column])
        results.append(analyze_company(data, predict_risk))

    summary = {
        "total": len(results),
        "safe": sum(1 for item in results if item["zone"] == "Safe"),
        "grey": sum(1 for item in results if item["zone"] == "Grey Zone"),
        "distress": sum(1 for item in results if item["zone"] == "Distress"),
        "average_risk": round(sum(item["risk_percent"] for item in results) / len(results), 2) if results else 0,
    }

    return {"summary": summary, "results": results}
