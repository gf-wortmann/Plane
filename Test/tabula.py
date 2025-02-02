import csv
import numpy
import numpy as np
import pandas as pd
from tkinter import filedialog, messagebox
from Model import plane_aerodynamics as pa

alt_range = np.arange(0, 10001, 1000)
row_names = ["V, m/s", "Cy_a", "Cx_0", "Cxi", "Cx_a", "LD ratio", "N_required, W"]

project = pa.Aerodynamics()
messagebox.showinfo('Info', 'Select the project *.json file')
ff = filedialog.askopenfilename()

project.set_general_params(ff)
title = f'{project.general_params["project"]["project_name"]} аэродинамические коэффициенты по высотам'
data_collector = []

for alt in alt_range:
    project.set_masses()
    project.set_plane_geometry()
    project.set_mass(project.toff_mass - project.fuel_mass / 2)
    project.set_altitude(alt)
    project.calculate_aerodynamics()
    
    np.set_printoptions(precision=8)
    data_to_out = [project.v_range, project.cy_range, project.plane_cx0_range, project.cxi_range, project.plane_full_cx_range, project.plane_ld_ratio_range, project.plane_required_power_range]

    res = pd.DataFrame(data_to_out, index=row_names)
    data_collector.append(res)
    # print(res)

# np.set_printoptions(precision=8)
# res.to_csv('Project data.csv', sep='\t', index=True, header=False, float_format="%.8f")

file = filedialog.asksaveasfile(initialfile=title+'.xlsx', title="Select Excel file to save"
                                    , filetypes=(("Excel books", "*.xlsx"), ))
with pd.ExcelWriter(file.name) as writer:
    for data, alt in zip(data_collector, alt_range):
        data.to_excel(writer, sheet_name=f'Высота {alt}м', header=False)
