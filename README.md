# project-ilona willemse fishtank
This code creates a situation that visualises a fishtank within an animation.

![Fish visualisation](doc/image/prototype.png)
```
The fish move can swim, reproduce and eat algea. Algea can expand it's population and appear randomly by chance.
```

## How to run

```
$ python3 fish.py
```

# General idea

- Fish
    - [x] swim in a fishtank.
    - [x] through swimming energy level goes down
    - [x] energy can be obtained by eating algea.
    - [x] with energy fish can mate and bare children.
    - [x] fish die when no more energy

- algea
    - [] can grow with light.
    - [x] number gets reduced by fish that eat algea.

- input
    - [] light strenght
    - [x] starting algea density
    - [x] starting number of fish

- [] the more fish, the less light, the less algea.
- [x] the less algea the less food for the fish, so no mating.

- optional
    - [] different male and female fish for mating.
    - [] different species of fish
    - [] fish grow when they eat.
    - [] different kinds of fish that only mate with the same species.
    - [] adding slides in which the user can change certain values.

- end goal
    - [] visualise how fish populations are influenced by light strength

## libraries
```
- numpy
- matplotlib.pyplot to plot the data in an image
- matplotlib.animation to visualize the animation
- random to generate a random number to implement some chances
- matplotlib
- copy to copy some grids
- pandas to transform some data for visualisation
- mesa 
- shutil 
- matplotlib.offsetbox
```

## limitations that could come up
- not being able to insert an image inside the animation instead of a square
- not being able to let the fish grow
- adding the slides can be tough
- because i cannot use plt.show() it will be hard to visualize the animation if i let it run forever

## inspiration
```
https://docplayer.nl/161846295-Agent-based-modeling-domein-r-computational-science.html

I'd like to implement 2 different fish species if possible
also i might add a male vs female componend
```
