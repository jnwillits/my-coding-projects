#!/usr/bin/env python

'''
Jeff's Fuel Credit Calculator
A handy utility and a coding experience for me - Jeffrey Neil Willits  @jnwillits
'''

import PySimpleGUI as sg
import json
import os

sg.ChangeLookAndFeel('Dark')
sg.SetOptions(icon='gauge.ico', element_padding=(0, 0), font=('verdana', 9), text_color='#32CD32',
              background_color='#1E1E1E', text_element_background_color='#1E1E1E')
menu_def = [['&Setup', ['Set &Credit', '&Add Vehicle', '&Delete Vehicle']],
            ['Help', '&About...'], ]
gauge_values = ['empty', '1/16', '1/8', '3/16', '1/4', '5/16', '3/8', '7/16', '1/2', '9/16', '5/8', '11/16', '3/4',
                '13/16', '7/8', '15/16', 'full']
data_dict = {}
vehicle_name = ''

frame_layout = [
    [sg.T('', background_color='#707070')],
    [sg.T('', size=(60, 2), key='_CREDIT_AMOUNT_', font=('verdana', 12), background_color='#707070',
          text_color='#FFFAFA')],
]

layout = [
    [sg.Menu(menu_def, tearoff=False, pad=(20, 1))],
    [sg.T('')],
    [sg.T('', size=(60, 1), key='_CREDIT_RATE_')],
    [sg.T('')],
    [sg.T('Select a vehicle...', text_color='#FFFAFA')],
    [sg.Listbox(vehicle_name, text_color='#32CD32', background_color='#1E1E1E', change_submits=True,
                bind_return_key=True, size=(60, 5), key='_LIST_')],
    [sg.T('')],
    [sg.T('', size=(60, 1), key='_LIST_OUTPUT_')],
    [sg.T('', size=(60, 1), key='_CAPACITY_')],
    [sg.T('', size=(60, 1), key='_val_slider_2_')],
    [sg.T('', size=(60, 1), key='_check_out_')],
    [sg.T('')],
    [sg.T('')],
    [sg.T('Indicate check-out/in fuel in 1/16th increments...', size=(60, 1), text_color='#FFFAFA')],
    [sg.T('')],
    [sg.Slider(range=(0, 16), orientation='h', text_color='#FF4500', background_color='#1E1E1E', size=(34, 12),
               default_value=8, change_submits=True, pad=(0, 0), key='_val_slider_1_')],
    [sg.T(' E     ⅛     ¼    ⅜    ½    ⅝    ¾    ⅞     F', size=(60, 1), font=('verdana', 12))],
    [sg.T('')],
    [sg.Slider(range=(0, 16), orientation='h', text_color='#FF4500', background_color='#1E1E1E', size=(34, 12),
               default_value=8, change_submits=True, pad=(0, 0), key='_val_slider_2_')],
    [sg.T(' E     ⅛     ¼    ⅜    ½    ⅝    ¾    ⅞     F', size=(60, 1), font=('verdana', 12))],
    [sg.T('')],
    [sg.T('')],
    [sg.Frame('', frame_layout, border_width=0, background_color='#707070')],
]


class Vehicle:

    def __init__(self, name, capacity):
        self.name = name
        self.capacity = capacity


def read_data():
    if os.path.isfile('fuel-credit.json'):
        with open('fuel-credit.json') as f_obj:
            data_dict = json.load(f_obj)
    else:
        data_dict = {"credit": 1.00, "Pickup Truck (sample)": 30}

    if data_dict['credit'] == None or len(data_dict) < 2:
        data_dict = {"credit": 1.00, "Pickup Truck (sample)": 30}

    credit_per_gal = float(data_dict['credit'])

    vehicle_name = list(data_dict.keys())
    # Strip 'credit' from list.
    temp_lst = []
    for i in range(0, len(vehicle_name)):
        if vehicle_name[i] != 'credit':
            temp_lst.append(vehicle_name[i])
    vehicle_name = temp_lst
    return credit_per_gal, vehicle_name, data_dict


