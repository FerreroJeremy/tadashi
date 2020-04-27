# Tadashi

**Tadashi is a context-aware deep decision system for smart home.**

The project is currently in beta.
Pull requests, feedbacks and suggestions are welcome!

### What is it?

This project is closely modelled on the <a rel="arcades" href="https://gricad-gitlab.univ-grenoble-alpes.fr/brenona/arcades">ARCADES</a> project of my former colleague <a rel="alexis" href="https://github.com/AlexisBRENON">Alexis Brenon</a>.
I invite you to read the <a rel="hal" href="https://hal.archives-ouvertes.fr/hal-01829401">ARCADES paper</a>.
Please cite this paper if you need to refer to Tadashi.

If you understand French and if you are really interested by his work, I recommend you to read his <a rel="thesis" href="https://tel.archives-ouvertes.fr/tel-01818123">thesis</a>.

### What does Tadashi mean?

<p align="left"><img width="500px" src="https://media.comicbook.com/2015/09/tadashiageofultron-151099.png"></p>

> "In preparation for the Battle of Sokovia against Ultron, Tony Stark sifted through a collection of U.I. chips to select one that would replace J.A.R.V.I.S., whose matrices had been uploaded into the Vision. One chip seen was labelled "T.A.D.A.S.H.I.", however, he instead chose F.R.I.D.A.Y. [...] T.A.D.A.S.H.I. is a reference to the film Big Hero 6, where the robotic member of the titular team, Baymax, has its A.I. program stored in a chip labeled with the name of his creator, Tadashi Hamada."

― <a rel="mcuf" href="https://marvelcinematicuniverse.fandom.com/wiki/T.A.D.A.S.H.I.">Marvel Cinematic Universe Fandom</a>

### How it works?

#### Overview

<p align="center"><img src="https://github.com/FerreroJeremy/tadashi/blob/master/doc/component_diagram.png"></p>

When executed, the script launch a `PeriodicallyProcessor` that runs every `TIME_BETWEEN_TWO_PROCESS` seconds (5 seconds by default).
The course of the proceedings is explain in more detail below.

This assume that your home automation system -provider- is <a rel="fibaro" href="https://www.fibaro.com">Fibaro</a>.

#### Fibaro sensors

Firstly, a call to <a rel="fibaro_api" href="https://manuals.fibaro.com/knowledge-base-browse/rest-api/">Fibaro API</a> is carried out to ensure the gathering of all data about the sensors.
The auth info are in a config `yaml` file in the `config` folder of Fibaro module.

Then, the collected data are refactored in more human friendly python objects, more exactly a `History` and a `TadashiHistory` object.
Respectively, on the one hand, a list of `Device` objects, like:

```json
{
    "id": 12,
    "name": "lounge_motion_sensor",
    "roomID": 1,
    "type": "com.fibaro.FGMS001",
    "baseType": "com.fibaro.motionSensor",
    "value": "true",
    "batteryLevel": 100,
    "dead": "false",
    "timestamp": 1561315055.685408
}
```

And on the other hand, a list of `Room` objects (aggregated device/sensor data by room):

```json
{
    "place": 1,
    "temperature": 22.8,
    "light": true,
    "motion": true,
    "humidity": false,
    "gaz": 0,
    "door": 1,
    "shutter": 1,
    "noise": false
}
```

#### Map drawing

After, mapdrawing classes knowing the location of walls and sensors build a 256x256 pixel colorized SVG map of the home from the `TadashiHistory`, i.e. the list of the `Room` objects.

To charm you, I put below an example of generated map from sensor states:
<p align="center"><img width="300px" src="https://github.com/FerreroJeremy/tadashi/blob/master/doc/map.png"></p>

In the lower right corner, you can see (from left to right): the day of the week, the hour, whether it is day or night (here it is night), and the season (here it is winter). 
You can also see in the lower left corner a future feature, the context.
The context will be the activity do by the customer or the meta-state of the home, e.g. travelling, cooking, sleeping... and it will be useful to supply an additional information to the neural network.
The context can be passed in argument to the main script or can be setted in the config yaml file.
For now, the default context is set to `UNKNOWN` and does not appear on the map.

#### Linker

At every passage of the periodic process, the `Linker` compute the new action (new activated switch according sensors) and link it with the previous generated map (the map generated in the previous passage).
To perform that it compute the difference between the state *n* and the state *n-1* of the home.
A filter is provided to remove the switch/dimmer/controller to exclude of the prediction system.
You can only take into account some devices, by using the value of the `Sensor` enum in the `fibaroSnapshotManager.py` class.
By default, all the actuator device are take into account for prediction, and not the sensor devices.

This approach is based on the premise that in a home state *n-1* we want to automaticlly execute the command that led to the state *n*.
This postulate can be easily further improved, e.g. with multi-label classification.

#### Prediction

Thanks to a neural network (see below), the switch/dimmer/controller to (de)activate is predicted for a certain home state.
The corresponding command is finally executed through a Fibaro API call.

#### Monitoring

The monitoring module compute some alerting (e.g. the list of the devices with no more battery) and metrology (e.g. graphs with the most used and corrected sensors).
The metrology is a list of `Counter` objects, like:

```json
{
    "id": 12,
    "roomID": 1,
    "type": "com.fibaro.FGMS001",
    "baseType": "com.fibaro.motionSensor",
    "value": "true",
    "count": 19,
    "corrected": 4
}
```

