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
#++++++++++++++++++++++++++++++++
# project.calculate_aerodynamics()
# cx_ = project.plane_full_cx_range
# print(f'plane Cx range: {cx_}')
#+++++++++++++++++++++++++++++++
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
    
    title = f'{plane.general_params["project"]["project_name"]},\nпотребная мощность на высоте {plane.isa.get_altitude()}м с учетом потребления СЭС {electric_power_consumption}кВт'
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
    label_max_mass = f'Минимальная потребная мощность при массе {plane.mass:.2f}кг. ' r'$P_{min}$ =' f'{plane.max_duration_power / 1000 + electric_power_consumption:.2f}кВт на {plane.max_duration_speed * 3.6:.1f}км/ч'
    
    plane.set_mass(plane.toff_mass - plane.fuel_mass / 2)  # min mass
    # plane.set_mass(plane.toff_mass - plane.fuel_mass)  # min mass
    plane.calculate_aerodynamics()
    plane.calculate_max_duration_power()
    # plane.calculate_cruise_regime()
    y_range_min_mass = plane.get_plane_required_power_kilowatt() + electric_power_consumption
    print(f'min mass y-range calculated')
    # y_range_min_mass_minimum= min(y_range_min_mass)
    # min_speed_range = [plane.min_speed * 3.6 for x in y_range_min_mass]
    # nominal_speed_range = [plane.nominal_speed * 3.6 for x in y_range_min_mass]
    # x_rangen = project.v_range * 3.6
    label_min_mass = f'Потребная мощность при массе {plane.mass:.2f}кг. ' r'$P_{min}$ =' f'{plane.max_duration_power / 1000 + electric_power_consumption:.2f}кВт на {plane.max_duration_speed * 3.6:.1f}км/ч'
    # label_min_mass = f'Минимальная потребная мощность при удлинении 10 = ' f'{plane.max_duration_power / 1000 + electric_power_consumption:.2f}кВт на {plane.max_duration_speed * 3.6:.1f}км/ч'

#  comparing configuration
#     plane.set_mass(plane.toff_mass - plane.fuel_mass)  # min mass
#     plane.geometry.lifting_system.set_wing_aspect_ratio(7.0)
#     plane.calculate_aerodynamics()
#     plane.calculate_max_duration_power()
    # plane.calculate_cruise_regime()
    # y_range_min_mass_2 = plane.get_plane_required_power_kilowatt() + electric_power_consumption
    # y_range_min_mass_minimum= min(y_range_min_mass)
    # min_speed_range_2 = [plane.min_speed * 3.6 for x in y_range_min_mass_2]
    # x_rangen = project.v_range * 3.6
    # label_min_mass_2 = f'Минимальная потребная мощность при удлинении 7 = ' f'{plane.max_duration_power / 1000 + electric_power_consumption:.2f}кВт на {plane.max_duration_speed * 3.6:.1f}км/ч'
    # label_min_mass_2 = f'lamda7 Минимальная потребная мощность при массе {plane.mass:.0f}кг. ' r'$P_{min}$ =' f'{plane.max_duration_power / 1000 + electric_power_consumption:.2f}кВт на {plane.max_duration_speed * 3.6:.1f}км/ч'
