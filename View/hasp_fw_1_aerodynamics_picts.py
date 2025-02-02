import sys
# import matplotlib.pyplot as plt
import numpy as np
from matplotlib import patheffects as pe, pyplot as plt
from Model import plane_aerodynamics as pa
from tkinter import filedialog, messagebox
import pandas as pd

project = pa.Aerodynamics()
messagebox.showinfo('Info', 'Select the project *.json file')
ff = filedialog.askopenfilename()
# print(ff)
project.set_general_params(ff)
# project.set_general_params(filedialog.askopenfilename())
project.set_masses()
project.set_plane_geometry()
# project.set_mass(project.toff_mass)
# project.set_altitude(1000)
# project.calculate_aerodynamics()
# project.calculate_cruise_regime()
# print(f'cruise power = {project.cruise_power /736:.2f}hp, cruise speed = {project.cruise_speed * 3.6:.1f}kmh')
#
# project.calculate_cruise_regime_2()
# # print(f'cruise power 2 = {project.cruise_power_2 /736:.2f}hp, cruise speed 2 = {project.cruise_speed_2 * 3.6:.1f}kmh')
#
#
electric_power_consumption = project.general_params["power_plant"]["electric_power_consumption"]  # kWt
prop_effectivity = project.general_params["power_plant"]["prop_effectivity"]


def show_req_power(plane: pa, alt):
    plane.set_altitude(alt)
    
    title = f'{plane.general_params["project"]["project_name"]}, потребная мощность на высоте {plane.isa.get_altitude()}м с учетом потребления СЭС'
    xlabel = f'Скорость, км/ч'
    ylabel = f'Потребная мощность, кВт'
    
    plane.set_mass(plane.toff_mass)
    plane.calculate_aerodynamics()
    # plane.calculate_cruise_regime()
    # plane.calculate_plane_required_power()
    plane.calculate_max_duration_power()
    
    x_range = plane.v_range * 3.6
    y_range_max_mass = plane.get_plane_required_power_kilowatt() + electric_power_consumption
    # y_range_max_mass_minimum = min(y_range_max_mass)
    # print(f' plane mas is: {plane.mass}')
    label_max_mass = f'Потребная мощность при массе {plane.mass:.0f}кг. ' r'$P_{min}$ =' f'{plane.max_duration_power / 1000 + electric_power_consumption:.2f}кВт на {plane.max_duration_speed * 3.6:.1f}км/ч'
    
    plane.set_mass(plane.toff_mass - plane.fuel_mass)  # min mass
    plane.calculate_aerodynamics()
    plane.calculate_max_duration_power()
    # plane.calculate_cruise_regime()
    y_range_min_mass = plane.get_plane_required_power_kilowatt() + electric_power_consumption
    # y_range_min_mass_minimum= min(y_range_min_mass)
    
    # x_rangen = project.v_range * 3.6
    label_min_mass = f'Потребная мощность при массе {plane.mass:.0f}кг. ' r'$P_{min}$ =' f'{plane.max_duration_power / 1000 + electric_power_consumption:.2f}кВт на {plane.max_duration_speed * 3.6:.1f}км/ч'
    
    power_avail_range_nominal = [plane.general_params["power_plant"]["nominal_power_kw"] * prop_effectivity
                                 * plane.isa.get_engine_relative_power() for x in plane.v_range]
    power_avail_range_cruise = [plane.general_params["power_plant"]["cruise_power_kw"] * prop_effectivity
                                * plane.isa.get_engine_relative_power() for x in plane.v_range]
    power_avail_range_cruise_2 = [plane.general_params["power_plant"]["cruise_power_2_kw"] * prop_effectivity
                                  * plane.isa.get_engine_relative_power() for x in plane.v_range]
    
    plots = {label_max_mass: [x_range, y_range_max_mass],
             label_min_mass: [x_range, y_range_min_mass],
             "Располагаемая мощность, номинальный режим": [x_range, power_avail_range_nominal],
             "Располагаемая мощность, максимальный крейсерский режим": [x_range, power_avail_range_cruise],
             "Располагаемая мощность, минимальный крейсерский режим": [x_range, power_avail_range_cruise_2]
             }
    
    limits = {"xmin": min(x_range), "xmax": max(x_range), "ymin": min(y_range_min_mass) / 2,
              "ymax": plane.general_params["power_plant"][
                          "nominal_power_kw"] * plane.isa.get_engine_relative_power() * 1.1}
    graph_plot(plots, limits, title, xlabel, ylabel)


