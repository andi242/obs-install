import configparser
import logging, sys, os
from pathlib import Path

from funcs import initSetup, obsJsonSetup, getRelease, plugins, localplugins, obs, copyScripts, installBots

installFolder = "obs"

def main():
    logging.basicConfig(stream=sys.stdout, level=logging.INFO, format='[%(asctime)s] %(levelname)s - %(message)s',)
    logging.info("starting")
    config = configparser.ConfigParser()
    config.read(r'config.cfg')
    obsUrl = getRelease(config)
    obs(obsUrl)
    plugins(config)
    localplugins(config)
    initSetup(config)
    copyScripts(config)
    installBots(config)
    explorerInstallFolder = Path(installFolder + "\\bin\\64bit") 
    os.system(f"explorer.exe {explorerInstallFolder}")
    while True:
        print("Start the new OBS installation from its current folder now and press Enter to continue")
        user_input = input(f"install folder should open now\n")
        if user_input == "":
            break
    obsJsonSetup(config)

if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print("interrupted")
        pass
    except SystemExit:
        print("interrupted")
        pass
