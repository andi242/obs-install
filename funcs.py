import logging, json, requests, zipfile, io, shutil, re, os
from shutil import copyfile
import obsws_python as obs
from pathlib import Path

from obsws_python import reqs
# because https://github.com/aatikturk/obsws-python/issues/5


installFolder = "test"

def obs(obsUrl):
    global installFolder

    installFolder = input(f"set install folder (e.g. e:\obs) \n")
    logging.info(f"installing obs to: {installFolder}")
    r = requests.get(obsUrl)
    z = zipfile.ZipFile(io.BytesIO(r.content))
    z.extractall(installFolder)
    with open(f'{installFolder}/portable_mode.txt', 'w'): pass

def installBots(config):
    path_items = config.items( "bots" )
    for key, url in path_items:
        logging.info(f"{key}: {url}")
        r = requests.get(url)
        z = zipfile.ZipFile(io.BytesIO(r.content))
        z.extractall(installFolder + "/" + key)

def initSetup(config):
    globalIni = config.get('setup', 'globalconfig')
    input_file = Path(globalIni)
    logging.info(f"setup: {input_file}")
    output_file = Path(f"{installFolder}/config/obs-studio/global.ini")
    output_file.parent.mkdir(exist_ok=True, parents=True)
    copyfile(input_file, output_file)

def obsJsonSetup(config):
    configJson = "obs-config/config.json"
    cl = reqs.ReqClient(host='127.0.0.1', port=4455)
    resp = cl.send("GetVersion", raw=True)
    logging.info(f"OBS Version: {resp['obsVersion']}")
    with open(configJson) as conf:
        data = json.load(conf)
        print(data)
        for item in data:
            logging.info(f'request: {item["requestType"]}, {item["requestData"]}')
            try:
                cl.send(item["requestType"], data=item["requestData"], raw=True)
            except Exception as e:
                logging.error(e)
            finally:
                logging.info(f'request: {item["requestType"]} processed')

def getRelease(config):
    url = ""
    githubRelJson = config.get('obs', 'githubRelJson')
    resp = requests.get(githubRelJson).json()["assets"]
    pattern = re.compile("^OBS-Studio-.*.zip$")
    for item in resp:
        if pattern.match(item["name"]):
            logging.info(f'matched {item["name"]} with {item["browser_download_url"]}')
            url = item["browser_download_url"]
    if url == "":
        logging.info(f'download url not found!')
        exit(1)
    else:
        return url

def plugins(config):
    logging.info(f"installing plugins to: {installFolder}")
    path_items = config.items( "plugins" )
    for key, url in path_items:
        logging.info(f"{key}: {url}")
        r = requests.get(url)
        z = zipfile.ZipFile(io.BytesIO(r.content))
        z.extractall(f"{installFolder}/pluginsdl/{key}")
        output_file = Path(f"{installFolder}/install-log/{key}.txt")
        output_file.parent.mkdir(exist_ok=True, parents=True)
        logging.info(f"write install log for {key}")
        with open(output_file, "w") as myfile:
            for p in Path(f"{installFolder}/pluginsdl/{key}/").rglob( '*.*' ):
                myfile.write(str(p).replace( f'{installFolder}/pluginsdl/{key}/','' ) + '\n')
            myfile.close()
        shutil.rmtree(f"{installFolder}/pluginsdl")
        logging.info(f"install {key}")
        z.extractall(f"{installFolder}")

def localplugins(config):
    logging.info(f"installing plugins: {installFolder}")
    path_items = config.items( "locals" )
    for key, url in path_items:
        logging.info(f"{key}: {url}")
        z = zipfile.ZipFile("plugins/" + url)
        z.extractall(f"{installFolder}/pluginsdl/{key}")
        output_file = Path(f"{installFolder}/install-log/{key}.txt")
        output_file.parent.mkdir(exist_ok=True, parents=True)
        logging.info(f"write install log for {key}")
        with open(output_file, "w") as myfile:
            for p in Path(f"{installFolder}/pluginsdl/{key}/").rglob( '*.*' ):
                myfile.write(str(p).replace( f'{installFolder}/pluginsdl/{key}/','' ) + '\n')
            myfile.close()
        shutil.rmtree(f"{installFolder}/pluginsdl")
        logging.info(f"install {key}")
        z.extractall(f"{installFolder}")

def copyScripts(config):
    scriptsTarget = installFolder + "/data/obs-plugins/frontend-tools/scripts"
    scriptsFolder = config.get('setup', 'scriptspath')
    for file in os.listdir(scriptsFolder):
        logging.info(f"copy {file}")
        copyfile(scriptsFolder+"/"+file, scriptsTarget+"/"+file)