"""
This is the main flask application - called by Gunicorn
"""
import os
import subprocess
from threading import Timer
from flask import Flask, render_template, jsonify, request
from pumpclass import httpstatus, pressures
from logmanager import  logger
from app_control import settings, VERSION


app = Flask(__name__)
logger.info('Starting Pump Reader web app version %s', VERSION)
logger.info('Api-Key = %s', settings['api-key'])

def get_cpu_temperature():
    """Read CPU temperature"""
    with open(settings['cputemp'], 'r', encoding='utf-8') as f:
        log = f.readline()
    return round(float(log)/1000, 1)


def get_log_data(file_path):
    """Reads a file's lines and returns them in reverse order"""
    with open(file_path, 'r', encoding='utf-8') as f:
        lines = f.readlines()
    return list(reversed(lines))


@app.route('/')
def index():
    """Main web page handler, shows status page via the index.html template"""
    cputemperature = get_cpu_temperature()
    return render_template('index.html', pressures=httpstatus(), cputemperature=cputemperature,
                           version=VERSION)


@app.route('/api', methods=['POST'])
def api():
    """API Endpoint for programatic access - needs request data to be posted in a json file"""
    try:
        logger.debug('API headers: %s', request.headers)
        logger.debug('API request: %s', request.json)
        if 'Api-Key' in request.headers.keys():  # check api key exists
            if request.headers['Api-Key'] == settings['api-key']:  # check for correct API key
                item = request.json['item']
                if item == 'getpressures':
                    return jsonify(pressures()), 201
                if item == 'restart':
                    if request.json['command'] == 'pi':
                        logger.info('Restart command recieved: system will restart in 15 seconds')
                        timerthread = Timer(15, reboot)
                        timerthread.start()
                        return jsonify(pressures()), 201
                logger.warning('API: badly formed json message')
                return 'badly formed json message - item not found', 201
            logger.warning('API: access attempt using an invalid token from %s', request.headers[''])
            return 'access token(s) unuthorised', 401
        logger.warning('API: access attempt without a token from  %s', request.headers['X-Forwarded-For'])
        return 'access token(s) incorrect', 401
    except KeyError:
        return "badly formed json message", 201


@app.route('/pylog')
def showplogs():
    """Displays the application log file via the logs.html template"""
    cputemperature = get_cpu_temperature()
    logs = get_log_data(settings['logfilepath'])
    return render_template('logs.html', rows=logs, log='Pump Reader Application Log',
                           cputemperature=cputemperature, version=VERSION)

@app.route('/guaccesslog')
def showgalogs():
    """Displays the Gunicorn access log file via the logs.html template"""
    cputemperature = get_cpu_temperature()
    logs = get_log_data(settings['gunicornpath'] + 'gunicorn-access.log')
    return render_template('logs.html', rows=logs, log='gunicorn access log',
                           cputemperature=cputemperature, version=VERSION)

@app.route('/guerrorlog')
def showgelogs():
    """Displays the Gunicorn error log file via the logs.html template"""
    cputemperature = get_cpu_temperature()
    logs = get_log_data(settings['gunicornpath'] + 'gunicorn-error.log')
    return render_template('logs.html', rows=logs, log='gunicorn error log',
                           cputemperature=cputemperature, version=VERSION)


@app.route('/syslog')  # display the raspberry pi system log
def showslogs():
    """Displays the last 200 lines of the system log via the logs.html template"""
    with open(settings['cputemp'], 'r', encoding='utf-8') as f:
        log = f.readline()
    f.close()
    cputemperature = round(float(log)/1000, 1)
    log = subprocess.Popen('journalctl -n 200', shell=True,
                           stdout=subprocess.PIPE).stdout.read().decode(encoding='utf-8')
    logs = log.split('\n')
    logs.reverse()
    return render_template('logs.html', rows=logs, log='System Log',
                           cputemperature=cputemperature, version=VERSION)


def reboot():
    """Reboots the Raspberry Pi"""
    logger.warning('System is restarting now')
    os.system('sudo reboot')


if __name__ == '__main__':
    app.run()