The monitoring module also compute a graph with the most corrected predictions and the <a rel="matrix" href="https://en.wikipedia.org/wiki/Confusion_matrix">confusion matrix</a> of predictions.
This can be used later to integrate <a rel="reinforcement_learning" href="https://en.wikipedia.org/wiki/Reinforcement_learning">reinforcement learning</a> in the convolutional neural network as in <a rel="hal" href="https://hal.archives-ouvertes.fr/hal-01829401">ARCADES</a>.

<p align="center"><img width="900px" src="https://github.com/FerreroJeremy/tadashi/blob/master/doc/graphics.png"></p>

#### Deep learning

Once the mapping `[switch to activate - map]` list built by `Linker`, we can use this list to feed a convolutional neural network and learn a model.
In this way, when the home is in a certain state, the neural network can predict a command to execute.

The deep learning library uses is <a rel="keras" href="https://keras.io/">Keras</a>.
The convolutional network uses is the VGG, first introduced by <a rel="vgg" href="https://arxiv.org/pdf/1409.1556/">Simonyan and Zisserman (2014)</a> which was subsequently used in many projects winning numerous challenges in image recognition task.

After the model training, a graph is generated showing the loss and accuracy of the training.
<p align="center"><img width="500px" src="https://github.com/FerreroJeremy/tadashi/blob/master/doc/learning.png"></p>

Since the learning may take some time and doesn't have to be done frequently, it is not carried out at every passage of the periodic process, unlike the map, link and classification processing. 
It is performed independently by the script `train_network.py`.
If you want to do the learning automatically, you can change this in `tadashi.py`.
I invite you to take a look in `LockManager` too.

### How to use it?

1. Install all dependencies
```
make install
```
2. Launch Tadashi
```
make
```
3. In a second terminal, launch the learning script to build model
```
make learn
```
4. In a third terminal, launch the monitoring GUI (optional)
```
make overwatch
```

<p align="center"><img width="800px" src="https://github.com/FerreroJeremy/tadashi/blob/master/doc/monitoring_gui.png"></p>

### How adapt it to your home?

1. **Change the city of your home**
Tadashi uses the <a rel="astral" href="https://astral.readthedocs.io/en/latest/">Astral</a> library to know the time of sunrise and sunset of your location.
It uses it to make appear on the map if it is day or night.
This allows to supply additional information to the neural network.
By default, in the makefile, the city in args is Paris (the city supported by `Astral` closest to my actual location).

2. **Change the Map generation**
There is a good chance that your house is not architecturally identical to mine.
So, you will have to make some changes to make Tadashi work with your home.

    1. **Change a room**
You will have to redefine the walls and the sensor locations.
For this, you will have to directly modify the methods called in `*MapDrawer` classes.
For example, if you want to redefine the bathroom, you must play with the `BathroomMapDrawer` class.
Change the `(x, y)` tuple and the `width` and the `height` of the figure in the `draw_room_wall` method to change size and location of the walls.
Look at the <a rel="svgwrite" href="https://svgwrite.readthedocs.io/en/master/">svgwrite documentation</a> to learn how manipulate native svgwrite methods like `Rect` or `Line`.
For the sensors is easier, just change the `x` and `y` parameters of `draw_*_icon` methods in `draw_*_sensor` methods to change the location of the corresponding sensor.

    2. **Add a room**
Add a class corresponding to your room that inherits the parent `MapDrawer` class.
Override each of the necessary methods as do the other `*MapDrawer` classes (e.g. `LoungeMapDrawer`).
Override the `draw_room_wall` method to define the walls of the room, the `draw_*_sensor` methods to add sensors in the room, and so on.
Furthermore, when you add a room, you must define it into `Place` enum in the `room.py` model class.

    3. **Add a sensor**
Add a `draw_(your_sensor_name)_icon` method in the parent `MapDrawer` class.
And add a `draw_(your_sensor_name)_sensor` method in each `*MapDrawer` child classes where you want to include your new sensor.
Use the already existing `draw_*_icon` and `draw_*_sensor` methods to code the core of your methods and take a look at the <a rel="fa" href="https://pypi.org/project/fontawesome/">fontawesome library documentation</a> to choose the icon for your new sensor.
Furthermore, when you add a sensor, you must define it into `Sensor` enum in the `fibaroSnapshotManager.py` class.

3. **Other bigger changes**
Normally, if you use Fibaro in your smart home, the project is now ready and adapted to your home.
But, if you use another sensor provider, you should definitely refactor the whole `Fibaro` module and maybe modify the `Device` and `Room` objects too.
But, courage, if you know some things in Python, it shouldn't be too hard. I tried my best to do POO minimalist pythonic clean code.

Nothing to change in the neural network part, if the `Linker`'s output file is correct the learning will be correct too.

### Conception

<p align="center"><img src="https://github.com/FerreroJeremy/tadashi/blob/master/doc/class_diagram.png"></p>

The above UML class diagram was modeled with <a rel="staruml" href="http://staruml.io/">StarUML</a>.
The conception is faithful to the structure of the project, the classes are grouped by module, each of them dealing with a part of the project.
The classes imported from the Python Standard Library do not appear in the diagram (e.g. Exception).


### Dependencies

The list of the current dependencies can be found in the `requirements.txt` file, and is also available below.

- matplotlib 3.1.1
- svgwrite 1.3.1
- Keras 2.2.4
- fontawesome 5.7.2.post1
- opencv_python 4.1.0.25
- numpy 1.16.4
- requests 2.21.0
- pandas 0.24.2
- tensorflow 1.15.2
- pytz 2019.2
- CairoSVG 2.4.0
- astral 1.10.1
- scikit_learn 0.22.2.post1
- PyYAML 5.3.1
