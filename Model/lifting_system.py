import numpy as np
from Model import lifting_surface as ls
import inspect


class LiftingSystem:
    def __init__(self, wing_area: float = 10.0, wing_aspect_ratio: float = 10.0, fins_count: int = 1
                 , stab_volume_coefficient: float = 0.5, fin_volume_coefficient: float = 0.05):
        self.__calculated = False
        self.__wing = ls.LiftingSurface()
        self.__wing.set_area(wing_area)
        self.__wing.set_aspect_ratio(wing_aspect_ratio)
        self.__wing.calculate_geometry()
        self.__stab = ls.LiftingSurface()
        self.__fin = ls.LiftingSurface()
        self.__fins_count = fins_count
        # +++++++++++++++++++++++++++++++++++
        self.__tail_arm_ratio = 0.375
        self.__tail_arm = self.get_wing_span() * self.__tail_arm_ratio
        self.__stab_arm = self.__tail_arm
        self.__fin_arm = self.__tail_arm
        self.__stab_volume_coefficient = stab_volume_coefficient
        self.calculate_stab_area(self.__stab_arm, self.__stab_volume_coefficient)
        self.__fin_volume_coefficient = fin_volume_coefficient
        self.calculate_fin_area(self.__fin_arm, self.__fin_volume_coefficient)
    
    def are_parts_calculated(self):
        # result = False
        wing_calculated = self.__wing.calculated
        stab_calculated = self.__stab.calculated
        fin_calculated = self.__fin.calculated
        return wing_calculated and stab_calculated and fin_calculated
    
    def is_lifting_system_calculated(self):
        return self.__calculated
    
    '''___calculators area___'''
    
    def calculate_lifting_system(self):
        if not self.is_lifting_system_calculated():
            self.calculate_parts()
        self.__calculated = True
    
    def calculate_parts(self):
        # if not self.are_parts_calculated():
        #     if not self.__wing.calculated:
        # calculate_stab_area(self.__stab_arm, self.__stab_volume_coefficient)
        self.__wing.calculate_geometry()
        # self.__wing.calculated = True
        # if not self.__stab.calculated:
        self.calculate_stab_area(self.__stab_arm, self.__stab_volume_coefficient)
        self.__stab.calculate_geometry()
        # if not self.__fin.calculated:
        self.calculate_fin_area(self.__fin_arm, self.__fin_volume_coefficient)
        self.__fin.calculate_geometry()
    
    def calculate_stab_area(self, stab_arm, stab_volume_coefficient):
        self.__stab_arm = stab_arm
        if self.__fin_arm is not None:
            self.__tail_arm = (self.__stab_arm + self.__fin_arm) / 2.0
        self.__stab_volume_coefficient = stab_volume_coefficient
        if self.__wing.MAC is not None and self.__wing.area is not None:
            self.__stab.area = self.__stab_volume_coefficient * self.__wing.area * self.__wing.MAC / self.__stab_arm
            return self.__stab.area
        else:
            return None
    
    def calculate_fin_area(self, fin_arm, fin_volume_coefficient):
        self.__fin_arm = fin_arm
        if self.__stab_arm is not None and self.__fin_arm is not None:
            self.__tail_arm = (self.__stab_arm + self.__fin_arm) / 2.0
        self.__fin_volume_coefficient = fin_volume_coefficient
        if self.__wing.span is not None and self.__wing.area is not None:
            self.__fin.area = (self.__fin_volume_coefficient * self.__wing.area * self.__wing.span
                               / self.__fin_arm / self.__fins_count)
            return self.__fin.area
        else:
            return None
    
    '''_____end_of_calculators ares____'''
    
    '''___setters_area____'''
    
    def set_lifting_system_general_geometry(self, **params):
        self.set_wing_general_geometry(params['wing_area'], params['wing_aspect_ratio'], params['wing_taper_ratio_ru'],
                                       params['wing_sweep_angle_25'])
        self.set_tail_general_geometry(
            params['stab_arm'], params['fin_arm'], params['stab_volume_coefficient'], params['fin_volume_coefficient'],
            params['stab_aspect_ratio'], params['stab_taper_ratio_ru'], params['stab_sweep_angle_25'],
            params['fin_aspect_ratio'], params['fin_taper_ratio_ru'], params['fin_sweep_angle_25'],
            params['fins_count'])
        self.calculate_parts()
        # self.__wing.set_span(params['wing_span'])
        # self.__stab.set_span(params['stab_span'])
        # self.__fin.set_span(params['fin_span'])
    
    def set_lifting_system_general_geometry_2(self, **params):
        _wing = params['wing']
        _stab = params['stab']
        _fin = params['fin']
        _ls = params['lifting_system']
        
        self.set_wing_general_geometry(_wing['area'], _wing['aspect_ratio'], _wing['taper_ratio_ru'],
                                       _wing['sweep_angle_25'])
        self.set_stab_general_geometry(_stab['area'], _stab['aspect_ratio'], _stab['taper_ratio_ru'],
                                       _stab['sweep_angle_25'])
        self.set_fin_general_geometry(_fin['area'], _fin['aspect_ratio'], _fin['taper_ratio_ru'],
                                      _fin['sweep_angle_25'])
        # print(f'in set general lifting system 2: {_fin}')
        
        self.set_tail_general_geometry_2(
            _ls['stab_arm'], _ls['fin_arm'], _ls['stab_volume_coefficient'], _ls['fin_volume_coefficient'],
            _ls['fins_count'])
        # self.calculate_parts()
    
    def set_fins_count(self, fins_count: int):
        self.__fins_count = fins_count
        self.calculate_fin_area(self.__fin_arm, self.__fin_volume_coefficient)
        self.__fin.calculate_geometry()
    
    def set_wing_general_geometry(self, area, aspect_ratio, taper_ratio_ru=2.0, sweep_angle_25=0.0):
        self.__wing.set_general_geometry(area, aspect_ratio, taper_ratio_ru, sweep_angle_25)
        self.__wing.calculate_geometry()
    
    def set_wing_area(self, area):
        self.__wing.set_area(area)
        self.__wing.calculate_geometry()
        self.calculate_lifting_system()
        self.calculate_parts()
    
    def set_wing_taper_ratio_ru(self, taper_ratio):
        self.__wing.set_taper_ratio_ru(taper_ratio)
        self.__wing.calculate_geometry()
        self.calculate_lifting_system()
        self.calculate_parts()
    
    def set_wing_aspect_ratio(self, aspect_ratio):
        self.__wing.set_aspect_ratio(aspect_ratio)
        self.__calculated = False
        self.__wing.calculated = False
        self.__stab.calculated = False
        self.__fin.calculated = False
        self.calculate_lifting_system()
        self.calculate_parts()
    
    def set_wing_span(self, span):
        self.__wing.set_span(span)
        self.__wing.calculated = False
        self.calculate_lifting_system()
        self.calculate_parts()
    
    def set_stab_volume_coefficient(self, stab_volume_coefficient):
        self.__stab_volume_coefficient = stab_volume_coefficient
        self.__calculated = False
        self.calculate_lifting_system()
        self.calculate_parts()
    
    def set_stab_general_geometry(self, area, aspect_ratio, taper_ratio_ru=1.0, sweep_angle_25=0.0):
        self.__stab.set_general_geometry(area, aspect_ratio, taper_ratio_ru, sweep_angle_25)
        self.__stab.calculate_geometry()
    
    def set_stab_arm(self, stab_arm):
        self.__stab_arm = stab_arm
        self.__calculated = False
        self.calculate_lifting_system()
    
    def set_stab_aspect_ratio(self, aspect_ratio):
        self.__stab.set_aspect_ratio(aspect_ratio)
        # self.__stab.calculate_geometry()
    
    def set_stab_span(self, span):
        self.__stab.set_span(span)
        # self.__stab.calculate_geometry()
    
    def set_tail_arm(self, tail_arm):
        self.__tail_arm = tail_arm
        if self.__wing.span:
            self.__tail_arm_ratio = self.__tail_arm / self.__wing.span
        self.__calculated = False
    
    def set_tail_general_geometry(self, stab_arm, fin_arm, stab_volume_coefficient=0.5, fin_volume_coefficient=0.05,
                                  stab_aspect_ratio=4.0, stab_taper_ratio_ru=1.0, stab_sweep_angle_25=0.0,
                                  fin_aspect_ratio=2.0, fin_taper_ratio_ru=1.0, fin_sweep_angle_25=2.0,
                                  fins_count=1):
        stab_area = self.calculate_stab_area(stab_arm, stab_volume_coefficient)
        fin_area = self.calculate_fin_area(fin_arm, fin_volume_coefficient)
        
        self.set_stab_general_geometry(stab_area, stab_aspect_ratio, stab_taper_ratio_ru, stab_sweep_angle_25)
        self.set_fin_general_geometry(fin_area, fin_aspect_ratio, fin_taper_ratio_ru, fin_sweep_angle_25)
        self.set_fins_count(fins_count)
        self.calculate_lifting_system()
        self.calculate_parts()
    
    def set_tail_general_geometry_2(self, stab_arm=3.0, fin_arm=3.0, stab_volume_coefficient=0.5, fin_volume_coefficient=0.05,
                                    fins_count=1):
        # print(f'in set gen tail: stab arm = {stab_arm}, fin arm = {fin_arm}')
        self.calculate_stab_area(stab_arm, stab_volume_coefficient)
        self.calculate_fin_area(fin_arm, fin_volume_coefficient)
        
        self.set_fins_count(fins_count)
        self.calculate_lifting_system()
        self.calculate_parts()
    
    def set_fin_arm(self, fin_arm):
        self.__fin_arm = fin_arm
        # if self.__wing.span:
        #     self.__tail_arm_ratio = self.__tail_arm / self.__wing.span
        self.__calculated = False
        self.calculate_lifting_system()
    
    def set_fin_general_geometry(self, area, aspect_ratio, taper_ratio_ru=1.0, sweep_angle_25=0.0):
        self.__fin.set_general_geometry(area, aspect_ratio, taper_ratio_ru, sweep_angle_25)
        self.__fin.calculate_geometry()
        # print(f' fin in ls: {self.__fin.collect_general_geometry()}')
    
    def set_fin_ratios(self, aspect_ratio, taper_ratio_ru=1.0, sweep_angle_25=0.0):
        self.__fin.set_ratios(aspect_ratio, taper_ratio_ru, sweep_angle_25)
        self.__fin.calculate_geometry()
    
    def set_fin_volume_coefficient(self, fin_volume_coefficient):
        self.__fin_volume_coefficient = fin_volume_coefficient
        self.__calculated = False
        self.calculate_lifting_system()
        self.calculate_parts()
    
    def set_fin_aspect_ratio(self, aspect_ratio):
        self.__fin.set_aspect_ratio(aspect_ratio)
    
    '''___ end of setters area____'''
    
    # getters area++++++++++++++++++++++++++
    def get_wing_area(self):
        return self.__wing.area
    
    def get_wing_span(self):
        return self.__wing.span
    
    def get_wing_MAC(self):
        return self.__wing.MAC
    
    def get_wing_aspect_ratio(self):
        return self.__wing.aspect_ratio
    
    def get_stab_area(self):
        return self.__stab.area
    
    def get_stab_arm(self):
        return self.__stab_arm
    
    def get_stab_span(self):
        return self.__stab.span
    
    def get_stab_aspect_ratio(self):
        return self.__stab.aspect_ratio
    
    def get_stab_MAC(self):
        return self.__stab.MAC
    
    def get_fin_area(self):
        return self.__fin.area
    
    def get_fin_arm(self):
        return self.__fin_arm
    
    def get_fins_count(self):
        return self.__fins_count
    
    def get_fin_span(self):
        return self.__fin.span
    
    def get_fin_aspect_ratio(self):
        return self.__fin.aspect_ratio
    
    def get_fin_MAC(self):
        return self.__fin.MAC
    
    def get_fin_root_chord(self):
        return self.__fin.root_chord
    
    def get_fin_tip_cord(self):
        return self.__fin.tip_chord
    
    def get_general_geometry(self):
        w = self.__wing.collect_general_geometry()
        s = self.__stab.collect_general_geometry()
        f = self.__fin.collect_general_geometry()
        lls = {
            "stab_volume_coefficient": float(self.__stab_volume_coefficient),
            "stab_arm": float(self.__stab_arm),
            "fin_volume_coefficient": float(self.__fin_volume_coefficient),
            "fin_arm": float(self.__fin_arm),
            "fins_count": self.__fins_count
        }
        return {'wing': w, 'stab': s, 'fin': f, 'lifting_system': lls}