#  /comparing configuration



    # low alt engine, no alt. corrector
    # power_avail_range_nominal = [plane.general_params["power_plant"]["nominal_power_kw"] * prop_effectivity
    #                              * plane.isa.get_engine_relative_power_no_corrector() for x in plane.v_range]
    # power_avail_range_cruise = [plane.general_params["power_plant"]["cruise_power_kw"] * prop_effectivity
    #                             * plane.isa.get_engine_relative_power_no_corrector() for x in plane.v_range]
    # power_avail_range_cruise_2 = [plane.general_params["power_plant"]["cruise_power_2_kw"] * prop_effectivity
    #                               * plane.isa.get_engine_relative_power_no_corrector() for x in plane.v_range]
    # /low alt engine, no alt. corrector
    #
    # low alt engine, alt. corrector installed
    power_avail_range_nominal = [plane.general_params["power_plant"]["nominal_power_kw"] * prop_effectivity
                                 * plane.engine_isa.get_engine_relative_power() for x in plane.v_range]
    power_avail_range_toff = [plane.general_params["power_plant"]["toff_power_kw"] * prop_effectivity
                                 * plane.engine_isa.get_engine_relative_power() for x in plane.v_range]
    # # print(f'toff-json: {plane.general_params["power_plant"]["toff_power_kw"]}, avail nom: {power_avail_range_nominal}')
    power_avail_range_cruise = [plane.general_params["power_plant"]["cruise_power_kw"] * prop_effectivity
                                * plane.engine_isa.get_engine_relative_power() for x in plane.v_range]
    power_avail_range_cruise_2 = [plane.general_params["power_plant"]["cruise_power_2_kw"] * prop_effectivity
                                  * plane.engine_isa.get_engine_relative_power() for x in plane.v_range]
    # /low alt engine, alt. corrector installed
    
    # # turbo diesel engine  upto 3km
    # power_avail_range_nominal = [plane.general_params["power_plant"]["nominal_power_kw"] * prop_effectivity
    #                              for x in plane.v_range]
    # power_avail_range_cruise = [plane.general_params["power_plant"]["cruise_power_kw"] * prop_effectivity
    #                             for x in plane.v_range]
    # power_avail_range_cruise_2 = [plane.general_params["power_plant"]["cruise_power_2_kw"] * prop_effectivity
    #                               for x in plane.v_range]
    # #  /turbo diesel engine upto 3km

    # # electric engine
    # power_avail_range_nominal = [plane.general_params["power_plant"]["nominal_power_kw"] * prop_effectivity
    #                              for x in plane.v_range]
    # power_avail_range_cruise = [plane.general_params["power_plant"]["cruise_power_kw"] * prop_effectivity
    #                             for x in plane.v_range]
    # power_avail_range_cruise_2 = [plane.general_params["power_plant"]["cruise_power_2_kw"] * prop_effectivity
    #                               for x in plane.v_range]
    plots = {
            # label_max_mass: [x_range, y_range_max_mass],
            # label_max_mass: [x_range, y_range_min_mass],
            label_min_mass: [x_range, y_range_min_mass],
             # label_min_mass_2: [x_range, y_range_min_mass_2],
             f"Располагаемая мощность, взлётный режим {max(power_avail_range_toff):.2f} кВт": [
                 x_range,power_avail_range_toff],
             f"Располагаемая мощность, номинальный режим {max(power_avail_range_nominal):.2f} кВт": [
                 x_range, power_avail_range_nominal],
             f"Располагаемая мощность, максимальный крейсерский режим {max(power_avail_range_cruise):.2f} кВт": [
                 x_range, power_avail_range_cruise],
             f"Располагаемая мощность, минимальный крейсерский режим {max(power_avail_range_cruise_2):.2f} кВт": [
                 x_range, power_avail_range_cruise_2],
             # f"min speed = {plane.min_speed * 3.6:.1f} км/ч": [min_speed_range, y_range_min_mass],
             # f"speed at nominal power = {plane.nominal_speed * 3.6:.1f} км/ч": [nominal_speed_range, y_range_min_mass]
             }
    # #  /turbo diesel engine upto 3km


    limits = {"xmin": min(x_range), "xmax": max(x_range), "ymin": min(y_range_min_mass) / 12,
              "ymax": plane.general_params["power_plant"]["toff_power_kw"] * prop_effectivity * 1.1}
                          # "nominal_power_kw"] * plane.isa.get_engine_relative_power() * 1.1}
                          # "toff_power_kw"] * 0.75 * 1.1}
    graph_plot(plots, limits, title, xlabel, ylabel)


