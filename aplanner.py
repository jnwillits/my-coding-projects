#!/usr/bin/env python
"""
Jeff's Lien Sale Event Tracker

This helps with self storage planning for unit auctions. It does not have much general value as it requires a specific
Excel export from Sitelink operational self storage software. The code is useful to me for reference because it
contains methods for reading and handling files, date math, applications of the PySimpleGui framework, and it contains
simple methods for accessing values of nested dictionaries.

- Jeffrey Neil Willits  @jnwillits
"""

import PySimpleGUI as sg
import json
import os
import sys
import pandas as pd
from dateutil.parser import *
from datetime import datetime
from collections import defaultdict

sg.ChangeLookAndFeel('Dark')
sg.SetOptions(icon='aplanner_icon.ico', element_padding=(6, 6), font=('verdana', 9), text_color='#32CD32',
              background_color='#1E1E1E', text_element_background_color='#1E1E1E', button_color=('#32CD32', '#2F2F2F'))
unit_sub_dict = {}
unit_lst = []
ptd = ''
f_path = ''

menu_def = [['Setup', ['Display Data', ]],
            ['Help', 'About...']]

frame_layout = [
    [sg.T('PDN', size=(12, 1), background_color='#2f2f2f'),
     sg.T('', size=(2, 1), background_color='# 2f2f2f', ),
     sg.T('    PLN', size=(12, 1), background_color='#2f2f2f'),
     sg.T('', size=(2, 1), background_color='#2f2f2f', ),
     sg.T('          NLS', size=(12, 1), background_color='#2f2f2f'),
     sg.T('', size=(2, 1), background_color='#2f2f2f', ),
     sg.T('              FD', size=(12, 1), background_color='#2f2f2f'), ],
    [sg.Listbox(unit_lst, text_color='#32CD32', font=('Courier', 10, 'bold'), background_color='#1E1E1E',
                change_submits=True, bind_return_key=True, size=(10, 10), key='_PDN_LISTBOX_'),
     sg.T('', size=(4, 1), background_color='#2f2f2f', ),
     sg.Listbox(unit_lst, text_color='#32CD32', font=('Courier', 10, 'bold'), background_color='#1E1E1E',
                change_submits=True, bind_return_key=True, size=(10, 10), key='_PLN_LISTBOX_'),
     sg.T('', size=(5, 1), background_color='#2f2f2f', ),
     sg.Listbox(unit_lst, text_color='#32CD32', font=('Courier', 10, 'bold'), background_color='#1E1E1E',
                change_submits=True, bind_return_key=True, size=(10, 10), key='_NLS_LISTBOX_'),
     sg.T('', size=(4, 1), background_color='#2f2f2f', ),
     sg.Listbox(unit_lst, text_color='#32CD32', font=('Courier', 10, 'bold'), background_color='#1E1E1E',
                change_submits=True, bind_return_key=True, size=(10, 10), key='_FD_LISTBOX_'), ],
    [sg.Button('Today', visible=True, size=(12, 1), key='_PDN_COMPLETE_TODAY_'),
     sg.T('', size=(4, 1), background_color='#2f2f2f', ),
     sg.Button('Today', visible=True, size=(12, 1), key='_PLN_COMPLETE_TODAY_'),
     sg.T('', size=(4, 1), background_color='#2f2f2f', ),
     sg.Button('Today', visible=True, size=(12, 1), key='_NLS_COMPLETE_TODAY_'),
     sg.T('', size=(4, 1), background_color='#2f2f2f', ),
     sg.Button('Today', visible=True, size=(12, 1), key='_FD_COMPLETE_TODAY_'), ],
    [sg.Button('Past Date...', visible=True, size=(12, 1), key='_PDN_PAST_DATE_'),
     sg.T('', size=(4, 1), background_color='#2f2f2f', ),
     sg.Button('Past Date...', visible=True, size=(12, 1), key='_PLN_PAST_DATE_'),
     sg.T('', size=(4, 1), background_color='#2f2f2f', ),
     sg.Button('Past Date...', visible=True, size=(12, 1), key='_NLS_PAST_DATE_'),
     sg.T('', size=(4, 1), background_color='#2f2f2f', ),
     sg.Button('Past Date...', visible=True, size=(12, 1), key='_FD_PAST_DATE_'), ]]

