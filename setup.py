

from setuptools import setup

APP = ['to_do_list.py']  
DATA_FILES = []    

OPTIONS = {
    'argv_emulation': False,  
    'iconfile': 'todo.icns', 
    'packages': ['tkinter'],  
    'plist': {
      
        'CFBundleName': 'To Do List',
        'CFBundleDisplayName': 'To Do List',
        'CFBundleGetInfoString': "Kişisel Yapılacaklar Listesi Uygulaması",
        'CFBundleIdentifier': "com.kisisel.todolist",
        'CFBundleVersion': "1.0.0",
        'CFBundleShortVersionString': "1.0",
        'NSHighResolutionCapable': True, 
    }
}

setup(
    app=APP,
    name='To Do List',
    data_files=DATA_FILES,
    options={'py2app': OPTIONS},
    setup_requires=['py2app'],
)