def show_fuel_consumption(plane: pa, alt):
    fuel_mass = plane.fuel_mass * 0.95
    # fuel_mass = plane.fuel_mass * 0.9
    # print(f'fuel_mass is {type(fuel_mass)}')
    # fuel_spare = 60.0  # kg
    fuel_spare = 0.0  # kg
    # print(f'fuel_spare is {type(fuel_spare)}')
    fuel_specific_consumption = plane.general_params["power_plant"]["cruise_fuel_consumption"]  # kg*kW/h
    local_electric_power_consumption = plane.general_params["power_plant"]["electric_power_consumption"]
    plane.set_altitude(alt)
    plane.set_mass(plane.toff_mass)
    plane.geometry.set_lifting_system_general_geometry(plane.general_params)
    plane.calculate_aerodynamics()
    
    # plane.calculate_cruise_regime_1()
    # current_power = ((plane.cruise_power_1 / 1000 + local_electric_power_consumption)
    #                  / plane.general_params["power_plant"]["prop_effectivity"])
    # current_speed = plane.cruise_speed_1
    
    plane.calculate_cruise_regime()
    current_power = ((plane.cruise_power / 1000 + local_electric_power_consumption)
                     / plane.general_params["power_plant"]["prop_effectivity"])
    current_speed = plane.cruise_speed

    plane.calculate_cruise_regime_2()
    current_power = ((plane.cruise_power_2 / 1000 + local_electric_power_consumption)
                     / plane.general_params["power_plant"]["prop_effectivity"])
    current_speed = plane.cruise_speed_2
    
    # # plane.calculate_max_duration_power()
    # current_power = plane.max_duration_power / 1000 + local_electric_power_consumption
    
    minute_duration = 0
    duration_range = []
    fuel_range = []
    hour_consumption_range = []
    distance_consumption_range = []
    distance_range = []
    distance = 0
    
    title = (f'{plane.general_params["project"]["project_name"]}, график расхода топлива на 2-м крейсерском режиме '
             f'{current_power:.0f}кВт на высоте {plane.isa.get_altitude()}м \n и скорости {current_speed * 3.6:.0f}км/ч, '
             f'с учетом потребления СЭС {local_electric_power_consumption}kW')
    # xlabel = f'Время полета, ч'
    xlabel = f'Расстояние, км'
    ylabel = f'Остаток топлива, кг'
    
    while fuel_mass >= fuel_spare:
        fuel_minute_consumption = current_power * fuel_specific_consumption / 60
        fuel_distance_consumption = fuel_minute_consumption / (current_speed * 3.6) * 60
        fuel_mass -= fuel_minute_consumption
        minute_duration += 1
        distance += current_speed * 3.6 / 60
        hour_consumption_range.append(fuel_minute_consumption * 60)
        distance_consumption_range.append(fuel_distance_consumption)
        fuel_range.append(fuel_mass)
        duration_range.append(minute_duration / 60)
        distance_range.append(distance)
        
        plane.set_mass(plane.mass - fuel_minute_consumption)
        plane.calculate_aerodynamics()
        # plane.calculate_max_duration_speed()
        # plane.calculate_max_duration_power()
        # current_power = plane.max_duration_power / 1000 + local_electric_power_consumption
        
        # current_power = ((plane.cruise_power / 1000 + local_electric_power_consumption)
        #                  / plane.general_params["power_plant"]["prop_effectivity"])
        # current_speed = plane.cruise_speed
        # plane.calculate_cruise_regime_1()
        # current_power = ((plane.cruise_power_1 / 1000 + local_electric_power_consumption)
        #                  / plane.general_params["power_plant"]["prop_effectivity"])
        # current_speed = plane.cruise_speed_1
        # plane.calculate_cruise_regime_2()
        # current_power = ((plane.cruise_power_2 / 1000 + local_electric_power_consumption)
        #                  / plane.general_params["power_plant"]["prop_effectivity"])
        # current_speed = plane.cruise_speed_2
        # print(f' current speed = {current_speed * 3.6:.0f}, current power = {current_power:.0f}')
        
        # print(f' fuel amount = {fuel_mass}')
    
    limits = {"xmin": 0, "xmax": max(distance_range), "ymin": 0, "ymax": plane.fuel_mass}
    fuel_volume_label = 'Остаток топлива, кг'
    plots = {
        fuel_volume_label: [distance_range, fuel_range],
    }
    # graph_plot(plots, limits, title, xlabel, ylabel)
    
    # title = f'{plane.general_params["project"]["project_name"]}, часовой расход топлива на крейсерском режиме на высоте {plane.isa.get_altitude()}м с учетом потребления СЭС {local_electric_power_consumption}kW'
    # xlabel = f'Время полета, ч'
    # ylabel = f'Расход топлива, кг/ч'
    #
    # fuel_consumption_label = 'Часовой расход топлива, кг '
    # limits_consumption = {"xmin": 0, "xmax": max(duration_range), "ymin": 0, "ymax": max(hour_consumption_range)}
    # plots_consumption = {
    #     fuel_consumption_label: [duration_range, hour_consumption_range]
    # }
    # graph_plot(plots_consumption, limits_consumption, title, xlabel, ylabel)
    
    # title = (
    #     f'{plane.general_params["project"]["project_name"]}, километровый расход топлива на максимальном крейсерском режиме'
    #     # title = (f'{plane.general_params["project"]["project_name"]}, километровый расход топлива на минимальном крейсерском режиме'
    #     # title = (f'{plane.general_params["project"]["project_name"]}, километровый расход топлива на 2-м крейсерском режиме'
    #     f' на высоте {plane.isa.get_altitude()}м\nи скорости {current_speed * 3.6:.0f} км/ч '
    #     f'с учетом потребления СЭС {local_electric_power_consumption}kW')
    
    xlabel = f'Расстояние, км'
    # xlabel = f'Время полета, ч'
    ylabel = f'Расход топлива, кг/км'
    
    fuel_consumption_label = 'Километровый расход топлива, кг '
    limits_consumption = {"xmin": 0, "xmax": max(distance_range), "ymin": 0, "ymax": max(distance_consumption_range)}
    plots_consumption = {
        fuel_consumption_label: [distance_range, distance_consumption_range]
    }
    graph_plot(plots_consumption, limits_consumption, title, xlabel, ylabel)
    
    data = [duration_range, hour_consumption_range, fuel_range]
    index = ["Время, ч", "Расход топлива, кг/ч", "Остаток топлива, кг"]
    # save_to_excel(data, index, title)


