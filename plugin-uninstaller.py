
import configparser, re
import json
import logging, sys, os, shutil
from pathlib import Path, PurePath

def listPlugins(config):
    pluginLogs = config.get('main', 'installFolder') + "/install-log"
    dir_list = os.listdir(pluginLogs)
    logging.info("set one of these as $1 arg to uninstall")
    for item in dir_list:
        logging.info(f"found: {item.replace('.txt','')}")

def uninstPlugins(config, plugin):
    obsRoot = config.get('main', 'installFolder') + "/"
    pluginLogs = obsRoot + "install-log"
    logfile = pluginLogs + '/' + plugin + '.txt'
    logfile = Path(logfile)
    if logfile.is_file():
        logging.info(f"found {PurePath(logfile).stem}, reading.")
        with open(logfile, "r") as file:
            lines = file.readlines()
            for line in lines:
                line = line.replace("\n",'')
                file = Path(obsRoot + line)
                if file.is_file():
                    os.remove(file)
                    logging.info('removed ' + obsRoot + line)
                else:
                    logging.error(f"file not found: {obsRoot + line}")
    else:
        logging.error(f"file not found: {plugin}")
        return False
    os.remove(logfile)

def main():
    logging.basicConfig(stream=sys.stdout, level=logging.INFO, format='[%(asctime)s] %(levelname)s - %(message)s',)
    logging.info("starting")
    config = configparser.ConfigParser()
    config.read(r'config.cfg')
    if sys.argv[2:]:
        listPlugins(config)
    if sys.argv[1:]:
        logging.info(f"uinstalling {sys.argv[1]}")
        uninstPlugins(config,sys.argv[1])
    else:
        listPlugins(config)
        

if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print("stopped")
        pass
    except SystemExit:
        print("stopped")
        pass
