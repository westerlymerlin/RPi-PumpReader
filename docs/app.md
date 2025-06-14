# None

<a id="app"></a>

# app

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

<a id="app.os"></a>

## os

<a id="app.subprocess"></a>

## subprocess

<a id="app.Timer"></a>

## Timer

<a id="app.enumerate_threads"></a>

## enumerate\_threads

<a id="app.Flask"></a>

## Flask

<a id="app.render_template"></a>

## render\_template

<a id="app.jsonify"></a>

## jsonify

<a id="app.request"></a>

## request

<a id="app.httpstatus"></a>

## httpstatus

<a id="app.pressures"></a>

## pressures

<a id="app.logger"></a>

## logger

<a id="app.settings"></a>

## settings

<a id="app.VERSION"></a>

## VERSION

<a id="app.app"></a>

#### app

<a id="app.get_cpu_temperature"></a>

#### get\_cpu\_temperature

```python
def get_cpu_temperature()
```

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

<a id="app.threadlister"></a>

#### threadlister

```python
def threadlister()
```

Generates a list of active threads in the application.

This function enumerates all threads currently active in the application and
compiles a list of their names and native thread IDs. The resulting list can
be used for monitoring active threads and their associated data.

Returns:
    list: A list of lists, where each inner list contains the name and
    native ID of an active thread as [str, int].

<a id="app.get_log_data"></a>

#### get\_log\_data

```python
def get_log_data(file_path)
```

Reads log data from a file and returns the lines in reverse order. This function
opens the specified file, reads all lines into memory, and then returns them
as a list in reversed order.

Args:
    file_path (str): Path to the file containing the log data.

Returns:
    list[str]: A list of log lines in reversed order.

<a id="app.index"></a>

#### index

```python
@app.route('/')
def index()
```

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

<a id="app.api"></a>

#### api

```python
@app.route('/api', methods=['POST'])
def api()
```

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

<a id="app.showplogs"></a>

#### showplogs

```python
@app.route('/pylog')
def showplogs()
```

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

<a id="app.showgalogs"></a>

#### showgalogs

```python
@app.route('/guaccesslog')
def showgalogs()
```

Displays the Gunicorn access log file via the logs.html template

<a id="app.showgelogs"></a>

#### showgelogs

```python
@app.route('/guerrorlog')
def showgelogs()
```

Displays the Gunicorn error log file via the logs.html template

<a id="app.showslogs"></a>

#### showslogs

```python
@app.route('/syslog')
def showslogs()
```

Displays the Raspberry Pi system log, CPU temperature, and version information
formatted in an HTML template.

Retrieves the CPU temperature by reading a specified file, processes the
system logs using the 'journalctl' command, and renders a web page with
the logs and details.


Returns:
    Response: An assembled HTML response rendering the logs, CPU temperature,
    and version information on a web page.

<a id="app.reboot"></a>

#### reboot

```python
def reboot()
```

Initiates a system reboot by using a command through the operating system.

This function logs a warning message indicating that the system is restarting
and subsequently executes the system reboot command.

Raises:
    OSError: If the command execution fails for any reason (e.g., permission
    issues, unavailable system commands).

