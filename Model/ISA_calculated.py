import math


# from accessify import private


class ISAcalc:
    sea_level_temperature = 288
    sea_level_density = 1.225
    
    def __init__(self):
        self.__altitude = None
        self.__density = None
        self.__temperature = None
        self.__dynamic_viscosity = None
        self.__cinematic_viscosity = None
        self.__engine_power_loss = None
        # pass
    
    def calculate_parameters(self):
        self.__density = self.sea_level_density * (24000 - self.__altitude) / (24000 + self.__altitude)
        self.__temperature = self.sea_level_temperature - self.__altitude * 0.0065
        self.__dynamic_viscosity = 0.0000179 * (self.__temperature / self.sea_level_temperature) ** 0.76
        self.__cinematic_viscosity = self.__dynamic_viscosity / self.__density
        self.__engine_power_loss = 1 / (1.11 * self.__density / self.sea_level_density
                                        * math.sqrt(self.sea_level_temperature / self.__temperature) - 0.11)
    
    def set_altitude(self, altitude):
        if altitude <= 12000:
            self.__altitude = altitude
        else:
            self.__altitude = 12000
        self.calculate_parameters()
    
    def get_density(self):
        return self.__density
    
    def get_temperature(self):
        return self.__temperature
    
    def get_dynamic_viscosity(self):
        return self.__dynamic_viscosity
    
    def get_cinematic_viscosity(self):
        return self.__cinematic_viscosity
    
    def get_engine_power_loss(self):
        return self.__engine_power_loss
    
    def get_altitude(self):
        return self.__altitude


if __name__ == '__main__':
    check_alt = 5000
    isa = ISAcalc()
    isa.set_altitude(check_alt)
    
    rho = isa.get_density()
    kelvins = isa.get_temperature()
    dyn_visc = isa.get_dynamic_viscosity()
    cinem_visc = isa.get_cinematic_viscosity()
    
    print(f'rho(3000) = {rho}')
    print(f'Kelvins(3000) = {kelvins}')
    print(f'dynamic viscosity(3000) = {dyn_visc:.5e}')
    print(f'cinematic viscosity(3000) = {cinem_visc:.5e}')
    print(f'engine loss = {1 / isa.get_engine_power_loss()}')
    
    print(isa.get_altitude())
