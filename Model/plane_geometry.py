from Model import lifting_system as ls
from Model import ISA
import numpy as np
from Formulae import formulae as fe
from matplotlib import pyplot as plt
import json


class PlaneGeometry:
    def __init__(self):
        self.lifting_system = ls.LiftingSystem(fins_count=2, stab_volume_coefficient=1.0, fin_volume_coefficient=0.1)
        self.isa = ISA.ISA()
        self.fuselage_area = 72.0
        self.fuselage_length = 14.0
        self.engine_nacelle_area = 1.7
        self.engine_nacelle_length = 2.2
        self.engine_nacelles_count = 0
        # self.engine_nacelle_area = 9.9
        # self.engine_nacelle_length = 4.5
        # self.engine_nacelles_count = 2
        
        self.cx_0 = 0.02
        self.masse = 5000
    
    def set_lifting_system_general_geometry(self, ls_gen_params):
        self.lifting_system.set_lifting_system_general_geometry_2(**ls_gen_params)
    
    def set_fuselage_general_geometry(self, ls_gen_params):
        params = ls_gen_params["fuselage"]
        # print(f'params = {params}')
        self.fuselage_area = params["area"]
        self.fuselage_length = params["length"]
    
    def get_wing_MAC(self):
        return self.lifting_system.get_wing_MAC()
    
    def get_wing_area(self):
        return self.lifting_system.get_wing_area()
    
    def get_wing_aspect_ratio(self):
        return self.lifting_system.get_wing_aspect_ratio()
    
    def get_stab_MAC(self):
        return self.lifting_system.get_stab_MAC()
    
    def get_stab_area(self):
        return self.lifting_system.get_stab_area()
    
    def get_fin_MAC(self):
        return self.lifting_system.get_fin_MAC()
    
    def get_fin_area(self):
        return self.lifting_system.get_fin_area()
    
    def get_fins_count(self):
        return self.lifting_system.get_fins_count()
    
    def get_fuselage_length(self):
        return self.fuselage_length
    
    def get_fuselage_area(self):
        return self.fuselage_area
    
    def get_nacelle_length(self):
        return self.engine_nacelle_length
    
    def get_nacelle_area(self):
        return self.engine_nacelle_area
    
    # def get_lifting_system_general_geometry(self):
    #     self.lifting_system.w