layout = [
    [sg.Menu(menu_def, tearoff=False, pad=(20, 1))],
    [sg.T('')],
    [sg.T('', size=(60, 1), key='_PAST_DUE_COUNT_')],
    [sg.T('')],
    [sg.Frame('', frame_layout, border_width=0, size=(4, 250), background_color='#2f2f2f')], ]


def read_files():
    unit_dict = defaultdict(dict)
    if os.path.isfile('aplanner-filepath.json'):
        with open('aplanner-filepath.json') as f_obj:
            f_path = json.load(f_obj)
    else:
        sg.Popup('', '\nThe path to the following file must be identified: Aloha Self Storage - '
                     'Lahaina - Past Due Balances.xlsx\n\n', background_color='#000000', keep_on_top=True)
        if len(sys.argv) == 1:
            event, (f_path,) = sg.Window('My Script').Layout([[sg.Text('Document to open')],
                                                              [sg.In(size=(100, 10)), sg.FileBrowse()],
                                                              [sg.CloseButton('Open'),
                                                               sg.CloseButton('Cancel')]]).Read()
        else:
            f_path = sys.argv[1]
        if not f_path:
            sg.Popup("Cancel", "No file path was supplied.")
            raise SystemExit("Cancelling: no file name supplied.")
    df = pd.read_excel(f_path, sheet_name='Sheet1')
    unit_lst = (df['Unit'])
    paidthru_lst = (df['PaidThru'])
    if os.path.isfile('aplanner.json'):
        with open('aplanner.json') as f_obj:
            unit_dict = dict(json.load(f_obj))
    else:  # There's no file so start populating a new dictionary.
        for i in range(0, len(unit_lst)):
            unit_dict[unit_lst[i]]['ptd'] = str(parse(str(paidthru_lst[i])).date())
    return unit_lst, paidthru_lst, unit_dict, f_path


def write_data(f_path_pass, unit_dict_pass):
    with open('aplanner.json', 'w') as f_obj:
        json.dump(unit_dict_pass, f_obj)
    with open('aplanner-filepath.json', 'w') as f_obj:
        json.dump(f_path_pass, f_obj)


def format_display(unit_lst_pass2):
    display_lst = []
    for i in range(0, len(unit_lst_pass2)):
        spacer = ' '
        if len(unit_lst_pass2[i]) == 6:
            spacer = ''
        ptd = unit_dict[unit_lst_pass2[i]]['ptd']
        if 'pdn' in unit_dict[unit_lst_pass2[i]].keys():
            pdn = unit_dict[unit_lst_pass2[i]]['pdn']
        else:
            pdn = ''
        if 'pln' in unit_dict[unit_lst_pass2[i]].keys():
            pln = unit_dict[unit_lst_pass2[i]]['pln']
        else:
            pln = ''
        if 'nls' in unit_dict[unit_lst_pass2[i]].keys():
            nls = unit_dict[unit_lst_pass2[i]]['nls']
        else:
            nls = ''
        if 'fd' in unit_dict[unit_lst_pass2[i]].keys():
            fd = unit_dict[unit_lst_pass2[i]]['fd']
        else:
            fd = ''
        display_lst.append(f'{unit_lst_pass2[i]} {spacer} {ptd}    {pdn}    {pln}    {nls}    {fd}')
    return display_lst


def display_data_form(unit_lst_pass):
    layout_2 = [[sg.T('UNIT         PAID THRU           PDN                      PLN'),
                 sg.T('      NLS                      FD')],
                [sg.Listbox('', size=(800, 600), text_color='#32CD32', background_color='#1E1E1E',
                            font=('Courier', 10, 'bold'), key='_LISTBOX_')]]
    window_2 = sg.Window(" Jeff's Lien Sale Event Tracker", size=(800, 600), grab_anywhere=True,
                         auto_size_text=False, auto_size_buttons=False).Layout(layout_2).Finalize()
    window_2.Element('_LISTBOX_').Update(format_display(unit_lst_pass))
    while True:
        event_2, values_2 = window_2.Read(timeout=10)
        if event_2 is not None:
            continue
        else:
            break
    window_2.Close()


