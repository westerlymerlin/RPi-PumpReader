# https://sourceforge.net/p/raspberry-gpio-python/wiki/BasicUsage/

BCM = 11
BOARD = 10
OUT = 0
IN = 1
HIGH = 1
LOW = 0
ports = [0] * 40
PUD_UP = 1
PUD_DOWN = 0
RISING = 1
FALLING  = 0
BOTH = 2


def setmode(mode):
    print('Mode set is %s' % mode)


def setup(channel, direction, **kwarks):
    print('GPIO channels are set with a state of %s' % direction)


def output(channels, state):
    try:
        for channel in channels:
            ports[channel] = state
    except TypeError:
        ports[channels] = state
    print('GPIO Channel %s has been set to %s' % (channels, state))


def input(channel):
    return ports[channel]

def wait_for_edge(channel, edge, **kwargs):
    print('waitforedge channel = %s state = %s ' %(channel, edge))

def add_event_detect(channel, edge, **kwargs):
    print('add event detaect channel = %s state = %s ' %(channel, edge))

def cleanup():
    print('a')


def setwarnings(flag):
    print(flag)