if __name__ == '__main__':
    p = PlaneGeometry()
    param_file = 'tst2_general_ls_params.json'
    p.set_lifting_system_general_geometry(param_file)
    p.lifting_system.set_stab_span(5.6)
    f = fe.Formulae()
    # p.lifting_system.set_wing_general_geometry(32, 12.5, 2.5, 0.0)
    print(f'wing area= {p.lifting_system.get_wing_area()}')
    print(f'wing aspect ratio= {p.lifting_system.get_wing_aspect_ratio()}')
    ls1 = p.lifting_system
    # # ls.set_tail_srf_general_geometry(8.0, 7.7)
    # ls1.set_stab_arm(8.3)
    # ls1.set_fin_arm(8.0)
    # ls1.set_stab_volume_coefficient(1.0)
    # ls1.set_stab_span(6.0)
    # ls1.set_fin_volume_coefficient(0.1)
    # ls1.calculate_lifting_system()
    # ls1.calculate_parts()
    
    print(f'stab area= {p.lifting_system.get_stab_area()}')
    print(f'stab span= {p.lifting_system.get_stab_span()}')
    print(f'stab aspect ratio= {p.lifting_system.get_stab_aspect_ratio():.2f}')
    print(f'fin area= {p.lifting_system.get_fin_area()}')
    print(f'lifting_system: {p.lifting_system.get_general_geometry()}')
    
    isa = p.isa
    isa.set_altitude(0)
    rp = isa.get_engine_relative_power()
    v_range = np.arange(25, 101, 1)
    # print(f'v_range = {v_range}')
    wing_Re_range = v_range * ls1.get_wing_MAC() / isa.get_cinematic_viscosity()
    stab_Re_range = v_range * ls1.get_stab_MAC() / isa.get_cinematic_viscosity()
    fin_Re_range = v_range * ls1.get_fin_MAC() / isa.get_cinematic_viscosity()
    
    np.set_printoptions(formatter={'float': '{:.3e}'.format})
    print(f'Re ranges, wing: {wing_Re_range} , \n\nstab: {stab_Re_range}, \n\nfin: {fin_Re_range}')
    wing_cx0_range = f.schlichting_mixed_cf(wing_Re_range, 0.2) * 1.7 * 2.05
    # print(f'wing_cx_0 range: {wing_cx0_range}')
    q_range = f.dynamic_pressure(v_range, isa.get_density())
    cy_range = p.masse / ls1.get_wing_area() / q_range
    # print(f' cy: {cy_range}')
    cxi_range = f.cxi(cy_range, ls1.get_wing_aspect_ratio() / 0.9)
    Ka_range = cy_range / (cxi_range + wing_cx0_range * 4)
    # print(f'Ka range: {Ka_range}')
    Nreq_range = p.masse / Ka_range * v_range * 9.81
    # print(f'N required: {Nreq_range}')
    
    isa.set_altitude(3000)
    rp_2 = isa.get_engine_relative_power()
    Re_range_2 = v_range * ls1.get_wing_MAC() / isa.get_cinematic_viscosity()
    wing_cx0_range_2 = f.schlichting_mixed_cf(Re_range_2, 0.2) * 1.7 * 2.05
    q_range_2 = f.dynamic_pressure(v_range, isa.get_density())
    cy_range_2 = p.masse / ls1.get_wing_area() / q_range_2
    cxi_range_2 = f.cxi(cy_range_2, ls1.get_wing_aspect_ratio() / 0.9)
    Ka_range_2 = cy_range_2 / (cxi_range_2 + wing_cx0_range_2 * 4)
    Nreq_range_2 = p.masse / Ka_range_2 * v_range * 9.81
    Nreq_range_2_2 = [p.masse / Ka_range_2 * 9.81 * x for x in v_range]
    
    #+++++++++++++++++++++++++++++++++++++++++++++++++++
    # Plotting the Graph
    plt.plot(v_range * 3.6, Nreq_range / 1000, label=f'N required at 1000m')
    # plt.plot(v_range * 3.6, Ka_range)
    plt.plot(v_range * 3.6, [490 * 2 * rp * .55 * .736 * 0.8 for x in v_range], label=f'N available at 1000m',
             color='r')
    
    plt.plot(v_range * 3.6, Nreq_range_2 / 1000, label=f'N required at 3000m')
    plt.plot(v_range * 3.6, [490 * 2 * rp_2 * .55 * .736 * 0.8 for x in v_range], label=f'N available at 3000m',
             color='k')
    
    plt.title("Required power vs V")
    plt.xlabel("V")
    plt.ylabel("N")
    plt.legend()
    plt.show()
    
    # re, re_ax = plt.subplots(figsize=(10, 7))
    # re_ax.plot(v_range * 3.6, wing_Re_range, label=f'1000m')
    # re_ax.plot(v_range * 3.6, Re_range_2, label=f'3000m')
    # re_ax.set_title('Re vs velocity, altitude = "sea level"')
    # re_ax.set(xlabel='V, kmf', ylabel='Re')
    # re_ax.legend()
    # plt.show()
    #++++++++++++++++++++++++++++++++++++++++++++++++
    
    # ls1.set_stab_arm(9.2)
    # ls1.set_fin_arm(8.8)
    # # ls.set_stab_volume_coefficient(1.0)
    # ls1.set_stab_span(6.0)
    # # ls.set_fin_volume_coefficient(0.1)
    # ls1.calculate_lifting_system()
    # ls1.calculate_parts()
    #
    # print(f'stab area= {p.lifting_system.get_stab_area()}')
    # print(f'stab span= {p.lifting_system.get_stab_span()}')
    # print(f'stab aspect ratio= {p.lifting_system.get_stab_aspect_ratio():.2f}')
    # print(f'fin area= {p.lifting_system.get_fin_area()}')
    #
    # p2 = PlaneGeometry()
    # p2.lifting_system = ls.LiftingSystem(fins_count=1)
    # p2ls = p2.lifting_system
    # p2ls.set_wing_general_geometry(7, 25, 2.5, 1.0)
    # print(f'wing span = {p2ls.get_wing_span()}, wing aspect ratio = {p2ls.get_wing_aspect_ratio()}')
    # p2ls.set_wing_span(13.5)
    # p2ls.set_stab_volume_coefficient(0.5)
    # p2ls.set_fin_volume_coefficient(0.025)
    # p2ls.set_stab_aspect_ratio(6.0)
    # p2ls.set_fin_ratios(2.5, 1.25, 5.0)
    # p2ls.calculate_lifting_system()
    # p2ls.calculate_parts()
    # print(f'small geometry')
    # print(f'wing span = {p2ls.get_wing_span()}, wing aspect ratio = {p2ls.get_wing_aspect_ratio()}')
    # print(f'stab area= {p2ls.get_stab_area()}')
    # print(f'stab span= {p2ls.get_stab_span()}, stab aspect ratio = {p2ls.get_stab_aspect_ratio()}')
    # print(f'stab aspect ratio= {p2ls.get_stab_aspect_ratio():.2f}')
    # print(f'fin area= {p2ls.get_fin_area()}, fin span = {p2ls.get_fin_span()}, fin AR = {p2ls.get_fin_aspect_ratio()}')
    # print(f'fin root chord = {p2ls.get_fin_root_chord()}, fin tip chord = {p2ls.get_fin_tip_cord()}')
    # print(f'fin MAC = {p2ls.get_fin_MAC()}')
    #
    # for a in range(0, 12001, 500):
    #     p2.isa.set_altitude(a)
    #     print(f'Altitude = {p2.isa.get_altitude()}, kelvins = {p2.isa.get_temperature()}'
    #           f', cinematic viscosity = {p2.isa.get_cinematic_viscosity()}')
