import numpy as np
import math
from typing import Final


# import

class ISA:
    temperature_gradient_upto_11km: Final[float] = -0.0065
    temperature_gradient_upto_20km: Final[float] = 0.0
    temperature_gradient_upto_32km: Final[float] = 0.0009867
    temperature_standard_SL: Final[float] = 288.150
    temperature_in_stratosphere: Final[float] = 216.650
    
    pressure_standard_SL: Final[float] = 1.01325e5
    pressure_standard_11km = 22690.2829933025
    pressure_standard_20km = 5526.28870668925
    pressure_stratosphere_coefficient: Final[float] = 0.434294
    
    density_standard_SL = 1.2250
    
    gas_constant: Final[float] = 8314.4598
    molar_masse: Final[float] = 28.96442
    relative_gas_constant = gas_constant / molar_masse
    g_upto_11km: Final[float] = 9.790
    g_over_11_upto_20km: Final[float] = 9.750
    g_over_20km: Final[float] = 9.726
    
    beta_s: Final[float] = 1.458e-6
    S: Final[float] = 110.4
    
    altitude_SL: Final[float] = 0
    altitude_troposphere_upr_margin: Final[float] = 11000
    altitude_stratosphere_upr_margin: Final[float] = 20000
    altitude_upr_margin: Final[float] = 32000
    
    def __init__(self):
        self.__altitude = None
        self.__temperature = None
        self.__pressure = None
        self.__density = None
        self.__dynamic_viscosity = None
        self.__cinematic_viscosity = None
        self.__engine_power_loss = None
        
        self.set_altitude(0.0)
    
    def set_altitude(self, altitude):
        try:
            if self.altitude_SL <= altitude <= self.altitude_upr_margin:
                self.__altitude = altitude
                self.__calculate()
            else:
                raise ValueError("Too high!")
        except ValueError as e:
            print(e)
    
    def __calculate_temperature(self):
        if self.__altitude <= self.altitude_troposphere_upr_margin:
            self.__temperature = ((self.__altitude - self.altitude_SL) * self.temperature_gradient_upto_11km
                                  + self.temperature_standard_SL)
        elif self.altitude_troposphere_upr_margin < self.__altitude <= self.altitude_stratosphere_upr_margin:
            self.__temperature = self.temperature_in_stratosphere
        elif self.altitude_troposphere_upr_margin < self.__altitude:
            self.__temperature = ((self.__altitude - self.altitude_stratosphere_upr_margin)
                                  * self.temperature_gradient_upto_32km
                                  + self.temperature_in_stratosphere)
        
        # print(f'T ({self.__altitude}) = {self.__temperature:.5f}')
    
    def __calculate_pressure(self):
        m1 = 1
        m2 = 1
        lg_pressure = 0
        if self.__altitude <= self.altitude_troposphere_upr_margin:
            m1 = self.g_upto_11km / (self.temperature_gradient_upto_11km * self.relative_gas_constant)
            m2 = self.__temperature / self.temperature_standard_SL
            lg_pressure = math.log10(self.pressure_standard_SL) - m1 * math.log10(m2)
            # self.__pressure = 10 ** lg_pressure
        elif self.altitude_troposphere_upr_margin < self.__altitude <= self.altitude_stratosphere_upr_margin:
            lg_pressure = (math.log10(self.pressure_standard_11km) -
                           (self.pressure_stratosphere_coefficient * self.g_over_11_upto_20km /
                            (self.relative_gas_constant * self.__temperature)) *
                           (self.__altitude - self.altitude_troposphere_upr_margin)
                           )
        elif self.altitude_stratosphere_upr_margin < self.__altitude:
            m1 = self.g_over_20km / (self.temperature_gradient_upto_32km * self.relative_gas_constant)
            m2 = self.__temperature / self.temperature_in_stratosphere
            lg_pressure = math.log10(self.pressure_standard_20km) - m1 * math.log10(m2)
        else:
            pass
        self.__pressure = 10 ** lg_pressure
        
        # print(f'pressure({self.__altitude}) = {self.__pressure:.5e}')
    
    def __calculate_density(self):
        self.__density = self.__pressure / self.__temperature / self.relative_gas_constant
        # print(f'density at {self.__altitude} = {self.__density:.4e}')
    
    def __calculate_viscosity(self):
        self.__dynamic_viscosity = self.beta_s * self.__temperature ** (3 / 2) / (self.__temperature + self.S)
        self.__cinematic_viscosity = self.__dynamic_viscosity / self.__density
        # print(f'dynamic viscosity at {self.__altitude} = {self.__dynamic_viscosity}'
        #       f' when cinematic viscosity = {self.__cinematic_viscosity}')
    
    def __calculate_engine_power_loss(self):
        self.__engine_power_loss = 1 / (1.11 * self.__density / self.density_standard_SL
                                        * math.sqrt(self.temperature_standard_SL / self.__temperature) - 0.11)
    
    def __calculate(self):
        self.__calculate_temperature()
        self.__calculate_pressure()
        self.__calculate_density()
        self.__calculate_viscosity()
        self.__calculate_engine_power_loss()
    
    '''
    +++++++++++ getters area ++++++++++++
    '''
    
    def get_parameters(self):
        return {'H': self.__altitude,
                'T': self.__temperature,
                'P': self.__pressure,
                'rho': self.__density,
                'myu': self.__dynamic_viscosity,
                'nyu': self.__cinematic_viscosity,
                'rel_power': self.__engine_power_loss
                }
    
    def get_altitude(self):
        return self.__altitude
    
    def get_temperature(self):
        return self.__temperature
    
    def get_pressure(self):
        return self.__pressure
    
    def get_density(self):
        return self.__density
    
    def get_dynamic_viscosity(self):
        return self.__dynamic_viscosity
    
    def get_cinematic_viscosity(self):
        return self.__cinematic_viscosity
    
    def get_engine_power_loss(self):
        return self.__engine_power_loss
    
    def get_params_by_altitude(self, altitude):
        self.set_altitude(altitude)
        return self.get_parameters()
    
    '''
    +++++++++++ end of getters area ++++++++++++
    '''

#
# if __name__ == '__main__':
#     isa = ISA()
#     alt_range = np.arange(0.0, 5001.0, 1000.0)
#     atmosphere_range = [isa.get_params_by_altitude(x) for x in alt_range]
#     print(atmosphere_range[1]['H'])
#     for i in atmosphere_range:
#         print(i['H'], i['rho'], i['nyu'], f'power loss: {(100 * 0.55 * 0.75 - (450 / 20 / 75 * 30)) / i['rel_power'] - 4}')
