from pydantic import BaseModel

class CarbonDioxideConversionResponse(BaseModel):
    unit: str
    result: float
