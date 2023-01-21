import base64
import os
import pickle
import subprocess
from collections.abc import Callable
from pathlib import Path
from urllib.parse import urlencode
from typing import ParamSpec

PLUGIN_PATH = Path(os.environ.get('SWIFTBAR_PLUGIN_PATH', '.'))


P = ParamSpec('P')


def open_callback_url(scheme: str, path: str, **params: str | int | None) -> None:
    clean_params = urlencode({k:v for k,v in params.items() if v is not None})
    url = f'{scheme}://{path}?{clean_params}'
    cmd = ['open', '-g', url]
    subprocess.run(cmd, capture_output=True, check=True)


def refreshplugin() -> None:
    open_callback_url('swiftbar', 'refreshplugin', name=PLUGIN_PATH.name)


def refreshallplugins() -> None:
    open_callback_url('swiftbar', 'refreshallplugins')


def enableplugin() -> None:
    open_callback_url('swiftbar', 'enableplugin', name=PLUGIN_PATH.name)


def disableplugin() -> None:
    open_callback_url('swiftbar', 'disableplugin', name=PLUGIN_PATH.name)


def toggleplugin() -> None:
    open_callback_url('swiftbar', 'toggleplugin', name=PLUGIN_PATH.name)


def notify(**params: str | int | None) -> None:
    open_callback_url('swiftbar', 'notify', name=PLUGIN_PATH.name, **params)


def serialize_callback(callback: Callable[P, object], *args: P.args, **kwargs: P.kwargs) -> str:
    cb_byt = pickle.dumps((callback, args, kwargs))
    cb_b64 = base64.b64encode(cb_byt)
    cb_txt = cb_b64.decode('ascii')
    return cb_txt


def deserialize_callback(cb_txt: str) -> tuple[Callable[P, object], P.args, P.kwargs]:
    cb_b64 = cb_txt.encode('ascii')
    cb_byt = base64.b64decode(cb_b64)
    callback, args, kwargs = pickle.loads(cb_byt)
    return callback, args, kwargs
