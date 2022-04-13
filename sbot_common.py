import os
import subprocess
import sublime
import sublime_plugin



# In signet/highlight
# Decorator for tracing function entry.
def trace_func(func):
    def inner(ref, *args):
        print(f'FUN {ref.__class__.__name__}.{func.__name__} {args}')
        return func(ref, *args)
    return inner


# In signet/highlight _get_store_fn + , file_ext):
def get_store_fn(project_fn, file_ext):
    ''' General utility. '''
    
    store_path = os.path.join(sublime.packages_path(), 'User', 'SbotStore')
    pathlib.Path(store_path).mkdir(parents=True, exist_ok=True)
    project_fn = os.path.basename(project_fn).replace('.sublime-project', file_ext)
    store_fn = os.path.join(store_path, project_fn)
    return store_fn


# In clean/format/render _get_sel_regions + , mod_name) 'SbotClean'
def get_sel_regions(view, mod_name):
    ''' Function to get selections or optionally the whole view if sel_all is True.'''
    regions = []
    if len(view.sel()[0]) > 0:  # user sel
        regions = view.sel()
    else:
        settings = sublime.load_settings(f"{mod_name}.sublime-settings")
        if settings.get('sel_all'):
            regions = [sublime.Region(0, view.size())]
    return regions


# In format/sidebar _create_new_view
def create_new_view(window, text):
    ''' Creates a temp view with text. Returns the view.'''
    vnew = window.new_file()
    vnew.set_scratch(True)
    vnew.run_command('append', {'characters': text})  # insert has some odd behavior - indentation
    return vnew
