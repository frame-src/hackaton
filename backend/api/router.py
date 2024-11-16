from model.model import CarbonDioxideConversionResponse
from fastapi import APIRouter
from core.co2_calc import calc_co2


router = APIRouter()

# average CO₂ emissions per kilometer = 149 gCO2/km
@router.get('/CarbonDioxideBalance')
async def carbonDioxideBalance( km: int) :

	resp_val = calc_co2(row)
    response = CarbonDioxideConversionResponse(unit="KgCO2/km", result=resp_val)
    return response
