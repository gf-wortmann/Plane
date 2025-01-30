import sys
import tkinter as tk
from View import initial_form_2 as iform
from View import lifting_system_dialog_2 as lsd
from Model import lifting_system as lift
import json

_debug = True
container = []
# _top = tk.Tk()
init_window = None
global_root = None
# root = tk.Tk
# root.protocol('WM_DELETE_WINDOW', root.destroy)


def start_dialog():
    global root
    root = tk.Tk()
    global_root = root
    # root.protocol('WM_DELETE_WINDOW', root.destroy)
    # iform.InitialForm(root, calculate_lifting_system)
    iform.InitialForm(root, callback_func)
    root.mainloop()


def callback_func(sender, command):
    if _debug:
        print(f'in callback_func({type(sender)}, {command})')
    sender.title('called back!')
    
    if command == 'lifting_system':
        # global lsw
        # lsw = tk.Toplevel()
        lsd.LiftingSystemCalc(tk.Toplevel(), calculate_lifting_system)
    
    # pass


def calculate_lifting_system(sender: lsd.LiftingSystemCalc, lift_input):
    if _debug:
        print("in calculate_lifting_system")
        container.clear()
        for arg in lift_input:
            print('    another arg:', arg, lift_input[arg])
            container.append({arg: lift_input[arg]})
        sys.stdout.flush()
    
    lls = lift.LiftingSystem()
    lls.set_wing_general_geometry(lift_input['wing_area'], lift_input['wing_aspect_ratio']
                                  , lift_input['wing_taper_ratio_ru'])
    lls.set_tail_general_geometry(lift_input['stab_arm'], lift_input['fin_arm']
                                  , lift_input['stab_volume_coefficient'], lift_input['fin_volume_coefficient'])
    lls.set_fins_count(lift_input['fins_count'])

    result = {'stab_area': lls.get_stab_area(), 'fin_area': lls.get_fin_area(), 'wing_span': lls.get_wing_span()}
    sender.show_lifting_system_result(result)

    if _debug:
        print(f'wing area = {lls.get_wing_area()}, wing_span = {lls.get_wing_span()}, '
              f'\nstab area = {lls.get_stab_area()}, fin area = {lls.get_fin_area()}')
        print(result)
        for arg in result:
            container.append({arg: result[arg]})
            
    if _debug:
        print(f'container contains:')
        for i in container:
            print(i)
        with open ('tst_ls.json', 'w', encoding='utf-8') as f:
            json.dump([{'_debug': [{'ttt': 234}]}, {'lifting_system': container}], f, ensure_ascii=False, indent=4)
        print(container)
        


if __name__ == '__main__':
    start_dialog()
    
    # pass
    # iform.start_dialog()
