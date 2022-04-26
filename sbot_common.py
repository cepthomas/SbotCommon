import sys
import os
import pathlib
import sublime
import sublime_plugin


#-----------------------------------------------------------------------------------
def slog(cat, message=''):
    ''' Format a standard message with caller info and print it.
    If installed, it will route to sbot_logger via print().
    Note that cat should be four chars or less.
    '''
    
    # Check cat.
    cat = (cat + '____')[:4]

    # Get caller info.
    frame = sys._getframe(1)
    fn = os.path.basename(frame.f_code.co_filename)
    func = frame.f_code.co_name
    line = frame.f_lineno
    # mod_name = frame.f_globals["__name__"]

    full_func = ''
    try:
        class_name = frame.f_locals['self'].__class__.__name__
        full_func = f'{class_name}.{func}'
    except KeyError:
        full_func = func

    # Print to console or sbot_logger if installed.
    print(f'{cat} {full_func}() {fn}:{line} {message}')


#-----------------------------------------------------------------------------------
def get_store_fn(explicit_file_path, fn):
    ''' General utility to get store simple file name. '''
    store_path = None
    if explicit_file_path is None or len(explicit_file_path) == 0:
        store_path = os.path.join(sublime.packages_path(), 'User', 'SbotStore')
    else:
        store_path = explicit_file_path
        
    pathlib.Path(store_path).mkdir(parents=True, exist_ok=True)
    store_fn = os.path.join(store_path, fn)
    return store_fn


#-----------------------------------------------------------------------------------
def get_store_fn_for_project(explicit_file_path, project_fn, file_ext):
    ''' General utility to get store file name based on ST project name. '''
    project_fn = os.path.basename(project_fn).replace('.sublime-project', file_ext)
    store_fn = get_store_fn(explicit_file_path, project_fn)


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
