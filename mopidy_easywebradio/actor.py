from __future__ import unicode_literals

import logging

from mopidy import backend
from mopidy.models import Ref
import os, json

import pykka



logger = logging.getLogger(__name__)


class EasyRadioBackend(pykka.ThreadingActor, backend.Backend):
    uri_schemes = ['easyradio']

    def __init__(self, config, audio):
        super(EasyRadioBackend, self).__init__()

        self.library = EasyRadioLibrary(self)


class EasyRadioLibrary(backend.LibraryProvider):
    root_directory = Ref.directory(uri='easyradio:root', name='Easy Radio')

    def __init__(self, backend):
        super(EasyRadioLibrary, self).__init__(backend)

    def browse(self, uri):

        logger.info('Browsing %s' % uri)
        radio_file  = os.path.join(os.path.dirname(__file__), 'sample_list.json')
        with open(radio_file) as data_file:
            data = json.load(data_file)

        result = []

        return result

    def refresh(self, uri=None):
        self.backend.tunein.reload()

    def lookup(self, uri):
        return []

