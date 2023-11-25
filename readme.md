# obs install script in python

- download latest obs for windows
- install plugins from list
- install local zipped plugins
- configure obs for portable mode

## install

- install python 3.10 (higher should work as well)
- `pip install -r requirements.txt`
- edit [config.cfg](./config.cfg) if needed
- run `python installer.py`
- start OBS if prompted to install basic scene set from [config.json](./obs-config/config.json)

## uninstall plugins

- run `python plugin-uninstaller.py` to get the list of installed plugins
- run `python plugin-uninstaller.py <plugin-name>` to remove the plugin from install folder

> the install folder might need to be changed in [config.cfg](./config.cfg) if it has been moved

## todo

- install plugins only script
- gui perhaps? idk