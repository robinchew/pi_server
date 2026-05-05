import importlib.resources
import os
import sys
from time import sleep
import uuid

from flask import (
    Flask,
    request,
    make_response,
    Response as FlaskResponse
)
from gpiozero import LED

import static_files

try:
    from startup_config import default_headers
except ModuleNotFoundError:
    default_headers = {}

def Response(**kwargs):
    new_headers = kwargs.pop('headers', {})
    return FlaskResponse(
        **kwargs,
        headers={
            **default_headers,
            **new_headers,
        })

def DO_NOT_DEBUG_FOR_RASPBERRY_PI():
    '''
    Debug mode will not work if run as .pyz 
    or else you will get the following 'No module' error:

 * Serving Flask app 'run_server'
 * Debug mode: on
WARNING: This is a development server. Do not use it in a production deployment. Use a production WSGI server instead.
 * Running on all addresses (0.0.0.0)
 * Running on http://127.0.0.1:8080
 * Running on http://192.168.1.69:8080
Press CTRL+C to quit
 * Restarting with stat
/usr/bin/python: No module named run
    '''
    return False

app = Flask(__name__)

@app.route('/')
def index():
    user_id = request.cookies.get('user_id')
    is_new_user = user_id is None

    if not user_id:
        # If it doesn't exist, generate a unique ID
        user_id = str(uuid.uuid4())
    else:
        print(f"Returning visitor with ID: {user_id}")

    with open('/home/robin/gate_keepers.txt') as f:
        keeper_list = f.read().splitlines()

    if user_id in keeper_list:
        with (importlib.resources.files(static_files) / 'pi_index.html').open('rt') as f:
            # https://stackoverflow.com/questions/70764499/can-i-read-non-code-files-in-a-python-zip-archive
            #
            # TODO
            # Investigate: from jinja2 import PackageLoader
            resp = make_response(f.read())
    else:
        resp = make_response('<h1>' + user_id + '</h1>')

    if is_new_user:
        print(f"New visitor! Assigned ID: {user_id}")
        resp.set_cookie('user_id', user_id)

    return resp

if __name__ == '__main__':
    app.run(debug=True)

def page_404():
    return '404', 404

def on_off(pin_id, toggle_time):
    led = LED(pin_id)

    led.on()
    sleep(toggle_time)
    led.off()

    led.close() # This does seem to stop eventual gpiozero.exc.GPIOPinInUse error

def gpio_toggle_response(name, pin_id, toggle_time):
    on_off(pin_id, toggle_time)

    return Response(
        response=name + ' responded',
        headers=default_headers)

@app.route('/<string:path_name>')
def gpio_toggle_route(path_name):
    response_f, *args = {
        'gate': (gpio_toggle_response, path_name, 'GPIO23', 0.5),
        'garage': (gpio_toggle_response, path_name, 'GPIO18', 0.2),
    }.get(path_name, (page_404,))
    return response_f(*args)


def main():
    print('Path of __file__', os.path.abspath(__file__))
    try:
        port = int(sys.argv[1])
    except IndexError:
        port = 8000
    app.run(debug=DO_NOT_DEBUG_FOR_RASPBERRY_PI(), host='0.0.0.0', port=port)

if __name__ == '__main__':
    main()
