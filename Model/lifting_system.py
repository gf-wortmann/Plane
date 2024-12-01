import numpy as np
import wing
import inspect


class LiftingSystem:
    def __init__(self, fins_count=1, stab_volume_coefficient=0.5, fin_volume_coefficient=0.05):
        self.__calculated = False
        self.__wing = wing.Wing()
        self.__stab = wing.Wing()
        self.__fin = wing.Wing()
        self.__fins_count = fins_count
        #+++++++++++++++++++++++++++++++++++
        self.__tail_arm_ratio = 0.375
        self.__tail_arm = None
        self.__stab_arm = None
        self.__fin_arm = None
        self.__stab_volume_coefficient = stab_volume_coefficient
        self.__fin_volume_coefficient = fin_volume_coefficient
    
    def are_parts_calculated(self):
        # result = False
        wing_calculated = self.__wing.calculated
        stab_calculated = self.__stab.calculated
        fin_calculated = self.__fin.calculated
        return wing_calculated and stab_calculated and fin_calculated
    
    def is_lifting_system_calculated(self):
        return self.__calculated
    
    def calculate_lifting_system(self):
        if not self.is_lifting_system_calculated():
            self.calculate_parts()
    
    def calculate_parts(self):
        if not self.are_parts_calculated():
            if not self.__wing.calculated:
                self.__wing.calculate_geometry()
            if not self.__stab.calculated:
                self.__stab.calculate_geometry()
            if not self.__fin.calculated:
                self.__fin.calculate_geometry()
    
    def set_fin_volume_coefficient(self, fin_volume_coefficient):
        self.__fin_volume_coefficient = fin_volume_coefficient
        self.__calculated = False
    
    def set_stab_volume_coefficient(self, stab_volume_coefficient):
        self.__stab_volume_coefficient = stab_volume_coefficient
        self.__calculated = False
    
    def set_tail_arm(self, tail_arm):
        self.__tail_arm = tail_arm
        if self.__wing.span:
            self.__tail_arm_ratio = self.__tail_arm / self.__wing.span
        self.__calculated = False
    
    # def set_lifting_surface(self, surface: wing.Wing, area, aspect_ratio, taper_ratio_ru=2.0, sweep_angle_25=0.0):
    #     surface.set_general_geometry(area, aspect_ratio, taper_ratio_ru, sweep_angle_25)
    #     surface.calculate_geometry()
    #
    def set_wing_general_geometry(self, area, aspect_ratio, taper_ratio_ru=2.0, sweep_angle_25=0.0):
        self.__wing.set_general_geometry(area, aspect_ratio, taper_ratio_ru, sweep_angle_25)
        self.__wing.calculate_geometry()
    
    def set_stab_general_geometry(self, area, aspect_ratio, taper_ratio_ru=1.0, sweep_angle_25=0.0):
        self.__stab.set_general_geometry(area, aspect_ratio, taper_ratio_ru, sweep_angle_25)
        self.__stab.calculate_geometry()
    
    def set_fin_general_geometry(self, area, aspect_ratio, taper_ratio_ru=1.0, sweep_angle_25=0.0):
        self.__fin.set_general_geometry(area, aspect_ratio, taper_ratio_ru, sweep_angle_25)
        self.__fin.calculate_geometry()
    
    def calculate_stab_area(self, stab_arm, stab_volume_coefficient):
        self.__stab_arm = stab_arm
        if self.__fin_arm is not None:
            self.__tail_arm = (self.__stab_arm + self.__fin_arm) / 2.0
        self.__stab_volume_coefficient = stab_volume_coefficient
        if self.__wing.MAC is not None and self.__wing.area is not None:
            return self.__stab_volume_coefficient * self.__wing.area * self.__wing.MAC / self.__stab_arm
        else:
            return None
    
    def calculate_fin_area(self, fin_arm, fin_volume_coefficient):
        self.__fin_arm = fin_arm
        if self.__stab_arm is not None:
            self.__tail_arm = (self.__stab_arm + self.__fin_arm) / 2.0
        self.__fin_volume_coefficient = fin_volume_coefficient
        if self.__wing.span is not None and self.__wing.area is not None:
            return self.__fin_volume_coefficient * self.__wing.area * self.__wing.span / self.__fin_arm / self.__fins_count
        else:
            return None
    
    def set_tail_srf_general_geometry(self, stab_arm, fin_arm, stab_volume_coefficient=0.5, fin_volume_coefficient=0.05
                                      , stab_aspect_ratio=4.0, stab_taper_ratio_ru=1.0, stab_sweep_angle_25=0.0
                                      , fin_aspect_ratio=1.5, fin_taper_ratio_ru=1.0, fin_sweep_angle_25=2.0):
        stab_area = self.calculate_stab_area(stab_arm, stab_volume_coefficient)
        fin_area = self.calculate_fin_area(fin_arm, fin_volume_coefficient)
        
        self.set_stab_general_geometry(stab_area, stab_aspect_ratio, stab_taper_ratio_ru, stab_sweep_angle_25)
        self.set_fin_general_geometry(fin_area, fin_aspect_ratio, fin_taper_ratio_ru, fin_sweep_angle_25)
    
    # getters area++++++++++++++++++++++++++
    def get_wing_area(self):
        return self.__wing.area
    
    def get_wing_span(self):
        return self.__wing.span
    
    def get_wing_aspect_ratio(self):
        return self.__wing.aspect_ratio
    
    def get_stab_area(self):
        return self.__stab.area
    
    def get_stab_span(self):
        return self.__stab.span
    
    def get_stab_aspect_ratio(self):
        return self.__stab.aspect_ratio
    
    def get_fin_area(self):
        return self.__fin.area
    
    def get_fin_span(self):
        return self.__fin.span
    
    def get_fin_aspect_ratio(self):
        return self.__fin.aspect_ratio

# /getters area++++++++++++++++++++++++++


if __name__ == '__main__':
    ls = LiftingSystem(fins_count=2)
    ls.set_wing_general_geometry(36, 13.5, 2.5, 0.0)
    # ls.set_stab_general_geometry(8.0, 4.0, 1.0, 0.0)
    ls.set_tail_srf_general_geometry(7.7, 7.3, 1.0, 0.08
                                     , stab_aspect_ratio=4.0, fin_aspect_ratio=2.0, fin_sweep_angle_25=5.0
                                     , stab_taper_ratio_ru=1.0, fin_taper_ratio_ru=1.0)
    
    print(f'wing area = {ls.get_wing_area()}, wing span = {ls.get_wing_span()}')
    print(f'stab area = {ls.get_stab_area()}, stab span = {ls.get_stab_span()}')
    print(f'fin area = {ls.get_fin_area()}, fin span = {ls.get_fin_span()}')
