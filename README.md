# Tadashi

Tadashi is a context-aware deep decision system for smart home.

### What is it?

This project is closely modelled on the <a rel="arcades" href="https://gricad-gitlab.univ-grenoble-alpes.fr/brenona/arcades">ARCADES</a> project of my former colleague <a rel="alexis" href="https://github.com/AlexisBRENON">Alexis Brenon</a>.
I invite you to read the <a rel="hal" href="https://hal.archives-ouvertes.fr/hal-01829401">ARCADES paper</a>.
Please cite this paper if you use Tadashi.

If you understand French and if you are really interested by his work, I recommend you to read his <a rel="thesis" href="https://tel.archives-ouvertes.fr/tel-01818123">thesis</a>.

### What does Tadashi mean?

<p align="left"><img width="500px" src="https://media.comicbook.com/2015/09/tadashiageofultron-151099.png"></p>

> "In preparation for the Battle of Sokovia against Ultron, Tony Stark sifted through a collection of U.I. chips to select one that would replace J.A.R.V.I.S., whose matrices had been uploaded into the Vision. One chip seen was labelled "T.A.D.A.S.H.I.", however, he instead chose F.R.I.D.A.Y. [...] T.A.D.A.S.H.I. is a reference to the film Big Hero 6, where the robotic member of the titular team, Baymax, has its A.I. program stored in a chip labeled with the name of his creator, Tadashi Hamada."

― <a rel="mcuf" href="https://marvelcinematicuniverse.fandom.com/wiki/T.A.D.A.S.H.I.">Marvel Cinematic Universe Fandom</a>

### How it works?

#### Overview

<p align="center"><img src="https://github.com/FerreroJeremy/tadashi/blob/master/doc/component_diagram.png"></p>

#### Fibaro sensors

Firstly, a call to <a rel="fibaro_api" href="https://manuals.fibaro.com/knowledge-base-browse/rest-api/">Fibaro API</a> is carried out to ensure the gathering of all data about the sensors.
Then, the collected data are refactored in more human friendly python objects, more exactly a `History` and a `TadashiHistory` object.
Respectively, on the one hand, a list of `Device` objects, like:

```json
{
    "id": 1898,
    "name": "1897.0",
    "roomID": 0,
    "type": "com.fibaro.FGMS001",
    "baseType": "com.fibaro.motionSensor",
    "value": "true",
    "batteryLevel": 100,
    "dead": "false",
    "timestamp": 1561315055.685408
}
```

And on the other hand, a list of `Room` objects (aggregated device/sensor data by rooom):

```json
{
    "place": 0,
    "temperature": 2.0,
    "light": true,
    "motion": true,
    "humidity": true,
    "gaz": 2,
    "door": 1,
    "shutter": 1,
    "noise": true
}
```

#### Map drawing

After, a map of the home is built from the `TadashiHistory`, i.e. the list of the `Room` objects, with mapdrawing classes knowing the location of walls and sensors.

To charm you, I put below an example of generated map from sensor states:
<p align="center"><img width="300px" src="https://github.com/FerreroJeremy/tadashi/blob/master/doc/map.png"></p>

You can see in the lower left corner a future feature, the context.
The context will be the activity do by the customer or the meta-state of the home, e.g. travelling, cooking, sleeping... and it will be useful to supply an additional information to the neural network.

#### Linker

At every passage of the script, the `Linker` compute the new action -new activated switch according sensors- and link it with the previous generated map (the map generated in the previous passage) to feed the neural network.
Starting from the premise that in a home state n-1 we want to automaticlly execute the command that led to the state n.
This postulate can be easily further improved, e.g. multi-label classification.

#### Deep learning

Once the mapping [switch to activate - map] list built by `Linker` we can use it to feed a convolutional neural network and learn a model.
Like that, when the home is in a certain state, the neural network can predict a command to execute.
The command is finally executed through a Fibaro API call.

The deep learning library uses is <a rel="keras" href="https://keras.io/">Keras</a>.
The convolutional network uses is the VGG, first introduced by <a rel="vgg" href="https://arxiv.org/pdf/1409.1556/">Simonyan and Zisserman (2014)</a> which was subsequently used in many projects winning numerous challenges in image recognition task.

After the model training, a graph is generated showing the loss and accuracy of the training.
<p align="center"><img width="500px" src="https://github.com/FerreroJeremy/tadashi/blob/master/doc/learning.png"></p>

The learning is not carried out at each passage of the script, unlike the mapping, linking and classification process.
By default, it is done every 3 days after 3a.m.
You can change this in `tadashi.py`.
I invite you to take a look in `periodicallyProcessor.py` too.

#### Monitoring

The monitoring module compute some alerting (e.g. the list of the devices with no more battery) and metrology (e.g. graphs with the most used sensors).
The metrology is a list composed of `Counter` objects, like:

```json
{
    "id": 2004,
    "roomID": 1,
    "type": "com.fibaro.FGMS001",
    "baseType": "com.fibaro.motionSensor",
    "value": "true",
    "count": 19,
    "corrected": 4
}
```

The monitoring module compute also a graph with the most corrected predictions and the confusion matrice of predictions.
This can be used later to integrate reinforcement learning in the convolutional neural network as in <a rel="hal" href="https://hal.archives-ouvertes.fr/hal-01829401">ARCADES</a>.

<p align="center"><img width="900px" src="https://github.com/FerreroJeremy/tadashi/blob/master/doc/graphics.png"></p>

### How adapt it to your home?

1. **Change the city of your home**
Tadashi uses the <a rel="astral" href="https://astral.readthedocs.io/en/latest/">Astral</a> library to know the time of sunrise and sunset of your location.
It uses it to make appear on the map if it is day or night.
This allows to supply additional information to the neural network.
By default, the city is Paris (the city supported by `Astral` closest to my actual location).
You can change it in `tadashi.py`.

2. **Change the Map generation**
There is a good chance that your house is not architecturally identical to mine.
You will have to make some changes to make Tadashi work with your home.

    1. **Change a room**
You will have to redefine the walls and the sensor locations.
For this, you will have to directly modify the methods called in `*MapDrawer` classes.
For exemple, if you want to redefine the bathroom, you must play with the `BathroomMapDrawer` class.
Change the `(x, y)` tuple and `width` and the `height` of the figure in the `draw_room_wall` method to change size and location of the walls.
Look at the <a rel="svgwrite" href="https://svgwrite.readthedocs.io/en/master/">svgwrite documentation</a> to learn how manipulate native svgwrite methods like `Rect` or `Line`.
For the sensors is easier, just change the `x` and `y` parameter of the `draw_*_icon` methods to change the location of the corresponding sensor.
Try it! It's cool, it's like drawing!

    2. **Add a room**
Add a class corresponding to your room that inherits the parent `MapDrawer` class.
Override each of the necessary methods as do the other `*MapDrawer` classes (e.g. `LoungeMapDrawer`).
Override the `draw_room_wall` method to define the walls of the room, the `draw_*_sensor` methods to add sensors in the room, and so on.

3. **Add a sensor and other bigger changes**
Normally, if you use Fibaro in your smart home, the script is now ready and adapted to your home.
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

- pytz==2018.9
- pandas==0.24.2
- imutils==0.5.2
- svgwrite==1.2.1
- numpy==1.16.4
- astral==1.10.1
- seaborn==0.9.0
- matplotlib==3.1.0
- Keras==2.2.4
- tensorflow=1.14
- fontawesome==5.7.2.post1
- scikit_learn==0.21.2