def show_ld_ratio(plane: pa, alt_range: np.arange):
    title = plane.general_params["project"]["project_name"] + '\n' + f'аэродинамическое качество от скорости'
    # title = f'ВАП-СТ, аэродинамическое качество по высотам'
    xlabel = f'Скорость, км/ч'
    ylabel = r'$K_a$'
    plots_ld_ratio = {}
    limits_ld_ratio = {}
    data = []
    index = ["Скорость, км/ч", ]
    
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
    # save_to_excel(data, index, title)


def show_max_duration_speed(plane: pa, alt_range: np.arange):
    title = plane.general_params["project"]["project_name"] + f'\nнаивыгоднейшая скорость по высотам'
    # title = f'ВАП-СТ, аэродинамическое качество по высотам'
    xlabel = f'Высота, м'
    ylabel = r'$V_{нв}$, км/ч'
    plots = {}
    data = [alt_range, ]
    index = ["Высота, м", ]
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
            plane.calculate_max_duration_cy()
            # plane.calculate_max_duration_power()
            
            y_range.append(plane.max_duration_speed * 3.6)
            # print(plane.max_duration_speed, plane.max_duration_cy)
        label = r'$V_{нв}$ км/ч,' f' масса = {plane.mass}, ' r'$C_{ya}$ = ' f'{plane.max_duration_cy:.2f}'
        plots[label] = [alt_range, y_range]
        data.append(y_range)
        index.append(f'V_нв, км/ч, масса {plane.mass}кг')
        limits = {"xmin": min(alt_range) * 0.5, "xmax": max(alt_range) * 1.1
            , "ymin": min(y_range) * 0.5, "ymax": max(y_range) * 1.1
                  }
    
    graph_plot(plots, limits, title, xlabel, ylabel)
    # save_to_excel(data, index, title)


