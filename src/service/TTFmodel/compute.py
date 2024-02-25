import datetime
from pydantic import BaseModel
import numpy as np
import src.service.TTFmodel.parameters as pm
import src.service.TTFmodel.utils as util

class FireRisk(BaseModel):
    ttf: float
    timestamp: datetime.datetime



def compute_firerisk(temp_outside: list[float], relative_humidity_outside: list[float]):
    """Computes the firerisks for the provided temperatures and humidities.
    
    Parameters
    ----------
    temp_outside : list[float], required
        a list of temperatures outside per timestep. Expected to be in celsius.
    
    humidity_out: list[float], required
        a list of humidities outside per timestep.
    
    Returns
    -------
    list[float]
        The relative humidity inside per timestep
    
    list[float]
        The ttf per timestep
    """
    
    temp_inside = [pm.T_c_in] * len(temp_outside)  # Potential future changes may involve dynamic in-home temperatures

    """ compute saturation vapor pressures and water concentrations, outdoor and indoor """
    # w = water, sat = saturation
    pressure_water_saturation_outside = list(map(util.calc_pwsat, temp_outside))
    consentration_water_saturation_outside = list(map(util.calc_cwsat, pressure_water_saturation_outside, temp_outside))
    consentration_water_outside = list(map(util.calc_cw, relative_humidity_outside, consentration_water_saturation_outside))
    pressure_water_saturation_inside = list(map(util.calc_pwsat, temp_inside))
    consentration_water_saturation_inside = list(map(util.calc_cwsat, pressure_water_saturation_inside, temp_inside))

    # ventilation variables
    air_change_hour = list(map(util.calc_ach, temp_outside, temp_inside))
    ventilation_beta = list(map(util.calc_beta, air_change_hour))

    # calculate supply per timestep and make a supply vector (for future updates - currently containing constant values)
    supply_pts = (pm.supply_24h / (24 * 3600)) * pm.delta_t
    supply = [supply_pts] * len(temp_outside)

    """ create wall array and vector """

    # wall array - storing fmc values - rows represent a step in time, columns represent wooden panel layers.
    wall = np.zeros(shape=(len(temp_outside), pm.sub_layers))
    # used to update the wall array
    wall_vector = np.zeros(pm.sub_layers)

    # initial fmc value in wooden panels
    initial_fmc = util.calc_fmc(pm.RH_in) * pm.rho_wood

    """ placeholders """
    # shall contain wooden surface fmc values
    surface = np.zeros(len(temp_outside))
    # shall contain wooden surface (boundary layer) rh values
    relative_humidity_wall = np.zeros(len(temp_outside))
    # shall contain bulk air (in-home) rh values
    relative_humidity_inside = np.zeros(len(temp_outside))
    # shall contain bulk air (in-home) water concentrations
    consentration_water_inside = np.zeros(len(temp_outside))
    # shall contain water concentration difference between rh_wall and rh_in
    delta_c = np.zeros(len(temp_outside))
    # shall contain water concentration (contribution) per timestep from wooden surfaces
    c_wall = np.zeros(len(temp_outside))


    # set initial conditions
    wall[0] = [initial_fmc] * pm.sub_layers
    surface[0] = util.calc_surf(wall[0][0], wall[0][1])
    relative_humidity_wall[0] = util.calc_rhwall(surface[0])
    relative_humidity_inside[0] = pm.RH_in
    consentration_water_inside[0] = pm.RH_in * consentration_water_saturation_inside[0]
    delta_c[0] = util.calc_deltac(relative_humidity_inside[0], relative_humidity_wall[0], consentration_water_saturation_inside[0])
    c_wall[0] = util.calc_cwall(delta_c[0])

    c_ac = list(map(util.calc_cac, ventilation_beta, consentration_water_outside, temp_outside, temp_inside))
    c_supply = (list(map(util.calc_csupply, supply)))

    for i in range(len(temp_outside) - 1):
        # compute fmc in layer 1
        wall_vector[0] = util.calc_layer1(relative_humidity_inside[i], relative_humidity_wall[i], wall[i][0], wall[i][1], consentration_water_saturation_inside[i])
        n = 0
        for l in range(pm.sub_layers-2):
            # compute fmc in wall layers 2 to N-1
            n = n + 1
            wall_vector[n] = util.calc_middle_layers(wall[i][n], wall[i][n - 1], wall[i][n + 1])
        # compute fmc in wall layer N (panel backside)
        wall_vector[-1] = util.calc_outer_layer(wall[i][-1], wall[i][-2])
        # update wall array
        wall[i + 1][:] = wall_vector
        # update surface vector
        surface[i + 1] = util.calc_surf(wall[i + 1][0], wall[i + 1][1])
        # update rh_wall
        relative_humidity_wall[i + 1] = util.calc_rhwall(surface[i + 1])
        # update water concentration difference between bulk air and boundary layer
        delta_c[i + 1] = util.calc_deltac(relative_humidity_inside[i], relative_humidity_wall[i], consentration_water_saturation_inside[i])
        # update indoor water concentration
        consentration_water_inside[i + 1] = util.calc_cwin(c_ac[i], c_wall[i], c_supply[i], consentration_water_inside[i], ventilation_beta[i])
        # update indoor relative humidity
        relative_humidity_inside[i + 1] = consentration_water_inside[i + 1] / consentration_water_saturation_inside[i + 1]
        # update c_wall
        c_wall[i + 1] = util.calc_cwall(delta_c[i + 1])

    # Compute ttf
    factor = 100 / pm.rho_wood
    fmc = list(map(lambda x: x*factor, surface))
    ttf = list(map(lambda y: 2 * np.exp(0.16*y),fmc))

    return relative_humidity_inside, ttf