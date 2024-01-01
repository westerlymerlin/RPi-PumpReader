"""
This is the main flask application - called by Gunicorn
"""
import os
import subprocess
from threading import Timer
from flask import Flask, render_template, jsonify, request
from pumpclass import httpstatus, temperature, pressures, pyrometer
from logmanager import  logger
from settings import settings, VERSION


app = Flask(__name__)


@app.route('/')
def index():
    """Main web page handler, shows status page via the index.html template"""
    with open(settings['cputemp'], 'r', encoding='utf-8') as f:
        log = f.readline()
    f.close()
    cputemperature = round(float(log)/1000, 1)
    return render_template('index.html', pressures=httpstatus(), cputemperature=cputemperature, version=VERSION)


@app.route('/api', methods=['POST'])
def api():
    """API Endpoint for programatic access - needs request data to be posted in a json file"""
    try:
        item = request.json['item']
        if item == 'gettemperature':
            return jsonify(temperature()), 201
        if item == 'getpressures':
            return jsonify(pressures()), 201
        if item == 'resetmax':
            pyrometer.resetmax()
            return jsonify(pressures()), 201
        if item == 'laser':
            if request.json['command'] == "on":
                pyrometer.laseron()
            else:
                pyrometer.laseroff()
            return jsonify(temperature()), 201
        if item == 'restart':
            if request.json['command'] == 'pi':
                logger.info('Restart command recieved: system will restart in 15 seconds')
                timerthread = Timer(15, reboot)
                timerthread.start()
                return jsonify(pressures()), 201
        logger.warning('API: badly formed json message')
        return 'badly formed json message - item not found', 201
    except KeyError:
        return "badly formed json message", 201


@app.route('/pylog')
def showplogs():
    """Displays the application log file via the logs.html template"""
    with open(settings['cputemp'], 'r', encoding='utf-8') as f:
        log = f.readline()
    f.close()
    cputemperature = round(float(log)/1000, 1)
    with open(settings['logfilepath'], 'r', encoding='utf-8') as f:
        log = f.readlines()
    f.close()
    log.reverse()
    logs = tuple(log)
    return render_template('logs.html', rows=logs, log='Pump Reader Application Log', cputemperature=cputemperature, version=VERSION)


@app.route('/guaccesslog')
def showgalogs():
    """Displays the Gunicorn access log file via the logs.html template"""
    with open(settings['cputemp'], 'r', encoding='utf-8') as f:
        log = f.readline()
    f.close()
    cputemperature = round(float(log)/1000, 1)
    with open(settings['gunicornpath'] + 'gunicorn-access.log', 'r', encoding='utf-8') as f:
        log = f.readlines()
    f.close()
    log.reverse()
    logs = tuple(log)
    return render_template('logs.html', rows=logs, log='gunicorn access log', cputemperature=cputemperature, version=VERSION)


@app.route('/guerrorlog')
def showgelogs():
    """Displays the Gunicorn error log file via the logs.html template"""
    with open(settings['cputemp'], 'r', encoding='utf-8') as f:
        log = f.readline()
    f.close()
    cputemperature = round(float(log)/1000, 1)
    with open(settings['gunicornpath'] + 'gunicorn-error.log', 'r', encoding='utf-8') as f:
        log = f.readlines()
    f.close()
    log.reverse()
    logs = tuple(log)
    return render_template('logs.html', rows=logs, log='gunicorn error log', cputemperature=cputemperature, version=VERSION)


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
    return render_template('logs.html', rows=logs, log='System Log', cputemperature=cputemperature, version=VERSION)


def reboot():
    """Reboots the Raspberry Pi"""
    logger.warning('System is restarting now')
    os.system('sudo reboot')


if __name__ == '__main__':
    app.run()