def glider_polar_show(plane: pa, alt):
    title = plane.general_params["project"]["project_name"] + '\n' f'зависимость ' r'$V{_y}$ от $V{_x}$' f'на высоте {alt}м.'
    xlabel = r'$V_x$, км/ч'
    ylabel = r'$V_y$, м/с'
    plots = {}
    limits = {}
    vy_range = []
    
    plane.set_altitude(alt)
    masses = [plane.toff_mass, plane.toff_mass - plane.fuel_mass]  #, plane.empty_mass + 10]
    plane.geometry.set_lifting_system_general_geometry(plane.general_params)
    
    for _mass in masses:
        # print(f'mass being set = {_mass}')
        plane.set_mass(_mass)
        # print(f'plane mass = {plane.mass}, ')
        plane.calculate_aerodynamics()
        # print(f'plane mass = {plane.mass}, ')
        vy_range = -plane.v_range / plane.plane_ld_ratio_range
        label = f'Масса = {_mass}, ' 'm' '\u0305' f' = {_mass / plane.geometry.get_wing_area():.2f}' r'$кг/м^2$, ' r'$V_{y_{min}}$ = 'f'{max(vy_range):.2f}м/с, ' r'$К_{а_{max}}$ = '  f'{max(plane.plane_ld_ratio_range):.1f}'
        plots[label] = [plane.v_range * 3.6, vy_range]
    
    limits = {"xmin": plane.min_speed * 3.6 * 0.5, "xmax": max(plane.v_range) * 3.6 * 1.1
        , "ymin": min(vy_range) * 1.1, "ymax": max(vy_range) * 0.5
              }
    
    graph_plot(plots, limits, title, xlabel, ylabel)
    print(f'fin area = {plane.geometry.get_fin_area()}')
    print(f'stab area = {plane.geometry.get_stab_area()}')


def cx0_vs_v_aggr_show(plane: pa, alt):
    title = plane.general_params["project"]["project_name"] + '\n' f'Сводка коэффициентов сопротивлений при нулевой подъёмной силе по агрегатам на высоте {alt:.0f}м.'
    x_label = r'$V_x$, км/ч'
    y_label = r'$C_{x}$' ## scalpel_RR
    plots = {}

    plane.set_altitude(alt)
    plane.set_masses()
    plane.geometry.set_lifting_system_general_geometry(plane.general_params)

    plots = cx0_vs_v_aggr(plane)

    limits = {
        "xmin": 0, "xmax": max(plane.v_range) * 3.6 * 1.1,
        "ymin": 0, "ymax": max(plane.plane_cx0_range) * 1.1
              }

    graph_plot(plots, limits, title, x_label, y_label)

def cx_vs_v_types_show(plane: pa, alt):
    title = plane.general_params["project"]["project_name"] + '\n' f'Сводка коэффициентов сопротивлений по типам на высоте {alt:.0f}м.'
    x_label = r'$V_x$, км/ч'
    y_label = r'$C_{x}$' ## scalpel_RR

    plane.set_altitude(alt)
    plane.set_masses()
    plane.geometry.set_lifting_system_general_geometry(plane.general_params)

    plots = cx_vs_v_types(plane)

    limits = {
        "xmin": 0, "xmax": max(plane.v_range) * 3.6 * 1.1,
        "ymin": 0, "ymax": max(plane.plane_full_cx_range) * 1.1
              }

    graph_plot(plots, limits, title, x_label, y_label)

def cx_vs_v_types(plane: pa):
    plots = {}

    cx0_range = plane.plane_cx0_range
    cx0_label = r'$C_{x0}$'
    cxi_range = plane.cxi_range
    cxi_label = r'$C_{xi}$'
    full_cx_range = plane.plane_full_cx_range
    full_cx_label = r'$C_{xa}$'
    V_max_duration = plane.max_duration_speed * 3.6
    #   !scalpel-RR

    plots[cx0_label] = [plane.v_range * 3.6, cx0_range]
    plots[cxi_label] = [plane.v_range * 3.6, cxi_range]
    plots[full_cx_label] = [plane.v_range * 3.6, full_cx_range]
    plots[r'$V_{нв}$'] = [np.linspace(V_max_duration, V_max_duration, 101),
                          np.linspace(0, max(full_cx_range), 101)]

    return plots

