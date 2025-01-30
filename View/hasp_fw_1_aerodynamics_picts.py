import sys
# import matplotlib.pyplot as plt
import numpy as np
from matplotlib import patheffects as pe, pyplot as plt
from Model import plane_aerodynamics as pa

hap_fw = pa.Aerodynamics()
hap_fw.set_general_params("../Projects/HAP-FW/HAP-FW_f1_general_ls_params.json")
# hap_fw.set_general_params("../Projects/P45_twin_sailplane/P45_twin_sailplane_general_ls_params.json")
hap_fw.set_plane_geometry()
hap_fw.set_toff_mass()
hap_fw.set_empty_mass()
hap_fw.set_mass(hap_fw.toff_mass)
hap_fw.set_aerodynamics()
# print(f' mass = {hap_fw.mass}kg')
hap_fw.set_cruise_regime()
hap_fw.set_altitude(3000)


# print(f'fus area = {hap_fw.geometry.fuselage_area}, fus len = {hap_fw.geometry.fuselage_length}')
# print(f'cx_0 = {hap_fw.plane_cx0_range}')
# print(f'wing cx_0 = {hap_fw.wing_cx0_range}')
# print(f'L/D = {hap_fw.plane_ld_ratio_range}')


def show_req_power(plane: pa, alt):
    plane.set_altitude(alt)
    
    title = f'ВАП-СТ, потребная мощность на высоте {plane.isa.get_altitude()}м с учетом потребления СЭС'
    xlabel = f'Скорость, км/ч'
    ylabel = f'Потребная мощность, кВт'
    
    plane.set_mass(plane.toff_mass)
    plane.set_aerodynamics()
    plane.set_cruise_regime()
    
    x_range = plane.v_range * 3.6
    y_range_max = plane.get_plane_required_power_kilowatt() + 2.5
    label_max_mass = f'Потребная мощность при массе {plane.mass}кг'
    
    plane.set_mass(plane.empty_mass)
    plane.set_aerodynamics()
    plane.set_cruise_regime()
    
    # x_rangen = plane.v_range * 3.6
    y_range_min = plane.get_plane_required_power_kilowatt() + 2.5
    label_min_mass = f'Потребная мощность при массе {plane.mass}кг'
    
    N_avail_range_toff = [100 * plane.isa.get_engine_relative_power() * .736 * 0.8 for x in plane.v_range]
    N_avail_range_cruise = [100 * plane.isa.get_engine_relative_power() * .55 * .736 * 0.8 for x in plane.v_range]
    
    plots = {label_max_mass: [x_range, y_range_max],
             label_min_mass: [x_range, y_range_min],
             "Максимальная располагаемая мощность": [x_range, N_avail_range_toff],
             "Крейсерская располагаемая мощность": [x_range, N_avail_range_cruise]
             }
    
    limits = {"xmin": min(x_range), "xmax": max(x_range), "ymin": min(y_range_min), "ymax": 80}
    graph_plot(plots, limits, title, xlabel, ylabel)


