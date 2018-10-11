from cryptography.fernet import Fernet, base64, InvalidSignature, InvalidToken
import hashlib
from django.contrib.auth.hashers import make_password, PBKDF2PasswordHasher, BasePasswordHasher, get_random_string
import logging

log = logging.getLogger(__name__)
import requests


class JsonApi(object):

    @classmethod
    def get(cls, base_url, api_url):
        url = '{}{}'.format(base_url, api_url)
        data = {}
        response = None
        try:
            response = requests.get(url)
            response.raise_for_status()
            data = response.json()
        except Exception as exc:
            log.warning('GET failed: {} - {}'.format(url, exc))
            if response is not None and hasattr(response, 'content'):
                log.warning('RESPONSE {}'.format(response.content))
        finally:
            return data


    @classmethod
    def post(cls, base_url, api_url, data):
        url = '{}{}'.format(base_url, api_url)
        response_data = {}
        response = None
        try:
            response = requests.post(url, json=data)
            response.raise_for_status()
            if response.status_code == 201:
                log.info('Peer {} accepted block.'.format(base_url))
            if not len(response.content):
                if response.status_code == 304:
                    log.warning('Peer {}: unable to accept block.'.format(base_url))
            else:
                response_data = response.json()
        except Exception as exc:
            log.warning('POST failed: {} - {}'.format(url, exc))
            if response is not None and hasattr(response, 'content'):
                log.warning('RESPONSE {}'.format(response.content))
        finally:
            return response_data