def show_fuel_consumption(plane: pa, alt):
    fuel_mass = plane.fuel_mass * 0.9
    # print(f'fuel_mass is {type(fuel_mass)}')
    fuel_remain = 10.0  # kg
    # print(f'fuel_remain is {type(fuel_remain)}')
    fuel_specific_consumption = plane.general_params["power_plant"]["cruise_fuel_consumption"]  # kg*kW/h
    electric_power_consumption = plane.general_params["power_plant"]["electric_power_consumption"]
    plane.set_altitude(alt)
    plane.set_mass(plane.toff_mass)
    plane.calculate_aerodynamics()
    plane.calculate_max_duration_power()
    current_power = plane.max_duration_power / 1000 + electric_power_consumption
    
    duration = 0
    duration_range = []
    fuel_range = []
    consumption_range = []
    
    title = f'{plane.general_params["project"]["project_name"]}, график расхода топлива на крейсерском режме на высоте {plane.isa.get_altitude()}м с учетом потребления СЭС'
    xlabel = f'Время полета, ч'
    ylabel = f'Остаток топлива, кг'
    
    while fuel_mass >= fuel_remain:
        fuel_hour_consumption = current_power * fuel_specific_consumption
        fuel_mass -= fuel_hour_consumption
        duration += 1
        consumption_range.append(fuel_hour_consumption)
        fuel_range.append(fuel_mass)
        duration_range.append(duration)
        
        plane.set_mass(plane.mass - fuel_hour_consumption)
        plane.calculate_aerodynamics()
        # plane.calculate_max_duration_speed()
        plane.calculate_max_duration_power()
        current_power = plane.max_duration_power / 1000 + electric_power_consumption
        # print(f' fuel amount = {fuel_mass}')
    
    limits = {"xmin": 0, "xmax": max(duration_range), "ymin": 0, "ymax": plane.fuel_mass}
    fuel_volume_label = 'Остаток топлива, кг'
    plots = {
        fuel_volume_label: [duration_range, fuel_range],
    }
    graph_plot(plots, limits, title, xlabel, ylabel)
    
    title = f'{plane.general_params["project"]["project_name"]}, часовой расход топлива на крейсерском режме на высоте {plane.isa.get_altitude()}м с учетом потребления СЭС'
    xlabel = f'Время полета, ч'
    ylabel = f'Расход топлива, кг/ч'
    
    fuel_consumption_label = 'Часовой расход топлива, кг '
    limits_consumption = {"xmin": 0, "xmax": max(duration_range), "ymin": 0, "ymax": max(consumption_range)}
    plots_consumption = {
        fuel_consumption_label: [duration_range, consumption_range]
    }
    graph_plot(plots_consumption, limits_consumption, title, xlabel, ylabel)
    data = [duration_range, consumption_range, fuel_range]
    index = ["Время, ч", "Расход топлива, кг/ч", "Остаток топлива, кг"]
    save_to_excel(data, index, title)


def show_ld_ratio(plane: pa, alt_range: np.arange):
    title = plane.general_params["project"]["project_name"] + f' аэродинамическое качество по высотам'
    # title = f'ВАП-СТ, аэродинамическое качество по высотам'
    xlabel = f'Скорость, км/ч'
    ylabel = r'$K_a$'
    plots_ld_ratio = {}
    limits_ld_ratio = {}
    data = []
    index = ["Скорость, км/ч",]
    
    for alt in alt_range:
        plane.set_altitude(alt)
        plane.set_mass((plane.toff_mass + plane.empty_mass) / 2)
        plane.calculate_aerodynamics()
        ld_ratio_range = plane.get_plane_ld_ratio_range()
        limits_ld_ratio = {"xmin": min(plane.v_range * 3.6), "xmax": max(plane.v_range * 3.6)
            , "ymin": min(ld_ratio_range), "ymax": max(ld_ratio_range)
                           # , "ymin": -5, "ymax": 0.1
                           }
        ld_ratio_label = r'$K_a$' f' на высоте {alt}м'
        plots_ld_ratio[ld_ratio_label] = [plane.v_range * 3.6, ld_ratio_range]
        data.append(ld_ratio_range)
        index.append(f"К_а на высоте {alt}м")
    graph_plot(plots_ld_ratio, limits_ld_ratio, title, xlabel, ylabel)
    data.insert(0, plane.v_range)
    save_to_excel(data, index, title)


