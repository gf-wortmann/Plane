import types

from Model import plane_aerodynamics as pa
from tkinter import filedialog

project = pa.Aerodynamics()
file = filedialog.askopenfilename()

project.set_general_params(file)
project.set_masses()
project.set_plane_geometry()
project.set_mass(project.toff_mass)
project.set_altitude(3000)
project.calculate_aerodynamics()
print(f'if max drtn regime is calculated: max drtn speed: {project.max_duration_speed * 3.6:.1f}, max drtn power: {project.max_duration_power / 736:.1f}hp')
# project.calculate_cruise_regime()
# project.calculate_cruise_regime_2()
print(f'cruise power = {project.cruise_power /736:.2f}hp, cruise speed = {project.cruise_speed * 3.6:.1f}kmh')
# print(f'if c_speed_2 is set: {type(project.cruise_speed_2)}, if c_power_2 is set: {type(project.cruise_power_2)}')
print(f'cruise power 2 = {project.cruise_power_2 /736:.2f}hp, cruise speed 2 = {project.cruise_speed_2 * 3.6:.1f}kmh')

