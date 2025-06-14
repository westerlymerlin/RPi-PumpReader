"""
Pump Reader Web Application

This Flask application serves as a web interface for monitoring and controlling
a pump system. It provides:

- A web dashboard showing real-time pump pressure readings and system status
- REST API endpoints for programmatic access to pump data and control functions
- System monitoring capabilities including CPU temperature and log viewing
- Remote system control functions (restart)

The application is designed to run on a Raspberry Pi using Gunicorn as the WSGI server.

Usage:
    - Run directly: python app.py (development)
    - Run with Gunicorn: gunicorn app:app (production)

Configuration is loaded from app_control.settings
"""
import os
import subprocess
from threading import Timer, enumerate as enumerate_threads
from flask import Flask, render_template, jsonify, request
from pumpclass import httpstatus, pressures
from logmanager import logger
from app_control import settings, VERSION


app = Flask(__name__)
logger.info('Starting Pump Reader web app version %s', VERSION)
logger.info('Api-Key = %s', settings['api-key'])


def get_cpu_temperature():
    """
    Reads the CPU temperature from a file specified in the settings and returns
    the temperature in Celsius, rounded to one decimal place.

    Raises
    ------
    FileNotFoundError
        If the file specified in settings['cputemp'] does not exist.

    ValueError
        If the temperature read from the file cannot be converted to a float.

    Returns
    -------
    float
        The CPU temperature in Celsius, rounded to one decimal place.
    """
    with open(settings['cputemp'], 'r', encoding='utf-8') as f:
        log = f.readline()
    return round(float(log)/1000, 1)


def threadlister():
    """
    Generates a list of active threads in the application.

    This function enumerates all threads currently active in the application and
    compiles a list of their names and native thread IDs. The resulting list can
    be used for monitoring active threads and their associated data.

    Returns:
        list: A list of lists, where each inner list contains the name and
        native ID of an active thread as [str, int].
    """
    appthreads =[]
    for appthread in enumerate_threads():
        appthreads.append([appthread.name, appthread.native_id])
    return appthreads


def get_log_data(file_path):
    """
    Reads log data from a file and returns the lines in reverse order. This function
    opens the specified file, reads all lines into memory, and then returns them
    as a list in reversed order.

    Args:
        file_path (str): Path to the file containing the log data.

    Returns:
        list[str]: A list of log lines in reversed order.
    """
    with open(file_path, 'r', encoding='utf-8') as f:
        lines = f.readlines()
    return list(reversed(lines))


@app.route('/')
def index():
    """
    Function that serves as the root endpoint for a web application. It collects various system
    metrics, including CPU temperature, HTTP status pressures, and the number of threads, and
    renders them along with the application version into an HTML template for display.


    Returns:
        str: Rendered HTML content of the 'index.html' template with the following parameters:
             - pressures: The current HTTP status pressures retrieved from the httpstatus function.
             - cputemperature: The current CPU temperature obtained from the get_cpu_temperature
               function.
             - version: The application version defined by the global variable VERSION.
             - threadcount: The total number of threads fetched from the threadlister function.
    """
    cputemperature = get_cpu_temperature()
    return render_template('index.html', pressures=httpstatus(), cputemperature=cputemperature,
                           version=VERSION, threadcount=threadlister())


@app.route('/api', methods=['POST'])
def api():
    """
    Handles API POST requests to perform various actions such as retrieving pressure data or
    restarting the system. Validates the API key present in the request headers to ensure
    authorized access.


    Returns:
        Response object with JSON data or a string message indicating success, failure, or
        an error. The HTTP status code is also included in the response. The content of the
        response depends on the provided 'item' in the request data and the validity of the
        API key.

    Raises:
        KeyError: If the required 'item' or 'command' keys are missing from the
        request payload.
    """
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
            logger.warning('API: access attempt using an invalid token from  %s', request.headers['X-Forwarded-For'])
            return 'access token(s) unuthorised', 401
        logger.warning('API: access attempt without a token from  %s', request.headers['X-Forwarded-For'])
        return 'access token(s) incorrect', 401
    except KeyError:
        logger.warning('API: badly formed json message')
        return "badly formed json message", 201


@app.route('/pylog')
def showplogs():
    """
    Handles the '/pylog' route to display log data and system information.

    This function retrieves CPU temperature and log data, then renders an HTML
    template to display the logs along with additional system information such
    as the application's version and current CPU temperature.

    Returns:
        flask.Response: A rendered HTML response displaying the log data, application
                        name, CPU temperature, and version.

    Raises:
        No explicit exceptions are raised by this function, but exceptions may
        propagate from `get_cpu_temperature`, `get_log_data`, or `render_template`.

    """
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
    """
    Displays the Raspberry Pi system log, CPU temperature, and version information
    formatted in an HTML template.

    Retrieves the CPU temperature by reading a specified file, processes the
    system logs using the 'journalctl' command, and renders a web page with
    the logs and details.


    Returns:
        Response: An assembled HTML response rendering the logs, CPU temperature,
        and version information on a web page.
    """
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
    """
    Initiates a system reboot by using a command through the operating system.

    This function logs a warning message indicating that the system is restarting
    and subsequently executes the system reboot command.

    Raises:
        OSError: If the command execution fails for any reason (e.g., permission
        issues, unavailable system commands).
    """
    logger.warning('System is restarting now')
    os.system('sudo reboot')


if __name__ == '__main__':
    app.run()
