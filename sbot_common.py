import sys
import os
import subprocess
import pathlib
import sublime
import sublime_plugin


#-----------------------------------------------------------------------------------
def log_message(cat, message=''):
    ''' Format a standard message and print it.
    It will go to sbot_logger if installed - but cat must be four chars or less. '''
    
    # Get caller info.
    # This is the fastest way per https://gist.github.com/JettJones/c236494013f22723c1822126df944b12
    frame = sys._getframe(1)
    fn = os.path.basename(frame.f_code.co_filename)
    func = frame.f_code.co_name
    line = frame.f_lineno

    # Fix cat.
    cat = (cat + '____')[:4]

    smsg = f'{cat} {func}() {fn}:{line} {message}'
    print(smsg)


# #-----------------------------------------------------------------------------------
def get_store_fn(explicit_file_path, project_fn, file_ext):
    ''' General utility to get store file name. '''
    store_path = None
    if explicit_file_path is None or len(explicit_file_path) == 0:
        store_path = os.path.join(sublime.packages_path(), 'User', 'SbotStore')
    else:
        store_path = explicit_file_path
        
    pathlib.Path(store_path).mkdir(parents=True, exist_ok=True)
    project_fn = os.path.basename(project_fn).replace('.sublime-project', file_ext)
    store_fn = os.path.join(store_path, project_fn)
    return store_fn


#-----------------------------------------------------------------------------------
def get_sel_regions(view, settings):
    ''' Function to get selections or optionally the whole view if sel_all is True.'''
    regions = []
    if len(view.sel()[0]) > 0:  # user sel
        regions = view.sel()
    else:
        if settings.get('sel_all'):
            regions = [sublime.Region(0, view.size())]
    return regions


#-----------------------------------------------------------------------------------
def create_new_view(window, text):
    ''' Creates a temp view with text. Returns the view.'''
    vnew = window.new_file()
    vnew.set_scratch(True)
    vnew.run_command('append', {'characters': text})  # insert has some odd behavior - indentation
    return vnew


# TODO probably need a better home for these:
#-----------------------------------------------------------------------------------
class SbotGeneralEvent(sublime_plugin.EventListener):
    ''' Listener for window events of interest. '''

    def on_selection_modified(self, view):
        ''' Show the abs position in the status bar. '''
        pos = view.sel()[0].begin()
        view.set_status("position", f'Pos {pos}')


#-----------------------------------------------------------------------------------
class SbotSplitViewCommand(sublime_plugin.WindowCommand):
    ''' Toggles between split file views. '''

    def run(self):
        window = self.window

        if len(window.layout()['rows']) > 2:
            # Remove split.
            window.run_command("focus_group", {"group": 1})
            window.run_command("close_file")
            window.run_command("set_layout", {"cols": [0.0, 1.0], "rows": [0.0, 1.0], "cells": [[0, 0, 1, 1]]})
        else:
            # Add split.
            sel_row, _ = window.active_view().rowcol(window.active_view().sel()[0].a)  # current sel
            window.run_command("set_layout", {"cols": [0.0, 1.0], "rows": [0.0, 0.5, 1.0], "cells": [[0, 0, 1, 1], [0, 1, 1, 2]]})
            window.run_command("focus_group", {"group": 0})
            window.run_command("clone_file")
            window.run_command("move_to_group", {"group": 1})
            window.active_view().run_command("goto_line", {"line": sel_row})

