import csv
import numpy
import numpy as np
import pandas as pd
from tkinter import filedialog, messagebox
from Model import plane_aerodynamics as pa

alt_range = np.arange(0, 10001, 1000)

project = pa.Aerodynamics()
messagebox.showinfo('Info', 'Select the project *.json file')
ff = filedialog.askopenfilename()

project.set_general_params(ff)
title = f'{project.general_params["project"]["project_name"]} аэродинамические коэффициенты частей планера по высотам'
data_collector = []

for alt in alt_range:
    project.set_masses()
    project.set_plane_geometry()
    project.set_mass(project.toff_mass - project.fuel_mass / 2)
    project.set_altitude(alt)
    project.calculate_aerodynamics()
    
    np.set_printoptions(precision=8)
    
    data_to_out_ = [
        project.v_range,
        project.dynamic_pressure_range,
        project.wing_Re_range,
        project.fuselage_Re_range,
        project.fin_Re_range,
        project.stab_Re_range,
        project.wing_cx0_range,
        project.fuselage_cx0_range,
        project.fin_cx0_range,
        project.stab_cx0_range,
        project.plane_cx0_range,
        project.cy_range,
        project.cxi_range,
        project.plane_full_cx_range,
        project.plane_ld_ratio_range,
        ]
    index = [
        'V, м/с',
        'Q, Н/м^2',
        'Re крыла',
        'Re фюзеляжа',
        'Re ГО',
        'Re ВО',
        'Cx_0 крыла',
        'Cx_0 фюзеляжа',
        'Cx_0 ГО',
        'Cx_0 ВО',
        'Cx_0 БпЛА',
        'Cy',
        'Cx_i',
        'Cx_a',
        'К_а'
        ]
    
    res = pd.DataFrame(data_to_out_, index=index)
    data_collector.append(res)

file = filedialog.asksaveasfile(initialfile=title+'.xlsx', title="Select Excel file to save"
                                    , filetypes=(("Excel books", "*.xlsx"), ))
with pd.ExcelWriter(file.name) as writer:
    for data, alt in zip(data_collector, alt_range):
        data.to_excel(writer, sheet_name=f'Высота {alt}м', header=False)
