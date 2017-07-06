# Optitrack-Tracking
Tracking multiple objects with 2 reflective balls for each, computing positions and orientations.

## Usage 
`python client.py`

You can change IP addresses or ports in `config.ini`. 

Turn on/off functions in` config.ini`, set 'False' or 'True' to turn on/off functions, **only one of these three could be turned on** 

- print all the positions and orientations: `printData = True`

- print how many objects captured: `printObejctsCount = True`

- Print the frame rate: `printFramesCount = True` 

Send socket: `sendSocket = True`
