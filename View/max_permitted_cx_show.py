import sys

import matplotlib.pyplot as plt
import numpy as np
from matplotlib import patheffects as pe

sys.path.append('../Model')

from Model.select_params_for_cruise import EqPlate
from Model.input_parameters import plane_params, standard_atmosphere_density, constants
from Model import ISA as isa

e = EqPlate(plane_params, standard_atmosphere_density, constants)
work_altitude = 3000.0
isa = isa.ISA()
isa.set_altitude(work_altitude)

power_regime = 'power_cruise_regime_55'
calc_power = e.plane_params['power_toff_engine_type_1'] * e.plane_params[power_regime] * isa.get_engine_relative_power()
print(f'relative power turbo = {isa.get_engine_relative_power()}, regime is {e.plane_params[power_regime]}, calc power = {calc_power}')

x = e.speed_SI_range * 3.6

# drawing
fg, ax = plt.subplots(figsize=(14, 10))
ax.set_title(r"Пчела" f', 2*{e.plane_params["power_toff_engine_type_1"]} л.с.' r' Chevrolet LT4 tyrbo, предельные C$_{x0 min}$' f' по крейсерской скорости\n'
             r"$G_{cruise}$" f" = {e.plane_params['mass_cruise_calc']} кг, N = {e.plane_params[power_regime]}"
             r'N$_{ном.длит.}$'
             f" ({calc_power * 2:.0f} л.с. суммарно)"
             # f" ({e.plane_params['power_nominal_3km_eng_type_1'] * 2 * e.plane_params[power_regime]:.0f} л.с. суммарно)"
             f', Высота = {work_altitude} м.'
             )
ax.set(xlabel='Скорость, км/ч', ylabel=r'Предельные $C_{x min}$'
       , xlim=(min(x), max(x)), xticks=np.arange(min(x), max(x) + 20, 20.0)
       , ylim=(0, 0.05), yticks=np.arange(0, 0.05, 0.005)
       )

ax.grid(True)

colors = ['r', 'g', 'b', 'c', 'y', 'k']
line_fonts = ['-', '--', '-.', '.']

cont = 'cont'
ci = 0
for area_loading in e.wgt_to_area_SI_range:
    lfi = 0
    ci += 1
    for aspect_ratio in e.aspect_ratio_range:
        y = e.cx_max_permitted_vs_speed(area_loading, work_altitude, power_regime) - e.cx_i(work_altitude, area_loading,
                                                                                            aspect_ratio)
        ax.plot(x, y, colors[ci] + line_fonts[lfi],
                label=(f'n') + '\u0305' + f'= {area_loading / 9.81:.0f} $кгс/м^2$'
                                          f', \u03BB = {aspect_ratio}'
                # , path_effects=[pe.withTickedStroke(spacing=5, length=1)]
                )
        lfi += 1
    # ax.plot(x, [0.045 for x in x], 'k-.', path_effects=[pe.withTickedStroke(spacing=5, length=1)])
    # ax.plot(x, [0.035 for x in x], 'k--', path_effects=[pe.withTickedStroke(spacing=5, length=1)])
    ax.plot(x, [0.025 for x in x], 'r--', path_effects=[pe.withTickedStroke(spacing=5, length=1)])
    ax.plot(x, [0.02 for x in x], 'g--', path_effects=[pe.withTickedStroke(spacing=5, length=1)])
    
    # ax.annotate('Ан-14', xy=(340, 0.045), xytext=(340, 0.042), arrowprops=dict(arrowstyle="->"))
    # ax.annotate('Пчела с неубирающимся шасси', xy=(360, 0.035), xytext=(360, 0.04), arrowprops=dict(arrowstyle="->"))
    ax.annotate('"Пчела" - средний $Cx_0$', xy=(310, 0.025), xytext=(310, 0.027), arrowprops=dict(arrowstyle="->"))
    ax.annotate('"Пчела" - минимальный расчетный $Cx_0$', xy=(310, 0.02), xytext=(310, 0.022),
                arrowprops=dict(arrowstyle="->"))
ax.legend()
plt.show()
