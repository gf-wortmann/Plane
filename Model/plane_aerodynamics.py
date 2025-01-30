import json

from matplotlib import pyplot as plt

from Model import plane_geometry as pg
from Model import ISA as isa
import numpy as np
from Formulae import formulae as ff


class Aerodynamics:
    
    def __init__(self):
        self.empty_mass = None
        self.toff_mass = None
        self.max_duration_power = None
        self.cruise_power = None
        self.max_duration_speed = None
        self.cruise_speed = None
        self.plane_required_power_range = None
        self.plane_ld_ratio_range = None
        self.plane_full_cx_range = None
        self.cxi_range = None
        self.cy_range = None
        self.dynamic_pressure_range = None
        self.mass = None
        self.plane_cx0_range = None
        self.nacelle_cx0_range = None
        self.fuselage_cx0_range = None
        self.fin_cx0_range = None
        self.stab_cx0_range = None
        self.wing_cx0_range = None
        self.general_params = None
        self.nacelle_Re_range = None
        self.fuselage_Re_range = None
        self.fin_Re_range = None
        self.stab_Re_range = None
        self.wing_Re_range = None
        self.formulae = ff.Formulae()
        self.v_range = None
        self.geometry = pg.PlaneGeometry()
        self.isa = isa.ISA()
        
        # setting params
        
        # self.set_general_params()
        # self.set_plane_geometry()
        # self.set_altitude()
        # self.set_v_range()
        # self.set_Re_ranges()
        # self.set_aerodynamics()
    
    # def set_general_params(self, filename):
    def set_general_params(self, filename):  #='tst2_general_ls_params.json'):
        with open(filename, 'r', encoding='utf-8') as file:
            self.general_params = json.load(file)
    
    def set_altitude(self, altitude=0.0):
        self.isa.set_altitude(altitude)
        self.set_aerodynamics()
    
    def set_v_range(self):
        p = self.general_params['speed_range']
        self.v_range = np.arange(p['v_min'], p['v_max'] + p['v_step'], p['v_step'])
    
    def set_plane_geometry(self):
        self.geometry.set_lifting_system_general_geometry(self.general_params)
        self.geometry.set_fuselage_general_geometry(self.general_params)
    
    def calculate_Re_range(self, size):
        return self.formulae.Re(self.v_range, size, self.isa.get_cinematic_viscosity())
    
    def set_wing_Re_range(self):
        self.wing_Re_range = self.calculate_Re_range(self.geometry.get_wing_MAC())
    
    def set_stab_Re_range(self):
        self.stab_Re_range = self.calculate_Re_range(self.geometry.get_stab_MAC())
    
    def set_fin_Re_range(self):
        self.fin_Re_range = self.calculate_Re_range(self.geometry.get_fin_MAC())
    
    def set_fuselage_Re_range(self):
        self.fuselage_Re_range = self.calculate_Re_range(self.geometry.get_fuselage_length())
    
    def set_nacelle_Re_range(self):
        self.nacelle_Re_range = self.calculate_Re_range(self.geometry.get_nacelle_length())
    
    def set_Re_ranges(self):
        self.set_wing_Re_range()
        self.set_stab_Re_range()
        self.set_fin_Re_range()
        self.set_fuselage_Re_range()
        self.set_nacelle_Re_range()
    
    def set_wing_cx0_range(self):
        pp = self.general_params['aerodynamics']
        
        self.wing_cx0_range = (self.formulae.schlichting_mixed_cf(self.wing_Re_range, pp["wing_laminarity"])
                               * pp['wing_cx0_imperfection'] * pp["wing_area_wet_to_plan"])
    
    def set_empennage_cx0_range(self):
        pp = self.general_params['aerodynamics']
        self.stab_cx0_range = (self.formulae.schlichting_mixed_cf(self.stab_Re_range, pp["empennage_laminarity"])
                               * pp['wing_cx0_imperfection'] * pp["wing_area_wet_to_plan"])
        self.fin_cx0_range = (self.formulae.schlichting_mixed_cf(self.fin_Re_range, pp["empennage_laminarity"])
                              * pp['wing_cx0_imperfection'] * pp["wing_area_wet_to_plan"])
    
    def set_bodies_cx0_range(self):
        pp = self.general_params['aerodynamics']
        self.fuselage_cx0_range = (self.formulae.schlichting_mixed_cf(self.fuselage_Re_range, pp["fuselage_laminarity"])
                                   * pp["fuselage_cx0_imperfection"])
        self.nacelle_cx0_range = (self.formulae.schlichting_mixed_cf(self.nacelle_Re_range, pp["fuselage_laminarity"])
                                  * pp["fuselage_cx0_imperfection"])
    
    def set_plane_cx0_range(self):
        # struts
        fuselage_contrib = self.fuselage_cx0_range * self.geometry.get_fuselage_area() / self.geometry.get_wing_area()
        # print(f'fus contrib: {fuselage_contrib}')
        # nacelles_contrib = (self.nacelle_cx0_range * self.geometry.get_nacelle_area()
        #                     * self.geometry.engine_nacelles_count / self.geometry.get_wing_area())
        nacelles_contrib = 0
        stab_contrib = self.stab_cx0_range * self.geometry.get_stab_area() / self.geometry.get_wing_area()
        fin_contrib = (self.fin_cx0_range * self.geometry.get_fin_area() / self.geometry.get_wing_area()
                       * self.geometry.get_fins_count())
        gear_contrib = fuselage_contrib * 0.4
        # struts_contrib = fuselage_contrib * 0.25
        # struts_contrib = (5 * 2 * 0.0043 + 0.0150) / self.geometry.get_wing_area()
        struts_contrib = 0
        # print(f'struts contrib = {struts_contrib}, hmm.. {max(fuselage_contrib) * 0.25}')
        
        self.plane_cx0_range = (self.wing_cx0_range + fuselage_contrib + nacelles_contrib + stab_contrib + fin_contrib
                                + gear_contrib + struts_contrib
                                )
    
    def set_toff_mass(self):
        self.toff_mass = self.general_params['masses']['toff_mass']
        
    def set_empty_mass(self):
        self.empty_mass = self.general_params['masses']['empty_mass']
    
    def set_mass(self, mass):
        self.mass = mass
    
    def set_q_range(self):
        self.dynamic_pressure_range = self.formulae.dynamic_pressure(self.v_range, self.isa.get_density())
        # print(f'in set q range< density = {self.isa.get_density()}')
    
    def set_cy_range(self):
        self.cy_range = self.mass * 9.81 / (self.dynamic_pressure_range * self.geometry.get_wing_area())
    
    def set_cxi_range(self):
        pp = self.general_params['aerodynamics']
        # "wing_span_eff": 0.9,
        # "wing_planform_eff": 0.74
        self.cxi_range = self.formulae.cxi_range(self.cy_range, self.geometry.get_wing_aspect_ratio()
                                                 * pp['wing_span_eff'] * pp['wing_planform_eff'])
    
    def set_plane_full_cx_range(self):
        self.plane_full_cx_range = self.plane_cx0_range + self.cxi_range
    
    def set_plane_ld_ratio_range(self):
        self.plane_ld_ratio_range = self.cy_range / self.plane_full_cx_range
    
    def set_aerodynamics(self):
        self.set_v_range()
        self.set_q_range()
        self.set_Re_ranges()
        self.set_wing_cx0_range()
        self.set_empennage_cx0_range()
        self.set_bodies_cx0_range()
        self.set_plane_cx0_range()
        # self.set_toff_mass()
        # self.set_q_range()
        self.set_cy_range()
        self.set_cxi_range()
        self.set_plane_full_cx_range()
        self.set_plane_ld_ratio_range()
        self.set_plane_required_power()
        self.set_cruise_regime()
        self.set_max_duration_speed()
    
    def set_plane_required_power(self):
        self.plane_required_power_range = (self.plane_full_cx_range * self.dynamic_pressure_range
                                           * self.geometry.get_wing_area() * self.v_range)
    
    def set_cruise_regime(self):
        pt = min(self.plane_required_power_range / self.v_range)
        cruise_speed = 0
        cruise_power = 0
        for v, n in zip(self.v_range, self.plane_required_power_range):
            cruise_speed = v
            cruise_power = n
            if n / v == pt:
                break
        # print(f'vc = {vv}')
        self.cruise_speed = cruise_speed
        self.cruise_power = cruise_power
    
    def set_max_duration_speed(self):
        self.max_duration_power = min(self.plane_required_power_range)
        for v, n in zip(self.v_range, self.plane_required_power_range):
            if n == self.max_duration_power:
                self.max_duration_speed = v
                break
    
    def get_plane_ld_ratio_range(self):
        return self.plane_ld_ratio_range
    
    def get_plane_geometry(self):
        print(f'plane wing span = {self.geometry.lifting_system.get_wing_span()}')
    
    def get_plane_required_power(self):
        return self.plane_required_power_range
    
    def get_plane_required_power_kilowatt(self):
        return self.plane_required_power_range / 1000


