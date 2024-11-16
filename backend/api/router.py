from model.model import CarbonDioxideConversionResponse
from fastapi import APIRouter
from core.data_management import loadData

router = APIRouter()

# average CO₂ emissions per kilometer = 149 gCO2/km
@router.get('/CarbonDioxideBalance')
async def carbonDioxideBalance( km: int) :
    conv = (km * 149)/1000
    response = CarbonDioxideConversionResponse(unit="KgCO2/km", result=conv)
    return response


@router.get('/DataLoad')
async def dataLoadPandas():
    return await loadData()


@router.get('/Test')
async def test():
    return {'car' :150 , 'other': 50}