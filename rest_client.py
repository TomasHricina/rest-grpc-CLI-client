#!/usr/bin/env python

import requests
import sys
import simplejson

def check_if_port_already_in_url(_url):
    while _url.endswith('/'):
        _url = _url[:-1]
    if ':' in _url:
        possible_port = _url.split(':')[-1]
        try:
            port = int(possible_port)
        except ValueError:
            port = ''
        finally:
            return str(port)

def prepare_url(base, uuid, subcommand, port=None):
    _base = base
    if not base.startswith('http://') and not base.startswith('https://'):
        _base = 'http://'+ base
    _port = check_if_port_already_in_url(base)
    if _port:
        _port = ''
    else:
        if port:
            _port = ':'+str(port)
    
    _subcommand = subcommand.replace('/','')
    while _base.endswith('/'):
        _base = _base[:-1]
    _base += _port+'/file/'+uuid+'/'+_subcommand+'/'
    return _base

def rest_api_client(_url, _uuid, _subcommand, port=None):
    if '/file/' not in _url:
        url = prepare_url(_url, _uuid, _subcommand, port)
    else:
        url = _url
    print('Connecting to: ', url)
    print()
    try:
        response = requests.get(url, timeout=3)
    except requests.exceptions.HTTPError as ex:
        return ex
    except requests.ConnectionError as ex:
        return ex
    except requests.exceptions.Timeout as ex:
        return ex
    except requests.exceptions.RequestException as ex:
        return ex

    if 'stat' == _subcommand:
        try:
            _json = response.json()
            required_fields = 'create_datetime', 'size', 'mimetype', 'name'
            if set(_json.keys()) == set(required_fields):
                return _json
            else:
                return 404

        except simplejson.JSONDecodeError:
            return 404
    elif 'read' == _subcommand:
        try:
            return {'Content-Type': response.headers['Content-Type'],
                'Content-Disposition': response.headers['Content-Disposition']}
        except KeyError:
            return 404
