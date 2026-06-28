# from input_parameters_2 import plane_params as pp
import numpy as np


# __DEBUG__ = True
__DEBUG__ = False

class LiftingSurface:

    def __init__(self):
        self.calculated = False
        # super.__init__(self)
        # self.input_geometry = pp['geometry']['wing']
        # self.general_geometry = {}
        # fast access parameters
        self.types = ["rectangle", "trapezoid", "elliptic"]
        self.type = None
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

    # SETTERS AREA
    def set_general_geometry(self, area=40, aspect_ratio=10, taper_ratio_ru=2.0, sweep_angle_25=0.0):
        self.area = area
        self.aspect_ratio = aspect_ratio
        self.taper_ratio_ru = taper_ratio_ru
        self.taper_ratio_en = 1 / taper_ratio_ru
        self.sweep_angle_25 = sweep_angle_25
        self.calculate_geometry()

    def set_general_geometry_2(self, **params):
        self.area = params['area']
        self.aspect_ratio = params['aspect_ratio']

        if params["type"] in self.types:
            self.type = params["type"]
        else:
            print(f'wrong surface type: need be in {self.types}')
            return
        # if params["type"] == "elliptic":

###  ++++++++++++ to be cleared up =============
        self.taper_ratio_ru = params['taper_ratio_ru']
        self.taper_ratio_en = 1 / self.taper_ratio_ru
###  !!  ++++++++++++ to be cleared up =============

        self.sweep_angle_25 = params['sweep_angle_25']
        self.calculate_geometry()

    def set_ratios(self, aspect_ratio, taper_ratio_ru=2.0, sweep_angle_25=0.0):
        self.aspect_ratio = aspect_ratio
        self.taper_ratio_ru = taper_ratio_ru
        self.taper_ratio_en = 1 / taper_ratio_ru
        self.sweep_angle_25 = sweep_angle_25
        self.calculate_geometry()

    def set_area(self, area):
        self.area = area
        self.calculate_geometry()

    def set_span(self, span):
        aspect_ratio = span ** 2 / self.area
        self.span = span
        self.set_aspect_ratio(aspect_ratio)

    def set_aspect_ratio(self, aspect_ratio):
        self.aspect_ratio = aspect_ratio
        self.calculated = False
        self.calculate_geometry()

    def set_taper_ratio_ru(self, taper_ratio_ru):
        self.taper_ratio_ru = taper_ratio_ru
        self.taper_ratio_en = 1 / taper_ratio_ru
        self.calculate_geometry()

    # !SETTTERS AREA


    def calculate_geometry(self):
        self.span = np.sqrt(self.aspect_ratio * self.area)
        self.MGC = np.sqrt(self.area / self.aspect_ratio)
        if __DEBUG__ :
            print(f'in calculate_geometry, span = {self.span}')
        if self.type == "elliptic": self.calculate_plane_elliptic()
        elif self.type == "trapezoid": self.calculate_plane_trapezoid()
        elif self.type == "rectangle": self.calculate_plane_rectangle()
        else: self.calculate_plane_rectangle()
        self.calculated = True

    def calculate_plane_trapezoid(self):
        self.root_chord = self.MGC * (1 + ((self.taper_ratio_ru - 1) / (self.taper_ratio_ru + 1)))
        self.tip_chord = self.root_chord / self.taper_ratio_ru
        self.MAC = (self.root_chord * (2 / 3)
                    * ((1 + self.taper_ratio_en + self.taper_ratio_en ** 2) / (1 + self.taper_ratio_en))
                    )

    def calculate_plane_rectangle(self):
        self.root_chord = self.MGC
        self.tip_chord = self.root_chord
        self.MAC = self.MGC


    def calculate_plane_elliptic(self):
        self.root_chord = (self.area * 4 / (self.span * np.pi))
        self.tip_chord = 0.001 # just a cap for elliptic plane
        self.MAC = 8 / (3 * np.pi) * self.root_chord
        self.taper_ratio_ru = (self.root_chord / self.MAC) ** 2
        self.taper_ratio_en = 1 / self.taper_ratio_ru

    def print_geometry(self):
        d = self.collect_general_geometry()
        for k in d:
            try:
                print(f'{k}: {d[k]:.4f}')
            except TypeError:
                print(f'Value of {k} is not set yet.')

    def get_general_geometry(self):
        return self.collect_general_geometry()

    def collect_general_geometry(self):
        return {
            'area': float(self.area),
            'aspect_ratio': float(self.aspect_ratio),
            'taper_ratio_ru': float(self.taper_ratio_ru),
            'taper_ratio_en': float(self.taper_ratio_en),
            'sweep_angle_25': float(self.sweep_angle_25),
            'span': float(self.span),
            'root_chord': float(self.root_chord),
            'tip_chord': float(self.tip_chord),
            'MGC': float(self.MGC),
            'MAC': float(self.MAC)
        }


if __name__ == '__main__':
    w = LiftingSurface()
    params = {"type": "trapezoid"
    # params = {"type": "elliptic"
        , "area": 3.0
        , "aspect_ratio": 12
        , "sweep_angle_25": 0.0
        , "taper_ratio_ru": 2.5
        }
    w.set_general_geometry_2(**params)
    out = w.get_general_geometry()
    print(out)
    # w.set_area(39.6)
    # w.set_span(22.0)
    # w.set_taper_ratio_ru(2.6)
    # w.print_geometry()
    # w.set_area(33.0)
    # w.set_aspect_ratio(27.3)
    # w.set_taper_ratio_ru(4)
    # w.print_geometry()
    
    # w.set_span(0.4)
    # print('\n')
    # w.print_geometry()
    
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
