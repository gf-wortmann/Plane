import numpy as np
import math


class CoolingSystem:
    
    # '''constants'''
    
    # '''/constants'''
    
    def __init__(self):
        # '''geometry'''
        
        self.__cylinder_dia = 10  # D in centimeters
        self.__cylinder_dia_mm = 100  #
        self.__cylinders_number = 8  # i
        
        # '''/geometry'''
        # ratios
        self.__prop_coefft_1 = 0.49  # c - proportionality coefficient
        # self.__prop_coefft_2 = 1.6e-3  # c - proportionality coefficient - Diesels
        self.__prop_coefft_2 = 2.9e-3  # c - proportionality coefficient - spark machines
        self.__math_power_coefft = 0.65  # math power coefft for 4-stroke engines
        
        
        # /ratios
        
        # CHEMISTRY
        self.__heat_burning_lwr = 44.0  # Hu, Specific heat of burning, MJ/kg gasoline, spark ignition
#        self.__heat_burning_lwr = 44000.0  # Hu, Specific heat of burning, kJ/kg gasoline, spark ignition
        self.__delta_Hu = None
        self.__heat_alpha = None  # Heat corrected by mixture grade
        self.__mixture_grade = 1.1  # alpha, spark
        # self.__mixture_grade = 1.4  # alpha, diesel
        self.__stoichio_coefft = 0.51  # Stoichiometric coefficient, spark ignition
        self.__calc_delta_hu()
        self.__calc_heat_alpha()
        # /CHEMISTRY
        
        # working
        self.__rotations_per_minute = 5000
        self.__flux_outward_1 = None
        self.__flux_outward_2 = None
        self.__flux_outward_3 = None
        
        # self.set_rotation_per_second()
        self.__calc_flux_outward_1()
        self.__calc_flux_outward_2()
        self.__calc_flux_outward_3()
        # /working
    
    '''setters'''
    
    def set_rotation_per_minute(self, rps):
        self.__rotations_per_minute = rps
        self.recalculate()
    
    def set_hu(self, hu):
        self.__heat_burning_lwr = hu
    
    def set_mixture_grade(self, mg):
        self.__mixture_grade = mg
        self.__calc_delta_hu()
        
    def set_stoichio_coefft(self, sc):
        self.__stoichio_coefft = sc
        self.__calc_delta_hu()
    
    def set_cyl_dia_cm(self, dia):
        self.__cylinder_dia = dia
        self.__set_cyl_dia_mm()
    
    def __set_cyl_dia_mm(self):
        self.__cylinder_dia_mm = self.__cylinder_dia * 10
    
    def set_cylinders_number(self, cnum):
        self.__cylinders_number = cnum
    
    
    '''/setters'''
    
    '''calculators'''
    
    def recalculate(self):
        self.__calc_delta_hu()
        self.__calc_heat_alpha()
        self.__calc_flux_outward_1()
        self.__calc_flux_outward_2()
        self.__calc_flux_outward_3()
        
    
    def __calc_delta_hu(self):
        self.__delta_Hu = 119.95 * (1 - self.__mixture_grade) * self.__stoichio_coefft
        
    def __calc_flux_outward_1(self):
        self.__flux_outward_1 = (self.__prop_coefft_1 * self.__cylinders_number
                                 * self.__cylinder_dia ** (1 + 2 * self.__math_power_coefft)
                                 * self.__rotations_per_minute ** self.__math_power_coefft
                                 * (self.__heat_burning_lwr - self.__delta_Hu)
                                 / (self.__mixture_grade * self.__heat_burning_lwr)
                                 )
        
    def __calc_flux_outward_2(self):
        self.__flux_outward_2 = ((self.__prop_coefft_2 * self.__cylinders_number
                                * self.__cylinder_dia_mm ** (1 + 2 * self.__math_power_coefft))
                                 * self.__rotations_per_minute ** self.__math_power_coefft) / self.__mixture_grade
        
    def __calc_flux_outward_3(self):
        self.__flux_outward_3 = (((self.__prop_coefft_2 * self.__cylinders_number
                                 * self.__cylinder_dia_mm ** (1 + 2 * self.__math_power_coefft))
                                  * self.__rotations_per_minute ** self.__math_power_coefft)
                               * self.__heat_alpha / (self.__mixture_grade * self.__heat_burning_lwr))
    
    def __calc_heat_alpha(self):
        if self.__mixture_grade <= 1.0:
            self.__heat_alpha = self.__heat_burning_lwr * (1.39 * self.__mixture_grade - 0.39)
        elif self.__mixture_grade > 1.0:
            self.__heat_alpha = 0.94 * self.__heat_burning_lwr * self.__mixture_grade ** 0.11
            
        
    
    '''/calculators'''
    
    '''getters'''
    def get_cylinders_number(self):
        return self.__cylinders_number

    def get_cylinder_dia_cm(self):
        return self.__cylinder_dia

    def get_cylinder_dia_mm(self):
        return self.__cylinder_dia_mm
    
    def get_flux_outward_1(self):
        return self.__flux_outward_1

    def get_flux_outward_2(self):
        return self.__flux_outward_2
    
    def get_flux_outward_3(self):
        return self.__flux_outward_3
    
    '''/getters'''


if __name__ == '__main__':
    lt = CoolingSystem()
    lt.set_rotation_per_minute(6450)
    lt.set_cyl_dia_cm(10.325)
    lt.set_cylinders_number(8)
    lt.recalculate()
    print(f' LT flux 1 = {lt.get_flux_outward_1()}')
    print(f' LT flux 2 = {lt.get_flux_outward_2()}')
    print(f' LT flux 3 = {lt.get_flux_outward_3()}')
    
    rotax = CoolingSystem()
    rotax.set_rotation_per_minute(5800)
    rotax.set_cyl_dia_cm(8.4)
    rotax.set_cylinders_number(4)
    rotax.recalculate()
    print(f' rotax flux 1 = {rotax.get_flux_outward_1()}')
    print(f' rotax flux 2 = {rotax.get_flux_outward_2()}')
    print(f' rotax flux 3 = {rotax.get_flux_outward_3()}')
    
    