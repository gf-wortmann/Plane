# -*- coding: utf-8 -*-
"""
Created on Wed Oct 23 13:29:41 2024

@author: fyodorovgv
"""
import numpy as np


class Formulae:
    def __init__(self):
        pass
    
    def span_by_area__aspect_ratio(self, area, aspect_ratio):
        return np.sqrt(area * aspect_ratio)
    
    def MGC_by_area__aspect_ratio(self, area, aspect_ratio):
        return np.sqrt(area / aspect_ratio)
    
    def cxi_range(self, cy_range, aspect_ratio):
        return cy_range ** 2 / np.pi / aspect_ratio
        
    def cxi(self, cy, aspect_ratio):
        return cy ** 2 / np.pi / aspect_ratio
        # return cx_range
    
    def schlichting_laminar_cf(self, Re):
        return 1.3 / np.sqrt(Re)
    
    def schlichting_turbulent_cf(self, Re):
        return 0.455 / np.log10(Re) ** 2.58

    def schlichting_mixed_cf(self, Re, mix_ratio):
        return self.schlichting_laminar_cf(Re) * mix_ratio + self.schlichting_turbulent_cf(Re) * (1 - mix_ratio)
    
    def dynamic_pressure(self, v, density):
        return density * v ** 2 / 2
    
    def Re(self, v, size, nu):
        return v * size / nu
    
    
    
    
    
    
    
    
if __name__ == '__main__':
    f = Formulae()
    print(f'cf = {f.schlichting_laminar_cf(3.44e6)}')
    print(f'cf = {f.schlichting_laminar_cf(3437955.928)}')
    print(f'cf = {f.schlichting_turbulent_cf(3437955.928)}')
    print(f'cf = {f.schlichting_mixed_cf(3437955.928, 0.2)}')
    print(f'cx = {f.schlichting_mixed_cf(3437955.928, 0.2) * 1.7 * 2.05}')
    
    # print()