def show_fuel_consumption(plane: pa, alt):
    electric_generation = 2.5  # kW
    fuel_mass = (plane.toff_mass - plane.empty_mass) * 0.9
    fuel_mass_2 = (plane.toff_mass - plane.empty_mass) * 0.9
    fuel_remain = 5  # kg
    fuel_specific_consumption = 0.285  # kg*kW/h
    plane.set_altitude(alt)
    plane.set_mass(plane.toff_mass)
    plane.set_aerodynamics()
    plane.set_cruise_regime()
    current_power = plane.max_duration_power / 1000 + electric_generation
    duration = 0
    duration_range = []
    fuel_range = []
    consumption_range = []
    
    title = f'ВАП-СТ, график расхода топлива на крейсерском режме на высоте {plane.isa.get_altitude()}м с учетом потребления СЭС'
    xlabel = f'Время полета, ч'
    ylabel = f'Остаток топлива, кг'
    
    while fuel_mass > fuel_remain:
        fuel_hour_consumption = current_power * fuel_specific_consumption
        fuel_mass -= fuel_hour_consumption
        duration += 1
        consumption_range.append(fuel_hour_consumption)
        fuel_range.append(fuel_mass)
        duration_range.append(duration)
        plane.set_mass(plane.mass - fuel_hour_consumption)
        plane.set_aerodynamics()
        plane.set_cruise_regime()
        current_power = plane.max_duration_power / 1000 + electric_generation
        print(f'fuel amount = {fuel_mass}')
    
    print(current_power, current_power * fuel_specific_consumption)
    print(f'duration of flight = {duration}')
    
    limits = {"xmin": 0, "xmax": max(duration_range), "ymin": 0, "ymax": fuel_mass_2}
    fuel_volume_label = 'Остаток топлива, кг'
    plots = {
        fuel_volume_label: [duration_range, fuel_range],
        # fuel_consumption_label: [duration_range, consumption_range]
    }
    graph_plot(plots, limits, title, xlabel, ylabel)
    
    title = f'ВАП-СТ, часовой расход топлива на крейсерском режме на высоте {plane.isa.get_altitude()}м с учетом потребления СЭС'
    xlabel = f'Время полета, ч'
    ylabel = f'Расход топлива, кг/ч'
    
    fuel_consumption_label = 'Часовой расход топлива, кг '
    limits_consumption = {"xmin": 0, "xmax": max(duration_range), "ymin": 0, "ymax": max(consumption_range)}
    plots_consumption = {
        # fuel_volume_label: [duration_range, fuel_range],
        fuel_consumption_label: [duration_range, consumption_range]
    }
    graph_plot(plots_consumption, limits_consumption, title, xlabel, ylabel)


def show_ld_ratio(plane: pa, alt_range: list):
    title = f'ВАП-СТ, аэродинамическое качество по высотам'
    xlabel = f'Скорость, км/ч'
    ylabel = r'$K_a$'
    plots_ld_ratio = {}
    limits_ld_ratio = {}
    
    for alt in alt_range:
        plane.set_altitude(alt)
        plane.set_mass = (plane.toff_mass + plane.empty_mass) / 2
        plane.set_aerodynamics()
        ld_ratio_range = plane.get_plane_ld_ratio_range()
        limits_ld_ratio = {"xmin": min(plane.v_range * 3.6), "xmax": max(plane.v_range * 3.6)
                           , "ymin": min(ld_ratio_range), "ymax": max(ld_ratio_range)
                           # , "ymin": -5, "ymax": 0.1
                           }
        ld_ratio_label = r'$K_a$' f' на высоте {alt}м'
        plots_ld_ratio[ld_ratio_label] = [plane.v_range * 3.6, ld_ratio_range]
    graph_plot(plots_ld_ratio, limits_ld_ratio, title, xlabel, ylabel)


def graph_plot(plots, limits, plot_title="title", xlabel="xlabel", ylabel="ylabel"):
    fg, ax = plt.subplots(figsize=(14, 10))
    # print(plots, type(plots))
    # dd = {"a": 11, "b": 22}
    # for k, v in dd:
    #     print(k, v)
    for title, data in plots.items():
        # print(t, type(t))
        # print(d, type(d))
        ax.plot(data[0], data[1], label=title)
    #
    # print(*plots.items())
    ax.set(title=plot_title, xlabel=xlabel, ylabel=ylabel
           , xlim=(limits["xmin"] * 0.5, limits["xmax"] * 1.1)
           , xticks=np.arange(limits["xmin"] * 5 // 100 * 10, limits["xmax"] * 11 // 10, limits["xmax"] // 100 * 10)
           , ylim=(limits["ymin"], limits["ymax"] * 1.1)
           , yticks=np.arange(limits["ymin"]*5 // 10, limits["ymax"] * 11 // 10, limits["ymax"] // 10 + 1)
           # , xticks=np.arange(limits["xmin"], limits, 20)
           # , yticks=2
           )
    
    ax.grid(True)
    ax.legend()
    # plt.show()


# show_req_power(hap_fw, 0)
# show_req_power(hap_fw, 3000)
# show_req_power(hap_fw, 5000)
# show_req_power(hap_fw, 7000)
# show_fuel_consumption(hap_fw, 3000)
# show_fuel_consumption(hap_fw, 5000)
# show_fuel_consumption(hap_fw, 7000)
show_ld_ratio(hap_fw, [0, 3000, 5000, 7000])
plt.show()
