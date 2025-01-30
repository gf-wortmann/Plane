import tkinter as tk
from Presenter import ps_2 as ps
import tkinter.ttk as ttk


_bgcolor = '#d9d9d9'
_fgcolor = 'black'
_tabfg1 = 'black'
_tabfg2 = 'white'
_bgmode = 'light'
_tabbg1 = '#d9d9d9'
_tabbg2 = 'gray40'
_actbg = '#aaccf8'


class InitialForm:
    def __init__(self, top, callback):
        super().__init__()
        '''This class configures and populates the toplevel window.
           top is the toplevel containing window.'''
        
        top.geometry("400x50")
        # top.minsize(200, 100)
        # top.maxsize(2000, 1400)
        top.resizable(0, 0)
        top.title("PlaneGeometry parameters")
        top.configure(background="#cfcfcf", highlightbackground="#d9d9d9", highlightcolor="black")
        
        self.top = top
        self.callback = callback
        
        self.menubar = tk.Menu(top, font="TkMenuFont", bg=_bgcolor, fg=_fgcolor, activebackground=_actbg)
        top.configure(menu=self.menubar)
        
        self.sub_menu = tk.Menu(self.menubar, activebackground=_actbg
                                , activeborderwidth=1, activeforeground='black'
                                , background='#d9d9d9', borderwidth=1, disabledforeground='#a3a3a3'
                                , font="-family {Segoe UI} -size 9", foreground='black', tearoff=1)
        
        self.menubar.add_cascade(compound='left'
                                 , font="-family {Segoe UI} -size 9", label='File'
                                 , menu=self.sub_menu, )
        self.sub_menu.add_command(compound='left'
                                  , font="-family {Segoe UI} -size 9", label='Save')
        self.sub_menu1 = tk.Menu(self.menubar, activebackground=_actbg
                                 , activeborderwidth=1, activeforeground='black'
                                 , background='#d9d9d9', borderwidth=1, disabledforeground='#a3a3a3'
                                 , font="-family {Segoe UI} -size 9", foreground='black', tearoff=1)
        
        self.menubar.add_cascade(compound='left'
                                 , font="-family {Segoe UI} -size 9", label='New calculation'
                                 , menu=self.sub_menu1, )
        self.sub_menu1.add_command(command=self.lifting_system_pressed
                                   , compound='left', font="-family {Segoe UI} -size 9"
                                   , label='Lifting System')
        self.sub_menu1.add_command(compound='left'
                                   , font="-family {Segoe UI} -size 9", label='Polar')
        
        # self.sub_menu1.

    def lifting_system_pressed(self):
        #
        # args = {'wing_area': 10  #float(self.WingAreaValue.get())
        #     , 'wing_aspect_ratio': 12.5  # float(self.WingARValue.get())
        #     , 'wing_taper_ratio_ru': 2.5  #float(self.WingTaperRatioValue.get())
        #     , 'stab_volume_coefficient': 0.5  #float(self.StabVolumeCoeffValue.get())
        #     , 'stab_arm': 3.0  #float(self.StabArmLengthValue.get())
        #     , 'fin_volume_coefficient': 0.05  #float(self.FinVolumeCoeffValue.get())
        #     , 'fin_arm': 3.0  #float(self.FinArmLengthValue.get())
        #     , 'fins_count': 1  #int(self.FinsCountValue.get())
        #         }
        #
        # self.callback(self.top, args)
        self.callback(self.top, 'lifting_system')
    
    

# def start_dialog():
#     ps.start_dialog()

# if __name__ == '__main__':
#     global root
#     root = tk.Tk()
#     root.protocol('WM_DELETE_WINDOW', root.destroy)
#     # Creates a toplevel widget.
#     global initial_window
#     # _top2 = root
#     initial_window = InitialForm(root)
#     # Creates a toplevel widget.
#
#     root.mainloop()
