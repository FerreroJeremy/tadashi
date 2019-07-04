# Tadashi

Tadashi is a context-aware deep decision system for smart home.

### What is it?

This project is closely modelled on the <a rel="arcades" href="https://gricad-gitlab.univ-grenoble-alpes.fr/brenona/arcades">ARCADES</a> project of my colleague <a rel="alexis" href="https://github.com/AlexisBRENON">Alexis Brenon</a>.
I invite you to read the <a rel="hal" href="https://hal.archives-ouvertes.fr/hal-01829401">ARCADES's paper</a>.
Please cite this paper if you use Tadashi.

If you speak French and if you are really interested by his work, I recommend you to read his <a rel="thesis" href="https://tel.archives-ouvertes.fr/tel-01818123">thesis</a>.

### What does Tadashi mean?

> "In preparation for the Battle of Sokovia against Ultron, Tony Stark sifted through a collection of U.I. chips to select one that would replace J.A.R.V.I.S., whose matrices had been uploaded into the Vision. One chip seen was labelled "T.A.D.A.S.H.I.", however, he instead chose F.R.I.D.A.Y. [...] T.A.D.A.S.H.I. is a reference to the film Big Hero 6, where the robotic member of the titular team, Baymax, has its A.I. program stored in a chip labeled with the name of his creator, Tadashi Hamada."

― <a rel="mcuf" href="https://marvelcinematicuniverse.fandom.com/wiki/T.A.D.A.S.H.I.">Marvel Cinematic Universe Fandom</a>

### How it works?

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
<p align="center"><img src="https://raw.githubusercontent.com/FerreroJeremy/tadashi/master/doc/map.png"></p>

You can see in the lower left corner a further feature, the context.
The context will be the activity do by the customer or the meta-state of the home, e.g. travelling, cooking, sleeping... and it will be useful to supply an additional information to the neural network.

#### Linker

At every passage of the script, the `Linker` compute the new action -new activated switch according sensors- and link it with the previous generated map (the map generated in the previous passage) to feed the neural network.
Starting from the premise that in a home state (context) n-1 we want to automaticlly execute the command that led to the state n.
This postulate can be easily improved further, e.g. multi-label classification.

#### Deep learning

Once the mapping list built by Linker we can use it to feed a neural network and learn a model.
Like that, when the home is in a certain context/state, the neural network can predict a command to execute.
The command is then executed through a Fibaro API call.

The learning is not carried out at each passage of the script, unlike the mapping and linking.
By default, it is done every 3 days after 3a.m.
You can change this in `tadashi.py`.
I invent you to take a look in `periodicallyProcessor.py`.

#### Monitoring

The monitoring module compute some alerting, like the list of the devices with no more battery, and metrology, like graphs with the most used sensors and the confusion matrice of model predictions.

The metrology is a list composed of `Counter` objects like:

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

3. **Add a sensor and Other bigger changes**
Normally, if you use Fibaro in your smart home, the script is now ready and adapted to your home.
But, if you use another sensor provider, you should definitely refactor the `FibaroSnapshotManager` class -API call- and probably the `Device` and `Room` objects.
And because the mapping, linking and monitoring depend on model objects, that depend on sensor provider and API call, you will need to change that too, so lot things in the end.
But, courage, if you know some things in Python, it shouldn't be too hard. I tried my best to do clean POO minimalist code.

Nothing to change in the neural network part, if the linker's file is correct the learning will be correct too, don't worry ;)

### Concept & Conception

<p align="center"><img src="https://raw.githubusercontent.com/FerreroJeremy/tadashi/master/doc/class_diagram.png"></p>
The above diagram was modeled with <a rel="staruml" href="http://staruml.io/">StarUML</a>.

### Dependencies

