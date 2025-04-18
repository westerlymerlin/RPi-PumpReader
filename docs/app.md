# Contents for: app

* [app](#app)
  * [os](#app.os)
  * [subprocess](#app.subprocess)
  * [Timer](#app.Timer)
  * [enumerate\_threads](#app.enumerate_threads)
  * [Flask](#app.Flask)
  * [render\_template](#app.render_template)
  * [jsonify](#app.jsonify)
  * [request](#app.request)
  * [httpstatus](#app.httpstatus)
  * [pressures](#app.pressures)
  * [logger](#app.logger)
  * [settings](#app.settings)
  * [VERSION](#app.VERSION)
  * [app](#app.app)
  * [get\_cpu\_temperature](#app.get_cpu_temperature)
  * [threadlister](#app.threadlister)
  * [get\_log\_data](#app.get_log_data)
  * [index](#app.index)
  * [api](#app.api)
  * [showplogs](#app.showplogs)
  * [showgalogs](#app.showgalogs)
  * [showgelogs](#app.showgelogs)
  * [showslogs](#app.showslogs)
  * [reboot](#app.reboot)

<a id="app"></a>

# app

This is the main flask application - called by Gunicorn

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

Read CPU temperature

<a id="app.threadlister"></a>

#### threadlister

```python
def threadlister()
```

List all threads in the application, used for debugging purposes only

<a id="app.get_log_data"></a>

#### get\_log\_data

```python
def get_log_data(file_path)
```

Reads a file's lines and returns them in reverse order

<a id="app.index"></a>

#### index

```python
@app.route('/')
def index()
```

Main web page handler, shows status page via the index.html template

<a id="app.api"></a>

#### api

```python
@app.route('/api', methods=['POST'])
def api()
```

API Endpoint for programatic access - needs request data to be posted in a json file

<a id="app.showplogs"></a>

#### showplogs

```python
@app.route('/pylog')
def showplogs()
```

Displays the application log file via the logs.html template

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

Displays the last 200 lines of the system log via the logs.html template

<a id="app.reboot"></a>

#### reboot

```python
def reboot()
```

Reboots the Raspberry Pi