def update_pdn_lst(unit_lst_pass, unit_dict_pass):
    pdn_lst = []
    date_format = "%Y-%m-%d"
    # Strip new balances less than eight days old.
    for i in range(0, len(unit_lst_pass)):
        if 'pdn' not in unit_dict_pass[unit_lst_pass[i]].keys():
            a = datetime.strptime(unit_dict_pass[unit_lst_pass[i]]['ptd'], date_format)
            b = datetime.strptime(datetime.today().strftime('%Y-%m-%d'), date_format)
            delta = b - a
            if delta.days > 7:
                pdn_lst.append(unit_lst_pass[i])
    return pdn_lst


def update_pln_lst(unit_lst_pass, unit_dict_pass):
    pln_lst = []
    date_format = "%Y-%m-%d"
    # Strip new balances less than eight days old.
    for i in range(0, len(unit_lst_pass)):
        if 'pln' not in unit_dict_pass[unit_lst_pass[i]].keys():
            if 'pdn' in unit_dict_pass[unit_lst_pass[i]].keys():
                a = datetime.strptime(unit_dict_pass[unit_lst_pass[i]]['pdn'], date_format)
                b = datetime.strptime(datetime.today().strftime('%Y-%m-%d'), date_format)
                delta = b - a
                if delta.days > 16:
                    pln_lst.append(unit_lst_pass[i])
    return pln_lst


def update_nls_lst(unit_lst_pass, unit_dict_pass):
    nls_lst = []
    date_format = "%Y-%m-%d"
    # Strip new balances less than eight days old.
    for i in range(0, len(unit_lst_pass)):
        if 'nls' not in unit_dict_pass[unit_lst_pass[i]].keys():
            if 'pln' in unit_dict_pass[unit_lst_pass[i]].keys():
                a = datetime.strptime(unit_dict_pass[unit_lst_pass[i]]['pln'], date_format)
                b = datetime.strptime(datetime.today().strftime('%Y-%m-%d'), date_format)
                delta = b - a
                if delta.days > 16:
                    nls_lst.append(unit_lst_pass[i])
    return nls_lst


def update_fd_lst(unit_lst_pass, unit_dict_pass):
    fd_lst = []
    date_format = "%Y-%m-%d"
    # Strip new balances less than eight days old.
    for i in range(0, len(unit_lst_pass)):
        if 'fd' not in unit_dict_pass[unit_lst_pass[i]].keys():
            if 'nls' in unit_dict_pass[unit_lst_pass[i]].keys():
                a = datetime.strptime(unit_dict_pass[unit_lst_pass[i]]['nls'], date_format)
                b = datetime.strptime(datetime.today().strftime('%Y-%m-%d'), date_format)
                delta = b - a
                if delta.days > 30:
                    fd_lst.append(unit_lst_pass[i])
    return fd_lst


def date_convert(date_str_pass):
    return '20' + date_str_pass[-2:] + '-' + date_str_pass[:2] + '-' + date_str_pass[2:4]


