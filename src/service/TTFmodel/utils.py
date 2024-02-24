# Copied from https://github.com/h584969/dynamic-frcm/blob/main/src/frcm/fireriskmodel/utils.py

import math
import numpy as np
import TTFmodel.parameters as mp

"""Functions for computing saturation vapor pressure, and water concentrations"""
""" pw_sat -- cw_sat -- cw_in -- initial fmc """


# saturation vapor pressure at temperature Temp_c (celsius)
def calc_pwsat(temp_c: float) -> float:
    """calculates the saturation vapor pressure for the specified temperature.

    Read more about saturation vapor pressure here: https://en.wikipedia.org/wiki/Vapour_pressure_of_water

    Parameters
    ----------
    temp_c: float, required
        The temperature to calculate for, expected to be in celsius.
    
    Returns
    -------
    float
        The saturation vapor pressure in Pascal.
    """

    pwsat = 610.78 * math.exp((17.2694 * temp_c) / (temp_c + 238.3))
    return pwsat


# saturation water concentration based on saturated vapor pressure (pwsat)
def calc_cwsat(pwsat: float ,temp_c: float) -> float:
    """Calculates the water constrentation based on the saturation vapor pressure.

    Note: This method expects the saturation vapor pressure to be based on the same temperature as provided in temp_c.
    Using different temperatures when calculation consentration and pressure might yield wrong results.

    Parameters
    ----------
    pwsat: float, required
        The saturation vapor pressure to compute the consentration for.
    
    temp_c: float, required
        The temperature to calculate the constrentation for. Expected to be in celsius.

    Returns
    -------
    float
        The water constrentation in kg/m^3
    """
    cwsat = (pwsat * mp.mol_weight)/(mp.gas_constant * (temp_c + 273.15))
    return cwsat


# actual water concentration in air
def calc_cw(rh: float, cwsat: float) -> float:
    """Calculates the actual water consentration based on the saturation vapor pressure and the provided humidity
    
    The formula used to calculate the actual humidity is the relative humidity as defined by
    100% * (c / cs) where p is the measured consentration and ps is the consentration at saturation vapor pressure.
    

    Parameters
    ----------
    rh: float, required
        The humidity, expected to be in kg/m^3 (mass per volume)
    
    cwsat: float, required
        The water consentration based on saturation vapor pressure. Expected to be kg/m^3 (mass per volume)
    
    Returns
    -------
    float
        The actual water consentration in kg/m^3
    
    """
    cw = rh / 100 * cwsat
    return cw


# computes initial fmc of wooden panels
# computes fmc from indoor rh (equilibrium state) rh must be given as a fraction, e.g., 0.35
def calc_fmc(rh) -> float:
    c_fmc = 0.0017 + 0.2524 * rh - 0.1986 * math.pow(rh,2) + 0.0279 * math.pow(rh,3) + 0.167 * math.pow(rh,4)
    return c_fmc


""" Functions related to ventilation """
""" Air change per Hour -- Beta"""


# air change per hour (ach)
def calc_ach(temp_c_out: float, temp_c_in: float) -> float:
    """Calculates how many times the total volume of air in a space is changed every hour

    For more information visit: https://en.wikipedia.org/wiki/Air_changes_per_hour
    
    Parameters
    ----------
    temp_c_out: float, required
        the outside temperature, expected to be in celsius
    temp_c_in: float, required
        the inside temperature, expected to be in celsius
    
    Returns
    -------
    float
        The air change per hour.
    """ 
    c_ach = mp.gamma * math.sqrt((abs(1 / (temp_c_out + 273.15) - 1 / (temp_c_in + 273.15)) / (temp_c_out + 273.15)))
    return c_ach


# beta ventilation factor
def calc_beta(c_ach: float) -> float:
    """Calculates the beta ventilation factor given the air change per hour
    
    Parameters
    ----------
    c_ach: float, required
        The air change per hour for celsius.

    Returns
    -------
    float
        The beta ventilation factor
    """

    c_beta = 1 - math.exp((-c_ach * mp.delta_t)/3600)
    return c_beta


""" Updating variables post the modelling of wooden panel humidity transport (wall modelling) """


# extrapolating wooden panel fmc to a surface value
def calc_surf(c1_t, c2_t) -> float:
    c_surf = c1_t - 0.5 * (c2_t - c1_t)
    return c_surf


# water concentration difference between bulk air and wall boundary layer - inputs from previous timestep
def calc_deltac(rhin, rhwall, cwsatin) -> float:
    deltac = (rhwall - rhin) * cwsatin
    return deltac


# relative humidity at wooden panel surfaces - inputs surface fmc at equal timestep
def calc_rhwall(cfmc) -> float:
    rhwall = 0.0698 - 1.258 * (cfmc / mp.rho_wood) + 125.35 * math.pow((cfmc / mp.rho_wood),2) - 809.43 * math.pow((cfmc / mp.rho_wood),3) + 1583.8 * math.pow((cfmc / mp.rho_wood),4)
    return rhwall


# indoor water concentration - input from previous timestep
def calc_cwin(cac, cwall, csupply, cwin, beta):
    cwin = (1 - beta) * cwin + cac + cwall + csupply
    return cwin


""" Calculation of wooden panel humidity transport """


# computing the fmc in layer 1 (c1_t+1) (facing interior of enclosure) by use of fmc values in layer 1 and layer 2
# inputs from previous timestep
def calc_layer1(rhin,rhwall,c1_t,c2_t, csatin) -> float:
    layer1 = c1_t + (mp.delta_t/mp.delta_x) * ((mp.D_W_a / mp.boundary_layer) * (rhin - rhwall) * csatin + (mp.D_w_s / mp.delta_x) * (c2_t - c1_t))
    return layer1


# computing the fmc in layers 2 to N-1 (second last layer) at time t+1 by second order central difference - inputs from
# previous timestep
def calc_middle_layers(cn_t, c_prev_n_t, c_post_n_t) -> float:
    middle_layer = cn_t + mp.fourier * (c_prev_n_t - 2*cn_t + c_post_n_t)
    return middle_layer


# computing the fmc in the last layer (backside of wooden panels) based on fmc from layer N-1 and Layer N both from
# previous timestep
def calc_outer_layer(cn_t, c_pre_n_t) -> float:
    outer_layer = cn_t + mp.fourier * (c_pre_n_t - cn_t)
    return outer_layer


""" The main contributions to change in indoor water concentration """
""" Supply -- Air Change by Ventilation -- Humidity Exchange From Wooden Surfaces"""


def calc_csupply(sup) -> float:
    csupply = sup / mp.Vol
    return csupply


def calc_cac(beta, cw_out, temp_c_out, temp_c_in) -> float:
    cac = beta * cw_out * ((temp_c_out + 273.15) / (temp_c_in + 273.15))
    return cac


def calc_cwall(deltac) -> float:
    cwall = (mp.A_ex * mp.D_W_a * deltac * mp.delta_t / mp.boundary_layer) / mp.Vol
    return cwall