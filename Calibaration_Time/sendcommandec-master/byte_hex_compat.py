## Add wrapper so I can print hex in a more readable format independently of the python version
## In more recent versions the .hex function already does what I wanted, but that is not the python3
## version available on centOS 7, so I needed to create a wrapper.
## When possible I still use the built-in function

from platform import python_version_tuple

if int(python_version_tuple()[0]) >= 3 and int(python_version_tuple()[1]) >= 8:
    def pretty_hex(value):
        return value.hex(' ', 2)
else:
    def pretty_hex(value):
        value = value.hex()
        return " ".join([ value[i:i+4] for i in range(0,len(value),4) ])
