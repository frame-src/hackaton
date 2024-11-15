from model.model import CarbonDioxideConversionResponse
from fastapi import APIRouter


router = APIRouter()

# average CO₂ emissions per kilometer = 149 gCO2/km
@router.get('/CarbonDioxideBalance')
async def carbonDioxideBalance( km: int) :
    conv = (km * 149)/1000
    response = CarbonDioxideConversionResponse(unit="KgCO2/km", result=conv)
    return response
