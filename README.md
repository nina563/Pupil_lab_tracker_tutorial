# Online tracking of the mapped gaze coordinates

In the `gaze_functions.py` file I am utilizing Pupil Labs' [real-time screen gaze mapping](https://github.com/pupil-labs/real-time-screen-gaze/tree/main) capabilities to map the user's gaze onto a screen surface defined by markers. The script generates marker images, creates a Tkinter canvas to display them, establishes a connection with a Pupil Labs device, and maps the user's gaze onto the defined surface.

`online_collecting_gaze.osexp` provides the same functionality but is realized for Opensesame. 

### Usage
To run the `gaze_functions.py` file: 
```
python main.py
```
### Unsolved Issues
The problem occurs in the begin() function when receiving the surface object from the updateSurface(gazeMapper) function. 