if __name__ == '__main__':
    # pa32 = Aerodynamics()
    # pa40 = Aerodynamics()
    hap_fw = Aerodynamics()
    hap_fw.set_general_params("../Projects/HAP-FW/HAP-FW_f1_general_ls_params.json")
    hap_fw.set_plane_geometry()
    hap_fw.set_toff_mass()
    hap_fw.set_empty_mass()
    hap_fw.set_mass(hap_fw.toff_mass)
    hap_fw.set_aerodynamics()
    print(f' mass = {hap_fw.mass}kg')
    hap_fw.set_cruise_regime()
    hap_fw.set_altitude(3000)
    
    # print(f'fus area = {hap_fw.geometry.fuselage_area}, fus len = {hap_fw.geometry.fuselage_length}')
    print(f'cx_0 = {hap_fw.plane_cx0_range}')
    print(f'wing cx_0 = {hap_fw.wing_cx0_range}')
    print(f'L/D = {hap_fw.plane_ld_ratio_range}')
    
    # pa32.set_general_params('p43_32sqm_general_ls_params.json')
    # pa32.set_plane_geometry()
    # pa32.set_aerodynamics()
    # pa32.set_cruise_regime()
    # print(f'pa32 fin area= {pa32.geometry.get_fin_area()}')
    #
    # pa40.set_general_params('p43_40sqm_general_ls_params.json')
    # pa40.set_plane_geometry()
    # pa40.set_aerodynamics()
    # pa40.set_cruise_regime()
    # print(f'pa40 fin area= {pa40.geometry.get_fin_area()}')
    
    # ================ PLOTTING ========================
    # pa32.set_altitude(3000)
    # pa40.set_altitude(3000)
    # #
    # plt.plot(pa32.v_range * 3.6, pa32.get_plane_required_power_kilowatt(),
    #          label=f'Wing area = {pa32.geometry.get_wing_area():.1f}' r'$^2$' f' required power at ' f'{pa32.isa.get_altitude()}m')
    # plt.plot(pa40.v_range * 3.6, pa40.get_plane_required_power_kilowatt(),
    #          label=f'Wing area = {pa40.geometry.get_wing_area():.1f}' r'$^2$' f' required power at ' f'{pa40.isa.get_altitude()}m')
    #
    # # plt.plot(v_range * 3.6, Ka_range)
    # plt.plot(pa32.v_range * 3.6, [490 * 2 * pa32.isa.get_engine_relative_power() * .55 * .736 * 0.8 for x in pa32.v_range], label=f'N available at {pa32.isa.get_altitude()}m')
    
    # pa32.set_altitude(3000)
    # pa40.set_altitude(3000)
    
    # #
    
    # alts = np.arange(0.0, 3001, 3000.0)
    # for alt in alts:
    #     hap_fw.set_altitude(float(alt))
    #     hap_fw.set_mass(hap_fw.toff_mass)
    #     hap_fw.set_aerodynamics()
    #
    #     plt.plot(hap_fw.v_range * 3.6, hap_fw.get_plane_required_power_kilowatt(),
    #              label=f'Mass = {hap_fw.mass:.1f}kg' f' at ' f'{hap_fw.isa.get_altitude()}m')
    #
    #     hap_fw.set_mass(hap_fw.empty_mass)
    #     hap_fw.set_aerodynamics()
    #
    #     plt.plot(hap_fw.v_range * 3.6, hap_fw.get_plane_required_power_kilowatt(),
    #              label=f'Mass = {hap_fw.mass:.1f}kg' f' at ' f'{hap_fw.isa.get_altitude()}m')
    #
    #     N_avail = 100 * hap_fw.isa.get_engine_relative_power() * 1.0 * .736 * 0.8
    #     plt.plot(hap_fw.v_range * 3.6,
    #              [N_avail for x in hap_fw.v_range],
    #              label=f'N cruise available {N_avail:.1f}kW at {hap_fw.isa.get_altitude()}m')
    #
    
    
    plt.plot(hap_fw.v_range * 3.6, hap_fw.get_plane_ld_ratio_range(),
             label=f'Wing area = {hap_fw.geometry.get_wing_area():.1f}' r'$m^2$' f' at ' f'{hap_fw.isa.get_altitude()}m')
    
        #
    # plt.plot(pa40.v_range * 3.6, pa40.get_plane_required_power_kilowatt(),
    #          label=f'Wing area = {pa40.geometry.get_wing_area():.1f}' r'$^2$' f' at ' f'{pa40.isa.get_altitude()}m')
    #
    # plt.plot(pa40.v_range * 3.6, pa40.get_plane_ld_ratio_range(),
    #          label=f'Wing area = {pa40.geometry.get_wing_area():.1f}' r'$^2$' f' at ' f'{pa40.isa.get_altitude()}m')
    
    # plt.plot(pa32.v_range * 3.6, pa32.cy_range,
    #          label=f'Wing area = {pa32.geometry.get_wing_area():.1f}' r'$^2$' f' at ' f'{pa32.isa.get_altitude()}m')
    # plt.plot(pa40.v_range * 3.6, pa40.cy_range,
    #          label=f'Wing area = {pa40.geometry.get_wing_area():.1f}' r'$^2$' f' at ' f'{pa40.isa.get_altitude()}m')
    
    # plt.plot(pa32.v_range * 3.6, pa32.v_range * min(pa32.get_plane_required_power_kilowatt() / pa32.v_range),
    #          label=f'Wing area = {pa32.geometry.get_wing_area():.1f}' r'$^2$' f' cruise power at ' f'{pa32.isa.get_altitude()}m')
    # plt.plot(pa40.v_range * 3.6, pa40.v_range * min(pa40.get_plane_required_power_kilowatt() / pa40.v_range),
    #          label=f'Wing area = {pa40.geometry.get_wing_area():.1f}' r'$^2$' f' cruise power at ' f'{pa40.isa.get_altitude()}m')
    #
    # pa40.set_max_duration_speed()
    # print(f'pa40 min power speed = {pa40.max_duration_speed * 3.6}')
    # pa32.set_max_duration_speed()
    # print(f'pa32 min power speed = {pa32.max_duration_speed * 3.6}')
    # #
    plt.title("Required power vs V")
    
    # plt.title(r"$C_y$ vs V")
    plt.xlabel("V, kmh")
    # plt.ylabel(r"$C_y$")
    # plt.ylabel("L/D ratio")
    plt.ylabel("N, kW")
    plt.legend()
    plt.show()
    
    plt.plot(hap_fw.wing_Re_range, hap_fw.wing_cx0_range,
             label=f'Wing' r'${Cx_0$}' f' at {hap_fw.isa.get_altitude()}m')
    plt.xlabel("Re")
    plt.ylabel("Wing" r'${Cx_0}$')
    plt.show()
    