# /getters area++++++++++++++++++++++++++


if __name__ == '__main__':
    ls = LiftingSystem(fins_count=2)
    ls.set_wing_general_geometry(40, 12.1, 2.6, 0.0)
    # ls.set_stab_general_geometry(8.0, 4.0, 1.0, 0.0)
    ls.set_tail_general_geometry(7.7, 7.3, 1.2, 0.1
                                 , stab_aspect_ratio=5.0, fin_aspect_ratio=2.4, fin_sweep_angle_25=5.0
                                 , stab_taper_ratio_ru=1.0, fin_taper_ratio_ru=1.0)
    #
    # print(ls.is_lifting_system_calculated())
    # print(f'wing area = {ls.get_wing_area()}, wing span = {ls.get_wing_span()}')
    # print(f'stab area = {ls.get_stab_area()}, stab span = {ls.get_stab_span()}')
    # print(f'fin area = {ls.get_fin_area()}, fin span = {ls.get_fin_span()}')
    
    ls.set_wing_aspect_ratio(12.1)
    ls.set_fins_count(2)
    print('\n')
    # print(ls.calculate_stab_area(ls.get_stab_arm(), 1.0))
    print(f'wing area = {ls.get_wing_area()}, wing span = {ls.get_wing_span()}')
    print(f'stab area = {ls.get_stab_area()}, stab span = {ls.get_stab_span()}')
    print(f'fin area = {ls.get_fin_area()}, fin span = {ls.get_fin_span()}')
    
    print(f'Summary tail srf area = {ls.get_stab_area() + ls.get_fin_area() * ls.get_fins_count()}')
    
    # ls.set_fin_volume_coefficient(0.1)
    # ls.set_stab_volume_coefficient(1.0)
    # print(ls.is_lifting_system_calculated())
    # print(f'fin area = {ls.get_fin_area()}, fin span = {ls.get_fin_span()}')
    # print(f'stab area = {ls.get_stab_area()}, stab span = {ls.get_stab_span()}')
    # print(ls.is_lifting_system_calculated())
    # print(f'Summary tail srf area = {ls.get_stab_area() + ls.get_fin_area() * ls.get_fins_count()}')
    #
    ls.set_stab_span(3.0 + 2.4 + 0.25 * 2)
    print(f'stab span is set to {ls.get_stab_span()}')
    print(f'stab area = {ls.get_stab_area()}, stab span = {ls.get_stab_span()}'
          f', stab aspect ratio = {ls.get_stab_aspect_ratio()}')
    print(f'Summary tail srf area = {ls.get_stab_area() + ls.get_fin_area() * ls.get_fins_count()}')
    
    # print('\n')
    # ls.set_stab_arm(ls.get_stab_arm() + 0.6)
    # ls.set_stab_volume_coefficient(1.2)
    # ls.set_stab_span(5.9)
    # ls.set_fin_arm(ls.get_fin_arm() + 0.7)
    # print(f'stab arm = {ls.get_stab_arm()}, fin arm = {ls.get_fin_arm()}')
    # print(f'wing area = {ls.get_wing_area()}, wing span = {ls.get_wing_span()}')
    # print(f'stab area = {ls.get_stab_area()}, stab span = {ls.get_stab_span()}'
    #       f', stab aspect ratio = {ls.get_stab_aspect_ratio()}')
    # print(f'fin area = {ls.get_fin_area()}, fin AR = {ls.get_fin_aspect_ratio()}, fin span = {ls.get_fin_span()}')
    # print(f'Summary tail srf area = {ls.get_stab_area() + ls.get_fin_area() * ls.get_fins_count()}')
    # print('\n')
    # ls.set_fins_count(1)
    # print(f'fins count = {ls.get_fins_count()}')
    # print(f'fin area = {ls.get_fin_area()}, fin AR = {ls.get_fin_aspect_ratio()}, fin span = {ls.get_fin_span():.3f}')
    # print('\n')
    # ls.set_wing_area(40)
    # print(f'wing area = {ls.get_wing_area()}, wing span = {ls.get_wing_span()}')
    # print(f'stab area = {ls.get_stab_area()}, stab span = {ls.get_stab_span()}')
    # print(f'fins count = {ls.get_fins_count()}')
    # print(f'fin area = {ls.get_fin_area()}, fin span = {ls.get_fin_span()}')
    # print('\n')
    # ls.set_wing_area(20)
    # print(f'wing area = {ls.get_wing_area()}, wing span = {ls.get_wing_span()}')
    # print(f'stab area = {ls.get_stab_area()}, stab span = {ls.get_stab_span()}')
    # print(f'fins count = {ls.get_fins_count()}')
    # print(f'fin area = {ls.get_fin_area()}, fin span = {ls.get_fin_span()}')
