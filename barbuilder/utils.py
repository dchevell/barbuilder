import subprocess
from urllib.parse import urlencode


def open_callback_url(action, **params):
    scheme = 'swiftbar://'
    clean_params = urlencode({k:v for k,v in params.items() if v is not None})
    url = f'swiftbar://{action}?{clean_params}'
    print(action, params, url)
    cmd = ['open', '-g', url]
    subprocess.run(cmd, capture_output=True, check=True)