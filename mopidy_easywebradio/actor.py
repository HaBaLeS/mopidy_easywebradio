from __future__ import unicode_literals

import logging

from mopidy import backend
from mopidy.models import Ref
import os, json

import pykka

logger = logging.getLogger(__name__)


class EasyRadioBackend(pykka.ThreadingActor, backend.Backend):

    uri_schemes = ['easywebradio']

    def __init__(self, config, audio):
        super(EasyRadioBackend, self).__init__()
        webradio_json = config['easywebradio']['config_file']
        self.library = EasyRadioLibrary(self,webradio_json )


class EasyRadioLibrary(backend.LibraryProvider):

    root_directory = Ref.directory(uri='easywebradio:root', name='Easy Radio')

    def __init__(self, backend, webradio_json):
        super(EasyRadioLibrary, self).__init__(backend)
        self.webradio_json = webradio_json

    def browse(self, uri):

        radio_file = os.path.join(os.path.dirname(__file__), self.webradio_json)
        with open(radio_file) as data_file:
            data = json.load(data_file)

        result = []
        if "easywebradio:root" == uri:
            for cat in data:
                catref = Ref.directory(uri='easywebradio:category:/' +cat['category']['cat_name'], name=cat['category']['cat_name'])
                result.append(catref)
        else:
            for cat in data:
                if cat['category']['cat_name'] in uri:
                    for pls in cat['category']['stations']:
                        result.append(Ref.track(uri=pls['streamurl'], name=pls['name']))

        return result

    def refresh(self, uri=None):
        self.backend.tunein.reload()

    def lookup(self, uri):
        return []

