import importlib.resources
import os
import sys
from time import sleep

from flask import Flask, Response
from gpiozero import LED

import static_files 



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
def hello_world():
    with (importlib.resources.files(static_files) / 'pi_index.html').open('rt') as f:
        # https://stackoverflow.com/questions/70764499/can-i-read-non-code-files-in-a-python-zip-archive
        return f.read()

def page_404():
    return '404', 404

def on_off(pin_id, toggle_time):
    led = LED(pin_id)

    led.on()
    sleep(toggle_time)
    led.off()

def gpio_toggle_response(name, pin_id, toggle_time):
    on_off(pin_id, toggle_time)

    return Response(
        name + ' responded',
        headers={
            'Access-Control-Allow-Origin': '*'
        })

@app.route('/<string:path_name>')
def gpio_toggle_route(path_name):
    response_f, *args = {
        'gate': (gpio_toggle_response, path_name, 'GPIO23', 0.4),
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
