import datetime
from pydantic import BaseModel
import numpy as np
import TTFmodel.parameters as pm
import TTFmodel.utils as util

class FireRisk(BaseModel):
    ttf: float
    timestamp: datetime.datetime



def compute_firerisk(temp_out: list[float], humidity_out: list[float]):
    """Computes the firerisks for the provided temperatures and humidities.
    
    Parameters
    ----------
    temp_out : list[float], required
        a list of temperatures outside in Celsius.
    
    humidity_out: list[float], required
        a list of humidities outside.
    
    Returns
    -------
    something something

    """
    

    temp_inside = [pm.T_c_in] * len(temp_out)


    #The saturation vapor pressure outside for the provided temperatures
    saturation_vapor_pressure_out = list(map(util.calc_pwsat,temp_out))
    
    #The consentration of water based on the saturation vapor pressure and the provided temperatures
    saturation_vapor_consentration_out = list(map(util.calc_cwsat, saturation_vapor_pressure_out, temp_out))

    # The actual water consentration outside
    water_consentration_out = list(map(util.calc_cw, humidity_out, saturation_vapor_consentration_out))

    #The saturation vapor pressure inside for the provided temperatures
    saturation_vapor_pressure_inside = list(map(util.calc_pwsat, temp_inside))

    # The consentration of water based on the saturation vapor pressure inside and the provided temperatures
    saturation_vapor_consentration_inside = list(map(util.calc_cwsat, saturation_vapor_pressure_inside, temp_inside))


    #Ventilation variables
    ach = list(map(util.calc_ach, temp_out, temp_inside))
    beta = list(map(util.calc_beta, ach))


    supply_per_timestep = (pm.supply_24h / (24 * 3600)) * pm.delta_t
    supply = [supply_per_timestep] * len(temp_out)

    wall = n