def show_max_duration_speed(plane: pa, alt_range: np.arange):
    title = plane.general_params["project"]["project_name"] + f' наивыгоднейшая скорость по высотам'
    # title = f'ВАП-СТ, аэродинамическое качество по высотам'
    xlabel = f'Высота, м'
    ylabel = r'$V_нв$, км/ч'
    plots = {}
    data = [alt_range,]
    index = ["Высота, м",]
    # limits = {}
    # x_range = alt_range
    masses = [plane.empty_mass, plane.toff_mass]
    for mass in masses:
        y_range = []
        for alt in alt_range:
            plane.set_altitude(alt)
            plane.set_mass(mass)
            plane.calculate_aerodynamics()
            plane.calculate_max_duration_speed()
            # plane.calculate_max_duration_power()
            
            y_range.append(plane.max_duration_speed * 3.6)
            # print(plane.max_duration_speed, plane.max_duration_cy)
        label = r'${V_нв}$ км/ч,' f' масса = {plane.mass}'
        plots[label] = [alt_range, y_range]
        data.append(y_range)
        index.append(f'V_нв, км/ч, масса {plane.mass}кг')
        limits = {"xmin": min(alt_range) * 0.5, "xmax": max(alt_range) * 1.1
            , "ymin": min(y_range) * 0.5, "ymax": max(y_range) * 1.1
                  }
    
    graph_plot(plots, limits, title, xlabel, ylabel)
    save_to_excel(data, index, title)


def glider_polar_show(plane: pa):
    title = plane.general_params["project"]["project_name"] + f' зависимость ' r'$V{_y}$ от $V{_x}$'
    xlabel = r'$V_x$, км/ч'
    ylabel = r'$V_y$, м/с'
    plots = {}
    limits = {}
    vy_range = []
    
    plane.set_altitude(1000)
    masses = [plane.toff_mass, plane.empty_mass + 150]  #, plane.empty_mass + 10]
    
    for _mass in masses:
        # print(f'mass being set = {_mass}')
        plane.set_mass(_mass)
        # print(f'plane mass = {plane.mass}, ')
        plane.calculate_aerodynamics()
        # print(f'plane mass = {plane.mass}, ')
        vy_range = -plane.v_range / plane.plane_ld_ratio_range
        label = f'Масса = {_mass}, ' r'$V_{y_{min}}$ = 'f'{max(vy_range):.2f}м/с, ' r'$К_{а_{max}}$ = '  f'{max(plane.plane_ld_ratio_range):.1f}'
        plots[label] = [plane.v_range * 3.6, vy_range]
    
    limits = {"xmin": plane.min_speed * 3.6 * 0.5, "xmax": max(plane.v_range) * 3.6 * 1.1
        , "ymin": min(vy_range) * 1.1, "ymax": max(vy_range) * 0.5
              }
    
    graph_plot(plots, limits, title, xlabel, ylabel)

# def cruise_speeds_vs_alt(plane: pa, alt_range: np.arange):
#     title = plane.general_params["project"]["project_name"] + f' крейсерские скорости по высотам'
#     xlabel = r'$V_x$, км/ч'
#     ylabel = r'$V_y$, м/с'
#     plots = {}
#     limits = {}
#     vy_range = []


def graph_plot(plots, limits, plot_title="title", xlabel="xlabel", ylabel="ylabel"):
    fg, ax = plt.subplots(figsize=(14, 10))
    # print(plots, type(plots))
    # dd = {"a": 11, "b": 22}
    # for k, v in dd:
    #     print(k, v)
    for label, data in plots.items():
        # print(t, type(t))
        # print(d, type(d))
        ax.plot(data[0], data[1], label=label)
    #
    # print(*plots.items())
    ax.set(title=plot_title, xlabel=xlabel, ylabel=ylabel
           , xlim=(limits["xmin"] * 0.5, limits["xmax"] * 1.1)
           # , xticks=np.arange(limits["xmin"] * 5 // 100 * 10, limits["xmax"] * 11 // 10, limits["xmax"] // 100 * 10)
           , ylim=(limits["ymin"], limits["ymax"] * 1.1)
           # , yticks=np.arange(10, limits["ymax"] * 1.2, 2)
           # , yticks=np.arange(limits["ymin"]*5 // 10, limits["ymax"] * 11 // 10, limits["ymax"] // 10 + 1)
           # , xticks=np.arange(limits["xmin"], limits, 20)
           # , yticks=2
           )
    
    ax.grid(True)
    ax.legend()
    # plt.show()


def save_to_excel(data, index, def_name):
    file = filedialog.asksaveasfile(initialfile=def_name+'.xlsx', title="Select Excel file to save"
                                    , filetypes=(("Excel books", "*.xlsx"), ))
    df = pd.DataFrame(data, index=index)
    df.to_excel(file.name, header=False)
    

# show_req_power(project, 1000)
# show_req_power(project, 3000)
# show_req_power(project, 5000)
# show_req_power(project, 7000)
# show_fuel_consumption(project, 0)
# show_fuel_consumption(project, 3000)
# show_fuel_consumption(project, 5000)
# show_fuel_consumption(project, 7000)
# show_ld_ratio(project, np.arange(0, 10001, 1000))
# glider_polar_show(project)
# show_max_duration_speed(project, np.arange(0, 10001, 1000))
# save_to_excel(project)
plt.show()