def write_data(new_key, new_value, data_dict_pass):
    data_dict_pass[new_key] = new_value
    # Avoid null value for credit.
    # if data_dict_pass['credit'] != type(int) or data_dict_pass['credit'] != type(float):
    #     data_dict_pass['credit'] = 1

    with open('fuel-credit.json', 'w') as f_obj:
        json.dump(data_dict_pass, f_obj)
    return data_dict


def add_vehicle_form(data_dict_pass):
    layout_3 = [[sg.T('\n\n')],
                [sg.T('Vehicle name: '), sg.In(size=(60, 10), justification='left', key='_VEHICLE_NAME_')],
                [sg.T('\n\n')],
                [sg.T('Fuel tank capacity (gallons): '),
                 sg.In(size=(4, 10), justification='left', key='_VEHICLE_CAPACITY_')],
                [sg.Button('', bind_return_key=True, visible=False)], ]
    window_3 = sg.Window('Add a vehicle...', size=(300, 200)).Layout(layout_3)
    while True:
        event_3, values_3 = window_3.Read()
        if event_3 is not None:
            try:
                vehicle_name = (values_3['_VEHICLE_NAME_'])
            except:
                continue
            try:
                vehicle_capacity = float(values_3['_VEHICLE_CAPACITY_'])
                if vehicle_capacity < 1 or vehicle_capacity > 200:
                    sg.Popup('', '\nEnter a reasonable fuel capacity.\n\n', background_color='#000000',
                             keep_on_top=True)
                    continue
            except:
                sg.Popup('', '\nEnter a numerical dollar amount for capacity.\n\n', background_color='#000000',
                         keep_on_top=True)
                continue
            vehicle_obj = Vehicle(vehicle_name, vehicle_capacity)
            write_data(vehicle_obj.name, vehicle_obj.capacity, data_dict_pass)
            window_3.Close()
            # Return the vehicle object.   DONT NEED THIS.............
            return
        else:
            break
    window_3.Close()


def delete_vehicle_form(data_dict_pass):
    layout = [[sg.T('')],
              [sg.T('Select a vehicle to delete...', text_color='#FFFAFA')],
              [sg.Listbox(vehicle_name, text_color='#32CD32', background_color='#1E1E1E', change_submits=True,
                          bind_return_key=True, size=(60, 5), key='_LIST2_')],
              [sg.T('')],
              [sg.Button('Delete', visible=True, key='_BUTTON_')], ]
    window = sg.Window('Delete a vehicle...', size=(300, 200)).Layout(layout)
    while True:
        event_4, values_4 = window.Read(timeout=10)
        if event_4 is None or event_4 == 'Exit':
            break
        else:
            if event_4 is not None:
                if event_4 == '_BUTTON_':
                    vehicle_selected = values_4['_LIST2_']
                    data_dict_pass.pop(vehicle_selected[0], None)
                    if values_4['_LIST2_'].count == 0:
                        data_dict_pass = {"credit": 1.00, "Pickup Truck (sample)": 30}
                        # THIS DOESN'T FIRE....
                        sg.Popup('', '\nDeleting the final vehicle reset the data.\n\n', background_color='#000000',
                                 keep_on_top=True)
                    break
    window.Close()
    return data_dict_pass


def set_credit_form(data_dict_pass):
    layout_2 = [[sg.T('\n\n')],
                [sg.T('$ per gallon credit:'), sg.In(size=(5, 10), key='_credit_per_gal_')],
                [sg.T('', size=(6, 4), key='output')],
                [sg.Button('', bind_return_key=True, visible=False)]]
    window_2 = sg.Window('').Layout(layout_2)
    while True:
        event_2, values_2 = window_2.Read()
        if event_2 is not None:
            try:
                credit = float(values_2['_credit_per_gal_'])
                if credit < 0.01 or credit > 100:
                    sg.Popup('', '\nEnter a reasonable credit amount.\n\n', background_color='#000000',
                             keep_on_top=True)
                    continue
            except:
                sg.Popup('', '\nEnter a numerical dollar amount for credit per gallon.\n\n', background_color='#000000',
                         keep_on_top=True)
                continue
            window_2.Close()
            return credit
        else:
            # If it is going to exit without new credit input, return to previous value.
            return data_dict_pass['credit']
            break
    window_2.Close()


