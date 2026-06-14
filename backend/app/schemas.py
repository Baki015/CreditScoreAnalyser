from pydantic import BaseModel


class CompanyInput(BaseModel):
    company_name: str
    working_capital: float
    total_assets: float
    retained_earnings: float
    ebit: float
    market_value_equity: float
    total_liabilities: float
    sales: float
