import yaml
import os
import sys
from mylogger import logger
import actionhook

class Config:
    def __init__(self):
        config_file = os.getenv('SODALITE_CONFIG_PATH')
        try:
            with open(config_file) as f:
                # use safe_load instead load
                self.config = yaml.safe_load(f)
                self.actions = self.config['actions']
        except yaml.scanner.ScannerError:
            logger.exception("Error while parsing config file '{}'".format(config_file))
            raise

    # exension: string containing an extension (e.g.: 'txt')
    # returns: actionhook.ActionHooks object
    def get_actionmap(self):
        actionhooks = actionhook.ActionMap()
        actionhooks.dir = self.actions['dir']
        actionhooks.text = self.actions['text']

        customs = self.actions['custom']
        for custom_key in customs.keys():
            custom_entries = customs[custom_key]
            extensions = custom_entries['extensions']
            hooks = custom_entries['hooks']
            for extension in extensions:
                extension_dict = actionhooks.extensions.get(extension, {})
                extension_dict.update(hooks)
                actionhooks.extensions[extension] = extension_dict

        return actionhooks