def calculate_credit(credit_per_gal_pass, slider_1_output_pass, slider_2_output_pass, capacity_pass):
    return ((slider_2_output_pass - slider_1_output_pass) / 16) * capacity_pass * float(credit_per_gal_pass)


def update_fuel_credit():
    fuel_credit_amount = calculate_credit(credit_per_gal, int(values['_val_slider_1_']), int(values['_val_slider_2_']),
                                          capacity)
    if fuel_credit_amount >= 0:
        window.Element('_CREDIT_AMOUNT_').Update(f'   FUEL CREDIT: ${fuel_credit_amount:2.2f}')
    else:
        window.Element('_CREDIT_AMOUNT_').Update(f'   FUEL CREDIT: ${fuel_credit_amount:2.2f} (NO CREDIT)')


if __name__ == '__main__':
    credit_per_gal, vehicle_name, data_dict = read_data()
    window = sg.Window(" Jeff's Fuel Credit Calculator", size=(400, 550), default_element_size=(30, 1),
                       grab_anywhere=False, background_color='#1E1E1E',
                       auto_size_text=False, auto_size_buttons=False).Layout(layout).Finalize()
    window.Element('_LIST_').Update(vehicle_name)
    window.Element('_CREDIT_RATE_').Update(f'Credit is set for ${credit_per_gal:2.2f} per gallon.')
    while True:
        event, values = window.Read(timeout=10)
        if event is None or event == 'Exit':
            break
        else:
            slider_1_output = gauge_values[int(values['_val_slider_1_'])]
            slider_2_output = gauge_values[int(values['_val_slider_2_'])]
            window.Element('_val_slider_2_').Update(f'Check-out fuel was {slider_1_output}.')
            window.Element('_check_out_').Update(f'Fuel level was {slider_2_output} on return.')
            vehicle_selected = values['_LIST_']
            window.Element('_LIST_OUTPUT_').Update(f'Vehicle selected: {vehicle_selected[0]}')
            capacity = data_dict[vehicle_selected[0]]
            window.Element('_CAPACITY_').Update(f'Fuel capacity: {capacity:2.1f} gallons')
            update_fuel_credit()
            if event == 'About...':
                sg.PopupNoButtons('', 'This assists with vehicle rentals. When a vehicle',
                                  'is rented with a partially full fuel tank and is',
                                  'returned with additional fuel, it calculates credit.\n',
                                  'The program is not copyrighted, it is free to use and,',
                                  'the Python source code is available to copy from my',
                                  'GitHub repository.\n',
                                  'Version 1.1 released March 29, 2019.\n\n'
                                  'Jeffrey Neil Willits', '@jnwillits\n', no_titlebar=False, keep_on_top=True,
                                  grab_anywhere=True, background_color='#000000')
            elif event == 'Set Credit':
                credit_per_gal = set_credit_form(data_dict)
                write_data('credit', credit_per_gal, data_dict)
                window.Element('_CREDIT_RATE_').Update(f'Credit is set for ${credit_per_gal:2.2f} per gallon.')
                update_fuel_credit()
            elif event == 'Add Vehicle':
                add_vehicle_form(data_dict)
                write_data('credit', credit_per_gal, data_dict)
                credit_per_gal, vehicle_name, data_dict = read_data()
                window.Element('_LIST_').Update(vehicle_name)
                vehicle_selected = values['_LIST_']
                window.Element('_LIST_OUTPUT_').Update(f'Vehicle selected: {vehicle_selected[0]}')
                capacity = data_dict[vehicle_name[0]]
                window.Element('_CAPACITY_').Update(f'Fuel capacity: {capacity:2.1f} gallons')
            elif event == 'Delete Vehicle':
                delete_vehicle_form(data_dict)
                write_data('credit', credit_per_gal, data_dict)
                credit_per_gal, vehicle_name, data_dict = read_data()
                window.Element('_LIST_').Update(vehicle_name)
            elif event == '_LIST_':
                vehicle_selected = values['_LIST_']
                window.Element('_LIST_OUTPUT_').Update(f'Vehicle selected: {vehicle_selected[0]}')
                capacity = data_dict[vehicle_selected[0]]
                window.Element('_CAPACITY_').Update(f'Fuel capacity: {capacity:2.1f} gallons')
    window.Close()
