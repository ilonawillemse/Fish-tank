# project-ilona willemse fishtank
This code creates a situation that visualises a fishtank within an animation.

![Fish visualisation](doc/image/prototype.png)
```
The fish move like boids. The way the fish move influence other fish. or the fish will move randomly through the tank
```

## How to run

```
$ python3 fish.py
```

# General idea

- Fish
    - [] swim in a fishtank.
    - [] through swimming energy level goes down
    - [] energy can be obtained by eating algea.
    - [] with energy fish can mate and bare children.
    - [] fish die after a certain time stamp

- algea
    - [] can grow with light.
    - [] number gets reduced by fish that eat algea.

- input
    - [] light strenght
    - [] starting algea density
    - [] starting number of fish

- [] the more fish, the less light, the less algea.
- [] the less algea the less food for the fish, so no mating.

- optional
    - [] swim by boids model
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
- mesa ??
```

## limitations that could come up
- not being able to insert an image inside the animation instead of a square
- not being able to let the fish grow
- adding the slides can be tough
- boid model implementation
- because i cannot use plt.show() it will be hard to 
- visualize the animation if i let it run forever

## inspiration
```
https://docplayer.nl/161846295-Agent-based-modeling-domein-r-computational-science.html

also moving like boids was an inspiration bron

I'd like to implement 2 different fish species if possible
also i might add a male vs female componend
```
