# from input_parameters_2 import plane_params as pp
import numpy as np


class Wing:
    
    def __init__(self):
        self.calculated = False
        # super.__init__(self)
        # self.input_geometry = pp['geometry']['wing']
        # self.general_geometry = {}
        # fast access parameters
        self.area = 40.0
        self.aspect_ratio = 12.5
        self.taper_ratio_ru = 2.5
        self.taper_ratio_en = 1 / self.taper_ratio_ru
        self.sweep_angle_25 = 0.0
        self.span = None
        self.root_chord = None
        self.tip_chord = None
        self.MGC = None
        self.MAC = None
        self.calculate_geometry()
        # /fast access parameters
        # self.const = const
        # self.ISA = isa
    
    def set_general_geometry(self, area, aspect_ratio, taper_ratio_ru=2.0, sweep_angle_25=0.0):
        self.area = area
        self.aspect_ratio = aspect_ratio
        self.taper_ratio_ru = taper_ratio_ru
        self.taper_ratio_en = 1 / taper_ratio_ru
        self.sweep_angle_25 = sweep_angle_25
        self.calculate_geometry()
    
    def set_area(self, area):
        self.area = area
        self.calculate_geometry()
    
    def set_aspect_ratio(self, aspect_ratio):
        self.aspect_ratio = aspect_ratio
        self.calculate_geometry()
    
    def set_taper_ratio_ru(self, taper_ratio_ru):
        self.taper_ratio_ru = taper_ratio_ru
        self.taper_ratio_en = 1 / taper_ratio_ru
        self.calculate_geometry()
    
    def calculate_geometry(self):
        self.span = np.sqrt(self.aspect_ratio * self.area)
        self.MGC = np.sqrt(self.area / self.aspect_ratio)
        self.root_chord = self.MGC * (1 + ((self.taper_ratio_ru - 1) / (self.taper_ratio_ru + 1)))
        self.tip_chord = self.root_chord / self.taper_ratio_ru
        self.MAC = (self.root_chord * (2 / 3)
                    * ((1 + self.taper_ratio_en + self.taper_ratio_en ** 2) / (1 + self.taper_ratio_en))
                    )
        self.calculated = True
        
    def print_geometry(self):
        d = self.collect_general_geometry()
        for k in d:
            try:
                print(f'{k}: {d[k]:.2f}')
            except TypeError:
                print(f'Value of {k} is not set yet.')
    
    def get_general_geometry(self):
        return self.collect_general_geometry()
    
    def collect_general_geometry(self):
        return {
            'area': self.area,
            'aspect_ratio': self.aspect_ratio,
            'taper_ratio_ru': self.taper_ratio_ru,
            'taper_ratio_en': self.taper_ratio_en,
            'sweep_angle_25': self.sweep_angle_25,
            'span': self.span,
            'root_chord': self.root_chord,
            'tip_chord': self.tip_chord,
            'MGC': self.MGC,
            'MAC': self.MAC
        }


if __name__ == '__main__':
    w = Wing()
    # w.print_geometry()
    # w.set_area(33.0)
    # w.set_aspect_ratio(27.3)
    # w.set_taper_ratio_ru(4)
    w.print_geometry()
    
    # w.get_geometry()
    # g = pp['geometry']['wing']
    # w.set_geometry(g)
    # w.get_geometry()
    # print(w)
    
    # for p in pp['geometry']['wing']:
    #     print(pp['geometry']['wing'][p])
    #
    
    # aa = pp['geometry']['wing']
    # print(aa)
    # print(type(aa))
    # print(pp['geometry']['wing'])
