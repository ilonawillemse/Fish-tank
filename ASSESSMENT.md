<!-- things i like/proud of -->
- I'm  really proud of how my fishtank visualisation turned out and that i was able after all to include the live counting of fish and algea populations in a graph underneath the animation of the fishtank

- I really like how I finally was able to insert images of fish / algea inside my animation

- The floating part of my fish when they die i think is cool too.

- The balanced algea-fish relationship



<!-- how i cleaned up some parts -->
- I added some methods in order to return the counting of the fish and algea populations at once, this way i did not have to repeat my iterating over the grid for more than once.

- Also I limited the lines of code in the main by putting the visualisations inside some functions



<!-- biggest decisions -->
Some of the things I wanted to implement in my animation / agent model were: inserting an image of a fish to the grid for visualisation, live tracking of the fish/algea countings, on top of that live viewing this underneath the fishtank visualisation and giving my fish the oppertunity to grow.

At first I was not able to insert an image inside a gridpoint of matplotlib. I tried so much options to insert an image to the animation grid but nothing worked. I tried different approaches like some people tried on the internet but they did not work for me. For example, one approach only made my new 'picture' a close up from the real one instead of inserting it in a grid. When I decided to throw out my matplotlib aproach and changed it for the mesa visualisation this problem was fixed. By chosing for Mesa this implementation became more realistic.

I also tried visualising my fish and algea countings in the same gif as my fishtank but this was somehow very hard. I tried different approaches but everytime I got so close I got stuck and got really frustrated about it. This because I put a lot of effort and time in figuring this out. Saving images first and inserting them in a list and then making an animation with matplotlib did not work. Whenever I saved the pictures they got a PIL type and this was hard to visualise. I googled a lot but everything I found on the internet did not work for me. This problem was fixed too when I choose to try the Mesa visualisation.

At first I thought about letting my fish have the oppertunity to grow but this would be cumbersome by using matplotlib. I would have looked at the neighbour pixels and color them the same color but this was not the best way to go so I decided to postpone this implementation and I choose to fix my other implementations first. In the end when I already decided to settle for the Mesa visualisation all of a sudden this posibility for my fish to grow became more convenient.


<!-- hard life of having windows 10 -->
- Because I was unable to use plt.show(), the visualisation of the animation was hard since running it in an infinite loop was impossible and it took a long time to run a lot of iterations. I struggled with this problem a long time. I fixed it by choosing the mesa visualisation instead.