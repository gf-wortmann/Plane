# Calculation of duration of long time operating geometry

from input_parameters_2 import standard_atmosphere as isa, constants as const
import numpy as np

LD_ratio_starting = 50.0
engine_fuel_consumption = 0.06  # kg for hp in hour
fuel_to_toff_mass_ratio = 0.7
wing_loading_starting = 80  # kgf per sqm
'''
let Cya = 1, still...
'''
cya_starting = 1.2
density_range = isa['density_SI']
g = const['g']

va_starting = np.sqrt(2 * wing_loading_starting * g / (cya_starting * density_range[12000.0]))
print(va_starting)
_n_starting = va_starting * g / LD_ratio_starting
print(_n_starting)
_fuel_per_hour = _n_starting * engine_fuel_consumption / 736
print(_fuel_per_hour)

flight_duration = 800.0  # hours

h = 0
fuel_wasted_ratio = 0
wing_loading = wing_loading_starting
# cya = cya_starting
while fuel_wasted_ratio <= fuel_to_toff_mass_ratio and h < flight_duration:
    va = np.sqrt(2 * wing_loading * g / (cya_starting * density_range[20000.0]))
    _n = va * g / LD_ratio_starting
    _fuel_per_hour = _n * engine_fuel_consumption / 1000
    fuel_wasted_ratio += _fuel_per_hour
    wing_loading = wing_loading_starting * (1-fuel_wasted_ratio)
    h += 1.0
    print(f'fuel per hour: {_fuel_per_hour:.5f}, fuel wasted: {fuel_wasted_ratio:.5f}, wing loading is:'
          f' {wing_loading:.2f}, time of flight: {h}')
    
