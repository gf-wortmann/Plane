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
    
    def show_req_power_electric_simplex(self, alt):
        plane = self.plane
        electric_power_consumption = plane.general_params["power_plant"]["electric_power_consumption"]  # kW
        prop_effectivity = plane.general_params["power_plant"]["prop_effectivity"]
        plane.set_altitude(alt)
        
        title = f'{plane.general_params["project"]["project_name"]}, потребная мощность на высоте {plane.isa.get_altitude()}'
        xlabel = f'Скорость, км/ч'
        ylabel = f'Потребная мощность, кВт'
        
        plane.set_mass(plane.toff_mass)
        plane.calculate_aerodynamics()
        plane.calculate_max_duration_power()
        
        x_range = plane.v_range * 3.6
        
        plane.set_mass(plane.toff_mass - plane.fuel_mass)  # min mass
        plane.calculate_aerodynamics()
        plane.calculate_max_duration_power()
        y_range_min_mass = plane.get_plane_required_power_kilowatt()
        
        label_min_mass = f'Потребная мощность при массе {plane.mass:.0f}кг. ' r'$P_{min}$ =' f'{plane.max_duration_power / 1000 + electric_power_consumption:.2f}кВт на {plane.max_duration_speed * 3.6:.1f}км/ч'
        
        power_avail_range_nominal = [plane.general_params["power_plant"]["nominal_power_kw"] * prop_effectivity
                                     for x in plane.v_range]
        
        plots = {
            # label_max_mass: [x_range, y_range_max_mass],
            label_min_mass: [x_range, y_range_min_mass],
            f"Располагаемая мощность, номинальный режим {max(power_avail_range_nominal):.0f} кВт":
                [x_range, power_avail_range_nominal],
        }
        
        limits = {"xmin": min(x_range), "xmax": max(x_range), "ymin": min(y_range_min_mass) / 2,
                  "ymax": plane.general_params["power_plant"][
                              "nominal_power_kw"] * 1.5}
        self.graph_plot(plots, limits, title, xlabel, ylabel)
    
    def show_climb_on(self, alt):
        
        title = f'{self.plane.general_params["project"]["project_name"]}, график подъёма до высоты {alt}м '\
                r'при $G_0$ = ' f'{self.plane.mass}кг'
        xlabel = f'Время, ч'
        ylabel = f'Высота, м'
        
        power = self.plane.general_params["power_plant"]["nominal_power_kw"] * 1000
        electric_power_consumption = self.plane.general_params["power_plant"]["electric_power_consumption"]  # kW
        prop_effectivity = self.plane.general_params["power_plant"]["prop_effectivity"]
        alt_step = 10  #m
        
        alt_range = np.arange(0, alt + 1, alt_step)
        ext_range = []
        for alt in alt_range:
            self.plane.set_altitude(alt)
            alt_max_ext = max(power - self.plane.plane_required_power_range)
            for v, n in zip(self.plane.v_range, self.plane.plane_required_power_range):
                if power - n == alt_max_ext:
                    break
            
            real_ext = alt_max_ext * prop_effectivity * 0.95 - electric_power_consumption
            ext_range.append(real_ext)
        
        vy_range = [x / self.plane.mass / 9.81 for x in ext_range]
        time_range = [alt_step / x for x in vy_range]
        time_acc = [time_range[0]]
        
        for i in range(1, len(time_range)):
            time_acc.append(time_acc[i - 1] + time_range[i])
        
        time_acc_hr = [x / 3600 for x in time_acc]
        
        energy_consumption = power /1000 * max(time_acc_hr)  # kWh
        
        title = ((title
                 + f'\nРасход энергии без учета КПД БКС = {energy_consumption:.0f}кВт*ч')
                 + f'\nМасса аккумулятора от {energy_consumption / 0.25:.0f}кг')
        print(title)
        
        plots = {
            f'': [time_acc_hr, alt_range]
        }
        limits = {"xmin": 0, "xmax": max(time_acc_hr), "ymin": 0, "ymax": (max(alt_range) * 1.2)}
        
        self.graph_plot(plots, limits, title, xlabel, ylabel)
    
    def graph_plot(self, plots, limits, plot_title="title", xlabel="xlabel", ylabel="ylabel"):
        fg, ax = plt.subplots(figsize=(14, 10))
        for label, data in plots.items():
            ax.plot(data[0], data[1], label=label)

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
        plt.show()


if __name__ == "__main__":
    rep = Reports()
    rep.set_general_params(
        "C:/Users/79267/Urban_Univercity/Python_Developer/Plane_Project/Projects/HAP-FW/HAP-FW_electric_T-Motor U15 XXL KV29.json")
    # rep.set_general_params(
    #     "C:/Users/79267/Urban_Univercity/Python_Developer/Plane_Project/Projects/HAP-FW/HAP-FW_electric_M100.json")
    rep.set_plane()
    print(rep.plane.toff_mass)
    rep.show_req_power_electric_simplex(0)
    rep.show_req_power_electric_simplex(10000)
    # rep.show_climb_on(10000)
   