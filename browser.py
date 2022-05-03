import undetected_chromedriver as webdriver
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.select import Select
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import os
import shutil
import json
import tempfile
import configparser
from functools import reduce

class ChromeWithPrefs(webdriver.Chrome):
    def __init__(self, *args, options=None, **kwargs):
        if options:
            self._handle_prefs(options)

        super().__init__(*args, options=options, **kwargs)

        # remove the user_data_dir when quitting
        self.keep_user_data_dir = False

    @staticmethod
    def _handle_prefs(options):
        if prefs := options.experimental_options.get("prefs"):
            # turn a (dotted key, value) into a proper nested dict
            def undot_key(key, value):
                if "." in key:
                    key, rest = key.split(".", 1)
                    value = undot_key(rest, value)
                return {key: value}

            # undot prefs dict keys
            undot_prefs = reduce(
                lambda d1, d2: {**d1, **d2},  # merge dicts
                (undot_key(key, value) for key, value in prefs.items()),
            )

            # create an user_data_dir and add its path to the options
            user_data_dir = os.path.normpath(tempfile.mkdtemp())
            options.add_argument(f"--user-data-dir={user_data_dir}")

            # create the preferences json file in its default directory
            default_dir = os.path.join(user_data_dir, "Default")
            os.mkdir(default_dir)

            prefs_file = os.path.join(default_dir, "Preferences")
            with open(prefs_file, encoding="latin1", mode="w") as f:
                json.dump(undot_prefs, f)

            # pylint: disable=protected-access
            # remove the experimental_options to avoid an error
            del options._experimental_options["prefs"]


def config_set():
        config = configparser.ConfigParser()
        
        if not config.has_section("PREFS"):
            config.add_section("PREFS")
            config.set("PREFS", "download.default_directory", "download_csv")
            config.set("PREFS", "proxies", "")
            config.set("PREFS","plugins.always_open_pdf_externally","True")

        with open("config_s.ini", 'w') as configfile:
            config.write(configfile)

def config_read():

    config = configparser.ConfigParser()		
    config.read("config_s.ini")
    prefs_section = config['PREFS']
    prefs = {"download.default_directory":prefs_section["download.default_directory"],
    "plugins.always_open_pdf_externally":prefs_section["download.default_directory"]}
    
    return prefs

if __name__ == '__main__':
    
    config_set()
    prefs = config_read()
    options = webdriver.ChromeOptions()
    options.add_experimental_option("prefs", prefs)

    # use the derived Chrome class that handles prefs
    driver = ChromeWithPrefs(options=options)
