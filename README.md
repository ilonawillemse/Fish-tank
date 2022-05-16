# project-ilonawillemse

![Fish visualisation](doc/image/prototype.png)

## How to run

```
$ python3 fish.py
```


## Testing (not sure yet if i'm going to implement this because of time)

To test the implementation simply run `pytest` in the root folder of the project.

```
pytest
```

## General idea

```
Fish swim in a aquarium.
because of the swimming, the fish will get tired.
energy can be obtained by eating algea.
with energy fish can mate and bare children.

algea can grow with light strength.
algea get reduced by fish that eat algea.

the more fish, the less light, the less algea.

the less algea the less food for the fish, so no mating.

I might implement different male and female fish for the mating.

If possible I would like the fish to grow when they eat.

```

## libraries
numpy
matplotlib.pyplot to plot the data in an image
matplotlib.animation to visualize the animation
random to generate a random number to implement some chances
matplotlib
copy to copy some grids
pandas to transform some data for visualisation

# limitations that could come up
not being able to insert an image inside the animation instead of a square
not being able to let the fish grow


