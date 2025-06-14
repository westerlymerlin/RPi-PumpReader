# None

<a id="app_control"></a>

# app\_control

Settings module, reads the settings from a settings.json file. If it does not exist or a new setting
has appeared it will creat from the defaults in the initialise function.

<a id="app_control.random"></a>

## random

<a id="app_control.json"></a>

## json

<a id="app_control.datetime"></a>

## datetime

<a id="app_control.VERSION"></a>

#### VERSION

<a id="app_control.writesettings"></a>

#### writesettings

```python
def writesettings()
```

Write settings to json file

<a id="app_control.generate_api_key"></a>

#### generate\_api\_key

```python
def generate_api_key(key_len)
```

generate a new api key

<a id="app_control.initialise"></a>

#### initialise

```python
def initialise()
```

These are the default values written to the settings.json file the first time the app is run

<a id="app_control.readsettings"></a>

#### readsettings

```python
def readsettings()
```

Read the json file

<a id="app_control.loadsettings"></a>

#### loadsettings

```python
def loadsettings()
```

Replace the default settings with thsoe from the json files

<a id="app_control.settings"></a>

#### settings

