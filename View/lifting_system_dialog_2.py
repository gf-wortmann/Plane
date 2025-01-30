import tkinter as tk
# from Presenter import ps_2 as ps

_debug = True

_bgcolor = '#d9d9d9'
_fgcolor = 'black'
_tabfg1 = 'black'
_tabfg2 = 'white'
_bgmode = 'light'
_tabbg1 = '#d9d9d9'
_tabbg2 = 'gray40'
_actbg = '#aaccf8'


class LiftingSystemCalc:
    
    def __init__(self, top, callback):
        '''This class configures and populates the toplevel window.
           top is the toplevel containing window.'''
        
        top.geometry("1052x483+524+357")
        top.minsize(800, 250)
        top.maxsize(2000, 1400)
        top.resizable(1, 1)
        top.title("Lifting System")
        top.configure(background="#d9d9d9", highlightbackground="#d9d9d9", highlightcolor="black")
        
        self.top = top
        self.callback = callback
        
        self.InputFrame = tk.Frame(self.top)
        self.InputFrame.place(x=0, y=0, height=125, width=700)
        self.InputFrame.configure(relief='groove')
        self.InputFrame.configure(borderwidth="2")
        # self.InputFrame.configure(relief="groove")
        self.InputFrame.configure(background="#d9d9d9")
        self.InputFrame.configure(highlightbackground="#d9d9d9")
        self.InputFrame.configure(highlightcolor="black")
        
        self.StabVolumeCoeffFrame = tk.LabelFrame(self.InputFrame)
        self.StabVolumeCoeffFrame.place(x=6, y=0, height=50, width=150)
        self.StabVolumeCoeffFrame.configure(relief='groove')
        self.StabVolumeCoeffFrame.configure(font="-family {Segoe UI} -size 9")
        self.StabVolumeCoeffFrame.configure(foreground="black")
        self.StabVolumeCoeffFrame.configure(text='''Stab Volume coefficient''')
        self.StabVolumeCoeffFrame.configure(background="#d9d9d9")
        self.StabVolumeCoeffFrame.configure(highlightbackground="#d9d9d9")
        self.StabVolumeCoeffFrame.configure(highlightcolor="black")
        
        self.StabVolumeCoeffValue = tk.Entry(self.StabVolumeCoeffFrame)
        self.StabVolumeCoeffValue.place(x=6, y=24, height=20, width=100
                                        , bordermode='ignore')
        self.StabVolumeCoeffValue.delete(0, 'end')
        self.StabVolumeCoeffValue.insert(0, '0.5')
        self.StabVolumeCoeffValue.configure(background="white", disabledforeground="#a3a3a3", foreground="black"
                                            , highlightbackground="#d9d9d9",highlightcolor="black"
                                            , insertbackground="black", selectbackground="#d9d9d9"
                                            ,selectforeground="black")
        
        self.StabArmLengthFrame = tk.LabelFrame(self.InputFrame)
        self.StabArmLengthFrame.place(x=160, y=0, height=50, width=150)
        self.StabArmLengthFrame.configure(relief='groove')
        self.StabArmLengthFrame.configure(font="-family {Segoe UI} -size 9")
        self.StabArmLengthFrame.configure(foreground="black")
        self.StabArmLengthFrame.configure(text='''Stab Arm Lenght''')
        self.StabArmLengthFrame.configure(background="#d9d9d9")
        self.StabArmLengthFrame.configure(highlightbackground="#d9d9d9")
        self.StabArmLengthFrame.configure(highlightcolor="black")
        
        self.StabArmLengthValue = tk.Entry(self.StabArmLengthFrame)
        self.StabArmLengthValue.place(x=6, y=24, height=20, width=100
                                      , bordermode='ignore')
        self.StabArmLengthValue.configure(background="white")
        self.StabArmLengthValue.configure(disabledforeground="#a3a3a3")
        self.StabArmLengthValue.configure(font="-family {Courier New} -size 10")
        self.StabArmLengthValue.configure(foreground="black")
        self.StabArmLengthValue.configure(highlightbackground="#d9d9d9")
        self.StabArmLengthValue.configure(highlightcolor="black")
        self.StabArmLengthValue.configure(insertbackground="black")
        self.StabArmLengthValue.configure(selectbackground="#d9d9d9")
        self.StabArmLengthValue.configure(selectforeground="black")
        self.StabArmLengthValue.delete(0, 'end')
        self.StabArmLengthValue.insert(0, '3.0')
        
        self.FinVolumeCoeffFrame = tk.LabelFrame(self.InputFrame)
        self.FinVolumeCoeffFrame.place(x=316, y=0, height=50, width=150)
        self.FinVolumeCoeffFrame.configure(relief='groove')
        self.FinVolumeCoeffFrame.configure(font="-family {Segoe UI} -size 9")
        self.FinVolumeCoeffFrame.configure(foreground="black")
        self.FinVolumeCoeffFrame.configure(text='''Fin Volume coefficient''')
        self.FinVolumeCoeffFrame.configure(background="#d9d9d9")
        self.FinVolumeCoeffFrame.configure(highlightbackground="#d9d9d9")
        self.FinVolumeCoeffFrame.configure(highlightcolor="black")
        
        self.FinVolumeCoeffValue = tk.Entry(self.FinVolumeCoeffFrame)
        self.FinVolumeCoeffValue.place(x=6, y=24, height=20, width=100
                                       , bordermode='ignore')
        self.FinVolumeCoeffValue.configure(background="white")
        self.FinVolumeCoeffValue.configure(disabledforeground="#a3a3a3")
        self.FinVolumeCoeffValue.configure(font="-family {Courier New} -size 10")
        self.FinVolumeCoeffValue.configure(foreground="black")
        self.FinVolumeCoeffValue.configure(highlightbackground="#d9d9d9")
        self.FinVolumeCoeffValue.configure(highlightcolor="black")
        self.FinVolumeCoeffValue.configure(insertbackground="black")
        self.FinVolumeCoeffValue.configure(selectbackground="#d9d9d9")
        self.FinVolumeCoeffValue.configure(selectforeground="black")
        
        self.FinVolumeCoeffValue.delete(0, 'end')
        self.FinVolumeCoeffValue.insert(0, '0.05')
        
        self.FinArmLengthFrame = tk.LabelFrame(self.InputFrame)
        self.FinArmLengthFrame.place(x=470, y=0, height=50, width=150)
        self.FinArmLengthFrame.configure(relief='groove')
        self.FinArmLengthFrame.configure(font="-family {Segoe UI} -size 9")
        self.FinArmLengthFrame.configure(foreground="black")
        self.FinArmLengthFrame.configure(text='''Fin Arm Lenght''')
        self.FinArmLengthFrame.configure(background="#d9d9d9")
        self.FinArmLengthFrame.configure(highlightbackground="#d9d9d9")
        self.FinArmLengthFrame.configure(highlightcolor="black")
        
        self.FinArmLengthValue = tk.Entry(self.FinArmLengthFrame)
        self.FinArmLengthValue.place(x=6, y=24, height=20, width=100
                                     , bordermode='ignore')
        # self.FinArmLengthValue.configure(background="white")
        # self.FinArmLengthValue.configure(disabledforeground="#a3a3a3")
        # self.FinArmLengthValue.configure(foreground="black")
        # self.FinArmLengthValue.configure(highlightbackground="#d9d9d9")
        # self.FinArmLengthValue.configure(highlightcolor="black")
        # self.FinArmLengthValue.configure(insertbackground="black")
        # self.FinArmLengthValue.configure(selectbackground="#d9d9d9")
        # self.FinArmLengthValue.configure(selectforeground="black")
        
        self.FinArmLengthValue.delete(0,'end')
        self.FinArmLengthValue.insert(0, '3.0')
        
        self.WingAreaFrame = tk.LabelFrame(self.InputFrame)
        self.WingAreaFrame.place(x=6, y=60, height=50, width=150)
        self.WingAreaFrame.configure(relief='groove')
        # self.WingAreaFrame.configure(font="-family {Segoe UI} -size 9")
        self.WingAreaFrame.configure(foreground="black")
        self.WingAreaFrame.configure(text='''Wing area''')
        self.WingAreaFrame.configure(background="#d9d9d9")
        # self.WingAreaFrame.configure(highlightbackground="#d9d9d9")
        # self.WingAreaFrame.configure(highlightcolor="black")
        
        self.WingAreaValue = tk.Entry(self.WingAreaFrame)
        self.WingAreaValue.place(x=6, y=24, height=20, width=100
                                 , bordermode='ignore')
        # self.WingAreaValue.configure(background="white")
        # self.WingAreaValue.configure(disabledforeground="#a3a3a3")
        # self.WingAreaValue.configure(font="-family {Courier New} -size 10")
        # self.WingAreaValue.configure(foreground="black")
        # self.WingAreaValue.configure(highlightbackground="#d9d9d9")
        # self.WingAreaValue.configure(highlightcolor="black")
        # self.WingAreaValue.configure(insertbackground="black")
        # self.WingAreaValue.configure(selectbackground="#d9d9d9")
        # self.WingAreaValue.configure(selectforeground="black")
        
        self.WingAreaValue.delete(0, 'end')
        self.WingAreaValue.insert(0, '10')
        
        self.WingARFrame = tk.LabelFrame(self.InputFrame)
        self.WingARFrame.place(x=160, y=60, height=50, width=150)
        self.WingARFrame.configure(relief='groove', foreground="black", text='''Wing Aspect Ratio'''
                                   , background="#d9d9d9", highlightbackground="#d9d9d9", highlightcolor="black")
        
        self.WingARValue = tk.Entry(self.WingARFrame)
        self.WingARValue.place(x=6, y=24, height=20, width=100, bordermode='ignore')
        # self.WingARValue.configure(background="white", disabledforeground="#a3a3a3", foreground="black"
        #                            , highlightbackground="#d9d9d9", highlightcolor="black", insertbackground="black"
        #                            , selectbackground="#d9d9d9", selectforeground="black")
        self.WingARValue.insert(0, '10')
        
        self.WingTaperRatioFrame = tk.LabelFrame(self.InputFrame)
        self.WingTaperRatioFrame.place(x=316, y=60, height=50, width=150)
        self.WingTaperRatioFrame.configure(relief='groove', foreground="black", text='''Wing taper ratio RU'''
                                           , background="#d9d9d9", highlightbackground="#d9d9d9",
                                           highlightcolor="black")
        
        self.WingTaperRatioValue = tk.Entry(self.WingTaperRatioFrame)
        self.WingTaperRatioValue.place(x=6, y=24, height=20, width=100, bordermode='ignore')
        self.WingTaperRatioValue.configure(background="white", disabledforeground="#a3a3a3", foreground="black"
                                           , highlightbackground="#d9d9d9", highlightcolor="black",
                                           insertbackground="black"
                                           , selectbackground="#d9d9d9", selectforeground="black")
        self.WingTaperRatioValue.insert(0, '1.0')
        
        self.FinsCount = tk.LabelFrame(self.InputFrame)
        self.FinsCount.place(x=470, y=60, height=50, width=150)
        self.FinsCount.configure(relief='groove', foreground="black", text='''Fins count''', background="#d9d9d9"
                                 , highlightbackground="#d9d9d9", highlightcolor="black")
        
        self.FinsCountValue = tk.Entry(self.FinsCount)
        self.FinsCountValue.place(x=6, y=6, height=20, width=100)
        self.FinsCountValue.configure(background="white", disabledforeground="#a3a3a3", foreground="black"
                                      , highlightbackground="#d9d9d9", highlightcolor="black", insertbackground="black"
                                      , selectbackground="#d9d9d9", selectforeground="black")
        self.FinsCountValue.insert(0, '1')
        
        self.LSCalculate = tk.Button(self.InputFrame)
        self.LSCalculate.place(x=626, y=6, height=100, width=65)
        self.LSCalculate.configure(activebackground="#d9d9d9")
        self.LSCalculate.configure(activeforeground="black")
        self.LSCalculate.configure(background="#d9d9d9")
        self.LSCalculate.configure(borderwidth="4")
        self.LSCalculate.configure(command=self.calculate_lifting_system)
        self.LSCalculate.configure(disabledforeground="#a3a3a3")
        self.LSCalculate.configure(font="-family {Segoe UI} -size 9")
        self.LSCalculate.configure(foreground="black")
        self.LSCalculate.configure(highlightbackground="#d9d9d9")
        self.LSCalculate.configure(highlightcolor="black")
        self.LSCalculate.configure(text='Calculate''\n''lifting''\n''system')
        
        self.OutputFrame = tk.Frame(self.top)
        self.OutputFrame.place(x=0, y=140, height=125, width=700)
        self.OutputFrame.configure(relief='groove')
        self.OutputFrame.configure(borderwidth="2")
        self.OutputFrame.configure(background="#d9d9d9")
        self.OutputFrame.configure(highlightbackground="#d9d9d9")
        self.OutputFrame.configure(highlightcolor="black")
        
        # self.OutputFrame
        self.StabAreaFrame = tk.LabelFrame(self.OutputFrame)
        self.StabAreaFrame.place(x=6, y=0, height=50, width=150)
        self.StabAreaFrame.configure(text='Stab area', relief='groove', foreground="black", background="#d9d9d9"
                                     , highlightbackground="#d9d9d9", highlightcolor="black")
        
        self.StabAreaValue = tk.Entry(self.StabAreaFrame)
        self.StabAreaValue.place(x=6, y=6, height=20, width=100)
        self.StabAreaValue.configure(state='readonly')
        
        self.FinAreaFrame = tk.LabelFrame(self.OutputFrame)
        self.FinAreaFrame.place(x=160, y=0, height=50, width=150)
        self.FinAreaFrame.configure(text='Fin area', relief='groove', foreground="black", background="#d9d9d9"
                                    , highlightbackground="#d9d9d9", highlightcolor="black")
        
        self.FinAreaValue = tk.Entry(self.FinAreaFrame)
        self.FinAreaValue.place(x=6, y=6, height=20, width=100)
        self.FinAreaValue.configure(state='readonly')
        
        self.WingSpanFrame = tk.LabelFrame(self.OutputFrame)
        self.WingSpanFrame.place(x=320, y=0, height=50, width=150)
        self.WingSpanFrame.configure(text='Wing span', relief='groove', foreground="black", background="#d9d9d9"
                                     , highlightbackground="#d9d9d9", highlightcolor="black")
        
        self.WingSpanValue = tk.Entry(self.WingSpanFrame)
        self.WingSpanValue.place(x=6, y=6, height=20, width=100)
        self.WingSpanValue.configure(state='readonly')
    
    def calculate_lifting_system(self):
        # self.WingArea = float(self.WingAreaValue.get())
        # self.WingAspectRatio = float(self.WingARValue.get())
        # wa = float(self.WingAreaValue.get())
        # print(f'wing area = {self.WingArea}')
        # args = [self.WingArea, self.WingAspectRatio]
        args = {'wing_area': float(self.WingAreaValue.get())
            , 'wing_aspect_ratio': float(self.WingARValue.get())
            , 'wing_taper_ratio_ru': float(self.WingTaperRatioValue.get())
            , 'stab_volume_coefficient': float(self.StabVolumeCoeffValue.get())
            , 'stab_arm': float(self.StabArmLengthValue.get())
            , 'fin_volume_coefficient': float(self.FinVolumeCoeffValue.get())
            , 'fin_arm': float(self.FinArmLengthValue.get())
            , 'fins_count': int(self.FinsCountValue.get())
                }
        self.callback(self, args)
    
    def show_lifting_system_result(self, result):
        if _debug:
            print('show_lifting_system_result')
            for arg in result:
                print(f'    yet another arg:', arg)
        self.StabAreaValue.configure(state='normal')
        self.StabAreaValue.delete(0, 'end')
        self.StabAreaValue.insert(0, f'{result["stab_area"]:.2f}')
        self.StabAreaValue.configure(state='readonly')
        
        self.FinAreaValue.configure(state='normal')
        self.FinAreaValue.delete(0, 'end')
        self.FinAreaValue.insert(0, f'{result["fin_area"]:.2f}')
        self.FinAreaValue.configure(state='readonly')
        
        self.WingSpanValue.configure(state='normal')
        self.WingSpanValue.delete(0, 'end')
        self.WingSpanValue.insert(0, f'{result["wing_span"]:.2f}')
        self.WingSpanValue.configure(state='readonly')


if __name__ == '__main__':
    global root
    root = tk.Tk()
    root.protocol('WM_DELETE_WINDOW', root.destroy)
    # Creates a toplevel widget.
    global _w2
    # _top2 = root
    _w2 = LiftingSystemCalc(root)
    # Creates a toplevel widget.
    # _w2.StabAreaValue.insert(0, '000')
    # _w2.StabAreaValue.insert(1, '111')
    
    root.mainloop()
