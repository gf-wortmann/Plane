import numpy as np
from Model import plane_aerodynamics as pa
from matplotlib import pyplot as plt
from tkinter import filedialog, messagebox
import pandas as pd


class Reports:
    
    def __init__(self):
        self.plane = pa.Aerodynamics()
        
        
        
        
    def set_general_params(self, filename):  #='tst2_general_ls_params.json'):
        self.plane.set_general_params(filename)
    
    def set_plane(self):
        p = self.plane
        p.set_masses()
        p.set_plane_geometry()
        # p.set_altitude(0)
        p.calculate_aerodynamics()
    
    def calculate_v_range(self):
        v_min = self.plane.min_speed
        
        
if __name__ == "__main__":
    rep = Reports()
    rep.set_general_params("C:/Users/79267/Urban_Univercity/Python_Developer/Plane_Project/Projects/HAP-FW/HAP-FW_f1_general_ls_params.json")
    rep.set_plane()
    print(rep.plane.toff_mass)
    # print(rep.plane.plane_required_power_range)
    power = rep.plane.general_params["power_plant"]["nominal_power_kw"] * 1000
    ext = power - rep.plane.plane_required_power_range
    # print(f'ext = {ext}')
    max_ext = max(ext)
    alt_range = np.arange(0, 4001, 10)
    ext_range = []
    for alt in alt_range:
        rep.plane.set_altitude(alt)
        # alt_power = power * rep.plane.isa.get_engine_relative_power_no_corrector()
        alt_power = power * rep.plane.isa.get_engine_relative_power()
        alt_max_ext = max(alt_power - rep.plane.plane_required_power_range)
        v_at_vy_max = 0
        for v, n in zip(rep.plane.v_range, rep.plane.plane_required_power_range):
            if alt_power - n == alt_max_ext:
                v_at_vy_max = v
                break
        
        real_ext = alt_max_ext * 0.6 * 0.9 - 2000
        ext_range.append(real_ext)
        # print(f'max ext = {real_ext} at V = {v_at_vy_max} at H = {alt}')
        # print(f'Vy max = {real_ext / rep.plane.mass / 9.81}')

    vy_range = [x / rep.plane.mass / 9.81 for x in ext_range]
    time_range = [10 / x / 60 for x in vy_range]
    time_acc = [time_range[0]]
    
    for i in range(1, len(time_range)):
        time_acc.append(time_acc[i-1] + time_range[i])
        
    time = np.sum(time_range)
    print(f'time summary = {time}')
    # print(f'ext_range = {ext_range}')
    
    fg, ax = plt.subplots(figsize=(14, 10))
    ax.plot(time_acc, alt_range, label="time to climb on, min")
    #
    # print(*plots.items())

    ax.grid(True)
    ax.legend()
    plt.show()