def cx0_vs_v_aggr(plane: pa):
    plots = {}

    wing_cx0_range = plane.wing_cx0_range
    fus_cx0_range = plane.fuselage_cx0_range * plane.geometry.get_fuselage_area() / plane.geometry.get_wing_area()
    nacelle_cx0_range = plane.nacelle_cx0_range * plane.geometry.get_nacelle_area() / plane.geometry.get_wing_area()
    h_stab_cx0_range = plane.stab_cx0_range * plane.geometry.get_stab_area() / plane.geometry.get_wing_area()
    v_stab_cx0_range = plane.fin_cx0_range * plane.geometry.get_fin_area() / plane.geometry.get_wing_area()
    plane_cx0_range = plane.plane_cx0_range

    plots['Крыло'] = [plane.v_range * 3.6, wing_cx0_range]
    plots['Фюзеляж'] = [plane.v_range * 3.6, fus_cx0_range]
    plots['ГО'] = [plane.v_range * 3.6, h_stab_cx0_range]
    plots['ВО'] = [plane.v_range * 3.6, v_stab_cx0_range]
    # plots['Обзорная видеокамера'] = [plane.v_range * 3.6, nacelle_cx0_range]
    plots[r'$C_{x0}$'] = [plane.v_range * 3.6, plane_cx0_range]

    return plots


def cruise_speeds_vs_alt(plane: pa, alt_range: np.arange):
    # title = plane.general_params["project"]["project_name"] + f' крейсерские режимы по высотам'
    title = plane.general_params["project"]["project_name"] + f'  Диапазон скоростей и высот горизонтального полета'
    ylabel = 'Высота, м'
    xlabel = r'$V_{cruise}$, км/ч'
    xlabel_2 = r'$C_{y\ cruise}$, км/ч'
    xlabel_twin = r'$N_{cruise}$, кВт'
    plots = {}
    plots_2 = {}
    plots_twin = {}
    limits = {}
    v_min_range = []
    v_cruise_range = []
    v_cruise1_range = []
    v_cruise2_range = []
    v_nominal_range = []
    # p_vmin_range = []
    p_cruise_range = []
    p_cruise1_range = []
    p_cruise2_range = []
    p_nominal_range = []
    
    cy_cruise_range = []
    cy_cruise_1_range = []
    cy_cruise_2_range = []
    
    plot_data_2 = []
    plot_data_cy_2 = []
    plot_data_alt_2 = []
    
    for alt in alt_range:
        plane.set_altitude(alt)
        plane.set_mass(plane.toff_mass - plane.fuel_mass / 2)
        plane.calculate_aerodynamics()
        v_min_range.append(plane.min_speed * 3.6)
        v_cruise_range.append(plane.cruise_speed * 3.6)
        v_cruise1_range.append(plane.cruise_speed_1 * 3.6)
        v_cruise2_range.append(plane.cruise_speed_2 * 3.6)
        cy_cruise_range.append(plane.cruise_cy)
        cy_cruise_1_range.append(plane.cruise_cy_1)
        cy_cruise_2_range.append(plane.cruise_cy_2)
        v_nominal_range.append(plane.nominal_speed * 3.6)
        p_cruise_range.append(plane.cruise_power / 1000)
        p_cruise1_range.append(plane.cruise_power_1 / 1000)
        p_cruise2_range.append(plane.cruise_power_2 / 1000)
        p_nominal_range.append(plane.nominal_power / 1000)
        
        # for alt_2 in alt_range:
        #     for cy_2, cy in zip(cy_cruise_2_range, cy_cruise_range):
        #         if cy > cy_2:
        #             plot_data_cy_2.append(cy_2)
        #             plot_data_alt_2.append(alt_2)
        #             print(f'c_y_2: {cy_2}, c_y: {cy}, alt: {alt_2}')
        #         else:
        #             break
        
        
        # print(f'plot_data_2 {plot_data_2}')
        
        # p_vmin_range.append(plane.)
    
    # print(*zip(cy_cruise_2_range, cy_cruise_range, alt_range), '\n')
    for cy2, cy, alt2 in zip(cy_cruise_2_range, cy_cruise_range, alt_range):
        # print(f'cy2 = {cy2}, cy = {cy}, alt = {alt2}')
        if cy2 <= cy:
            plot_data_cy_2.append(cy2)
            plot_data_alt_2.append(alt2)
    
    plot_data_2 = [plot_data_cy_2, plot_data_alt_2]
    # print(f'plot data 2: ', *plot_data_2)
    
    # plots[r'$V_{max\ range}$'] = [v_cruise_range, alt_range]
    
    plots[r'$V_{max\ range}$'] = [v_cruise_range, alt_range]
    plots[r'$V_{cruise\ 75\%}$'] = [v_cruise1_range, alt_range]
    plots[r'$V_{cruise\ 55\%}$'] = [v_cruise2_range, alt_range]
    plots[r'$V_{nominal}$'] = [v_nominal_range, alt_range]
    plots[r'$V_{min}$,'] = [v_min_range, alt_range]
    
    plots_2[r'$C_{y\ max\ range}$,'] = [cy_cruise_range, alt_range]
    # plots_2[r'$C_{y1}$,'] = [cy_cruise_1_range, alt_range]
    plots_2[r'$C_{y2}$,'] = plot_data_2
    # plots_2[r'$C_{y2}$,'] = [cy_cruise_2_range, alt_range]
    
    # plots_twin[r'$N_{cruise min}$'] = [p_cruise_range, alt_range]
    # plots_twin[r'$N_{cruise max}$'] = [p_cruise1_range, alt_range]
    # plots_twin[r'$N_{cruise-2}$'] = [p_cruise2_range, alt_range]
    
    limits = {"ymin": 0, "ymax": max(alt_range) + 500
        , "xmin": min(v_cruise_range) * 0.5, "xmax": max(v_cruise1_range) * 1.2}
    
    limits_2 = {"ymin": 0, "ymax": max(alt_range) + 500
        , "xmin": min(cy_cruise_2_range) * 0.5, "xmax": max(cy_cruise_2_range) * 1.2}
    
    # graph_plot_twin(plots, plots_twin, limits, title, xlabel, ylabel, xlabel_twin)
    # graph_plot(plots, limits, title, xlabel, ylabel)
    graph_plot(plots_2, limits_2, title, xlabel_2, ylabel)


