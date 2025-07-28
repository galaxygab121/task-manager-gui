from setuptools import setup

APP = ['main.py']
DATA_FILES = ['tasks.json', 'reminder_sound.mp3']
OPTIONS = {
    'argv_emulation': True,
    'iconfile': 'icon.icns',
    'packages': ['tkcalendar', 'playsound', 'ics'],
    'resources': ['tasks.json', 'reminder_sound.mp3'],
    'plist': {
        'CFBundleName': 'Task Manager',
        'CFBundleShortVersionString': '1.0.0',
        'CFBundleVersion': '1.0.0',
        'CFBundleIdentifier': 'com.gabrielle.taskmanager',
        'NSHighResolutionCapable': True
    }
}

setup(
    app=APP,
    data_files=DATA_FILES,
    options={'py2app': OPTIONS},
    setup_requires=['py2app'],
)