if __name__ == '__main__':
    unit_lst, paidthru_lst, unit_dict, f_path = read_files()
    window = sg.Window(" Jeff's Lien Sale Event Tracker", size=(680, 460), default_element_size=(30, 1),
                       grab_anywhere=False, background_color='#1E1E1E', auto_size_text=False,
                       auto_size_buttons=False).Layout(layout).Finalize()
    window.Element('_PDN_LISTBOX_').Update(update_pdn_lst(unit_lst, unit_dict))
    window.Element('_PLN_LISTBOX_').Update(update_pln_lst(unit_lst, unit_dict))
    window.Element('_NLS_LISTBOX_').Update(update_nls_lst(unit_lst, unit_dict))
    window.Element('_FD_LISTBOX_').Update(update_fd_lst(unit_lst, unit_dict))
    window.Element('_PAST_DUE_COUNT_').Update(f'Number of past due accounts: {len(unit_lst)}')
    while True:
        event, values = window.Read(timeout=10)
        if event is None or event == 'Exit':
            break
        else:
            if event == 'About...':
                sg.Popup("Jeff's Lien Sale Event Tracker", 'This is a utility to help track legally required events',
                         'that lead to a self storage unit auction. It assures',
                         'the time interval between events adheres to requirements',
                         'of the Hawaii lien laws. When the program starts, it',
                         'searches for a specific Excel file that can be exported',
                         'from Sitelink. Sitelink is a popular operating software',
                         'for self storage. When event dates are marked, this',
                         'information is stored in a separate file. Obsolete records',
                         'are deleted automatically when the Excel file is read.\n',
                         'The program is not copyrighted and it is free for use.',
                         'Python source code for this is available in my public',
                         'GitHub repository.\n',
                         'Version 1.0 finished April 6, 2019.\n\n'
                         'Jeffrey Neil Willits', '@jnwillits\n', no_titlebar=True, keep_on_top=True,
                         grab_anywhere=True, background_color='#000000')
            elif event == 'Display Data':
                display_data_form(unit_lst)
            elif event == '_PDN_COMPLETE_TODAY_':
                unit_selected = values['_PDN_LISTBOX_'][0]
                unit_dict[unit_selected]['pdn'] = datetime.today().strftime('%Y-%m-%d')
                window.Element('_PDN_LISTBOX_').Update(update_pdn_lst(unit_lst, unit_dict))
                if values['_PDN_LISTBOX_'].count == 0:
                    continue
            elif event == '_PLN_COMPLETE_TODAY_':
                unit_selected = values['_PLN_LISTBOX_'][0]
                unit_dict[unit_selected]['pln'] = datetime.today().strftime('%Y-%m-%d')
                window.Element('_PLN_LISTBOX_').Update(update_pln_lst(unit_lst, unit_dict))
                if values['_PLN_LISTBOX_'].count == 0:
                    continue
            elif event == '_NLS_COMPLETE_TODAY_':
                unit_selected = values['_NLS_LISTBOX_'][0]
                unit_dict[unit_selected]['nls'] = datetime.today().strftime('%Y-%m-%d')
                window.Element('_NLS_LISTBOX_').Update(update_nls_lst(unit_lst, unit_dict))
                if values['_NLS_LISTBOX_'].count == 0:
                    continue
            elif event == '_FD_COMPLETE_TODAY_':
                unit_selected = values['_FD_LISTBOX_'][0]
                unit_dict[unit_selected]['fd'] = datetime.today().strftime('%Y-%m-%d')
                window.Element('_FD_LISTBOX_').Update(update_fd_lst(unit_lst, unit_dict))
                if values['_FD_LISTBOX_'].count == 0:
                    continue
            elif event == '_PDN_PAST_DATE_':
                date_str = sg.PopupGetText('Enter mmddyy...', '', size=(10, 50), background_color='#000000')
                unit_selected = values['_PDN_LISTBOX_'][0]
                unit_dict[unit_selected]['pdn'] = date_convert(date_str)
                window.Element('_PDN_LISTBOX_').Update(update_pdn_lst(unit_lst, unit_dict))
                window.Element('_PLN_LISTBOX_').Update(update_pln_lst(unit_lst, unit_dict))
                if values['_PDN_LISTBOX_'].count == 0:
                    continue
            elif event == '_PLN_PAST_DATE_':
                date_str = sg.PopupGetText('Enter mmddyy...', '', size=(10, 50), background_color='#000000')
                unit_selected = values['_PLN_LISTBOX_'][0]
                unit_dict[unit_selected]['pln'] = date_convert(date_str)
                window.Element('_PLN_LISTBOX_').Update(update_pln_lst(unit_lst, unit_dict))
                window.Element('_NLS_LISTBOX_').Update(update_nls_lst(unit_lst, unit_dict))
                if values['_PLN_LISTBOX_'].count == 0:
                    continue
            elif event == '_NLS_PAST_DATE_':
                date_str = sg.PopupGetText('Enter mmddyy...', '', size=(10, 50), background_color='#000000')
                unit_selected = values['_NLS_LISTBOX_'][0]
                unit_dict[unit_selected]['nls'] = date_convert(date_str)
                window.Element('_NLS_LISTBOX_').Update(update_nls_lst(unit_lst, unit_dict))
                window.Element('_FD_LISTBOX_').Update(update_fd_lst(unit_lst, unit_dict))
                if values['_NLS_LISTBOX_'].count == 0:
                    continue
            elif event == '_FD_PAST_DATE_':
                date_str = sg.PopupGetText('Enter mmddyy...', '', size=(10, 50), background_color='#000000')
                unit_selected = values['_FD_LISTBOX_'][0]
                unit_dict[unit_selected]['fd'] = date_convert(date_str)
                window.Element('_FD_LISTBOX_').Update(update_fd_lst(unit_lst, unit_dict))
                if values['_FD_LISTBOX_'].count == 0:
                    continue
    write_data(f_path, unit_dict)
    window.Close()
