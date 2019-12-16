# Real-time multi-object tracking with 1 or 2 markers in OptiTrack system
Tracking multiple objects with 2 reflective markers or even only 1 for each, computing positions and orientations. This program is for resolving the limitation of amount of rigid-body. 

### Tracking with two markers. 
Set two reflective markers on the top of your objects. Front - higher and Back - lower. The program would first cluster all the pairs to find objects, then determine the orientation by high-low pairs. Config 'maxDistance' in `config.ini` to edit the max distance between two points in a pair. 

Since all the objects on the map won't have a big change between frames, we can use this to track objects according to last frames. 

### Tracking with only one marker. 
Set only 1 marker at the top of each object, move all your objects by a few steps, then the program will record a few frames of data and use linear regression to find a approximate orientation for every object. 

The tracking is solved by the same method. 
### Usage 
`python client.py` or python `Client_1Point.py`

You can change IP addresses or ports in `config.ini`. 

Turn on/off functions in` config.ini`, set 'False' or 'True' to turn on/off functions, **only one of these three could be turned on** 

- print all the positions and orientations: `printData = True`

- print how many objects captured: `printObejctsCount = True`

- Print the frame rate: `printFramesCount = True` 

Send socket: `sendSocket = True`
