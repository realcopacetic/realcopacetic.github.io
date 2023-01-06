#!/usr/bin/python
# coding: utf-8


import xbmc
import xbmcaddon
import xbmcgui
import xbmcplugin
import json
import sys

ADDON = xbmcaddon.Addon()
ADDON_ID = ADDON.getAddonInfo('id')
DEBUG = xbmc.LOGDEBUG
DIALOG = xbmcgui.Dialog()
VIDEOPLAYLIST = xbmc.PlayList(xbmc.PLAYLIST_VIDEO)
MUSICPLAYLIST = xbmc.PlayList(xbmc.PLAYLIST_MUSIC)


def log(message):
    xbmc.log(f'{ADDON_ID} --> {message}', DEBUG)


def log_and_execute(action):
    log(f'EXECUTE {action}')
    xbmc.executebuiltin(action)


def condition(condition):
    return xbmc.getCondVisibility(condition)


def clear_playlists():
    log('CLEAR PLAYLISTS')
    VIDEOPLAYLIST.clear()
    MUSICPLAYLIST.clear()


def get_joined_items(item):
    if len(item) > 0 and item is not None:
        item = ' / '.join(item)
    else:
        item = ''

    return item


def json_call(method, properties=None, sort=None, query_filter=None, limit=None, params=None, item=None, options=None, limits=None, debug=False):
    json_string = {'jsonrpc': '2.0', 'id': 1, 'method': method, 'params': {}}

    if properties is not None:
        json_string['params']['properties'] = properties

    if limit is not None:
        json_string['params']['limits'] = {'start': 0, 'end': int(limit)}

    if sort is not None:
        json_string['params']['sort'] = sort

    if query_filter is not None:
        json_string['params']['filter'] = query_filter

    if options is not None:
        json_string['params']['options'] = options

    if limits is not None:
        json_string['params']['limits'] = limits

    if item is not None:
        json_string['params']['item'] = item

    if params is not None:
        json_string['params'].update(params)

    jsonrpc_call = json.dumps(json_string)
    result = xbmc.executeJSONRPC(jsonrpc_call)
    result = json.loads(result)

    if debug:
        log('--> JSON CALL: ' + json_prettyprint(json_string))
        log('--> JSON RESULT: ' + json_prettyprint(result))

    return result


def json_prettyprint(string):
    return json.dumps(string, sort_keys=True, indent=4, separators=(',', ': '))


def set_plugincontent(content=None, category=None):
    if category:
        xbmcplugin.setPluginCategory(int(sys.argv[1]), category)
    if content:
        xbmcplugin.setContent(int(sys.argv[1]), content)


def window_property(key, set_property=False, clear_property=False, window_id=10000):
    window = xbmcgui.Window(window_id)

    if clear_property:
        window.clearProperty(key)
        log(f'CLEARPROPERTY {window_id}, {key}')
    if set_property:
        window.setProperty(key, f'{set_property}')
        log(f'SETPROPERTY {window_id}, {key}, {set_property}')