def graph_plot_twin(plots, plots_twin, limits, plot_title="title", xlabel="xlabel", ylabel="ylabel",
                    xlabel_twin="xlabel_twin"):
    fg, ax = plt.subplots(figsize=(14, 10))
    ax1 = ax.twiny()
    ax1.set(xlabel=xlabel_twin)
    
    for label, data in plots.items():
        ax.plot(data[0], data[1], label=label)
    for label, data in plots_twin.items():
        ax1.plot(data[0], data[1], label=label, linestyle="-.")
    
    ax.set(title=plot_title, xlabel=xlabel, ylabel=ylabel
           , xlim=(limits["xmin"] * 0.5, limits["xmax"] * 1.1)
           , ylim=(limits["ymin"], limits["ymax"] * 1.1)
           )
    
    ax.grid(True)
    ax.legend()
    
    # ax1.grid(True)
    ax1.legend(loc=2)


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
    file = filedialog.asksaveasfile(initialfile=def_name + '.xlsx', title="Select Excel file to save"
                                    , filetypes=(("Excel books", "*.xlsx"),))
    df = pd.DataFrame(data, index=index)
    df.to_excel(file.name, header=False)


# show_req_power(project, 16000.0)
show_req_power(project, 0.0)
# show_req_power(project, 2000)
# show_req_power(project, 3000)
# show_req_power(project, 4000)
# show_req_power(project, 10000)
# show_req_power(project, 8000)
# show_fuel_consumption(project, 0)
# show_fuel_consumption(project, 2000)
# show_fuel_consumption(project, 4000)
# show_fuel_consumption(project, 6000)
# show_ld_ratio(project, np.arange(0000, 3000+1, 1000))
# glider_polar_show(project, 2000.0)
cx_vs_v_types_show(project, 1000)
cx0_vs_v_aggr_show(project, 1000)
# show_max_duration_speed(project, np.arange(0, 2000+1, 100))
# cruise_speeds_vs_alt(project, np.arange(0, 2000+1, 10))
# save_to_excel(project)
plt.show()
