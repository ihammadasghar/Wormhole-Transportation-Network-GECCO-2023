# Wormhole-Transportation-Network-GECCO-2023
This challenge is part of the SpOC (Space Optimisation Challenge) hosted by ESA's Advanced Concepts Team in partnership with GECCO 2023.

## Description
In the distant future, the dream of humankind to travel among the stars is about to become reality. The discovery of a habitable planet (called New Mars) with a breathable oxygen-nitrogen atmosphere orbiting Proxima Centauri is followed by an even more stunning discovery of a cluster of black holes close to the Solar System. The exciting part is that the black holes seem to be supporting a stable wormhole to distant corners of the Milky Way. Was it built by an unknown and unimaginably powerful alien civilisation, or is it a natural phenomenon? We may never know, but this does not stop us from preparing for the adventure of our life - the exploration of the newly discovered planet is finally within reach!

Twelve ships designed to withstand the colossal strain associated with traversing a wormhole are constructed and dispatched to the new planet via the wormhole network. The ships are dispatched together in order to avoid any surprises and delays, but it turns out that navigating a wormhole network is a lot more treacherous than anticipated: upon entering the region with the black holes, the twelve ships are quickly separated and pulled in different directions! Now each ship is facing the prospect of navigating the network on its own. Danger, Will Robinson!

To make matters worse, the effects of being close to an event horizon are already being felt: time is flowing at a different pace for each ship! What had started as a synchronised fleet is now at risk of being pulled apart further and further in time until they can no longer rendezvous at Proxima.

Luckily, every cloud has a silver lining: the physical properties of each black hole induce specific tension in the space-time continuum, which translates into a probabilistic temporal offset with a characteristic mean and variance for each wormhole associated with it. Importantly, the mean temporal offsets can also be negative - in other words, the wormholes can send the ships back in time! The twelve ships have the opportunity to harness these temporal offsets in order to arrive at their destination within a given temporal window with minimal uncertainty (variance).

The arrival time for each ship is relative: it is the sum of the initial delay induced by the event horizon and the means of the temporal offsets of all wormholes that it traverses along the way (so negative means subtract time from the ship's arrival time). The variances are unfortunately all positive. This gives the ships lots of opportunities to make sure that they can fit within the specified temporal window, but they have to minimise the uncertainty.

While the quantum computers onboard the ships provide a pretty accurate estimate of the distribution of means and variances throughout the wormhole network, they are still unable to provide a feasible path through the network. With your expertise, the fleet still has a chance to make it all the way to Proxima unscathed!

Of course, there is one important detail that we saved for last: although the ships are designed to withstand the stress of traversing a wormhole, they still suffer minor damage each time they dip below the event horizon. To guarantee the structural integrity of the ships, you must make sure that each ship navigates to the destination within a certain number of hyperspace jumps.

Help find a feasible way through the wormhole network and save our intrepid adventurers from a fate of being forever lost in the mists of time!

## N.B.
In addition, diving under the event horizon of a black hole perturbs the space-time continuum, and therefore all wormholes connected to that black hole incur a multiplicative increase in temporal variance. In practical terms, this means that subsequent revisits to a black hole with any ship will result in an exponentially larger cost.

## Data
We provide a database in the form of a compressed numpy archive named database.npz. It contains the necessary data to define a sparse directed network with 10000 nodes and 1998600 edges, as well as the initial conditions of the problem. In the context of the challenge, the nodes represent black holes and the edges represent wormholes. If an edge exists from node 
�
a to node 
�
b, this does not imply that there is an edge from 
�
b to 
�
a.

More specifically, the database contains the following entries:

### edges: 1998600 pairs of integers defining the edges of the network:
Source node	Target node
1	101
1	102
...	...
8374	9919
### meanvar: 1998600 pairs of floating-point numbers representing mean and variance of each edge:
### Edge	Mean	Variance
1 -> 101	-0.00120978	0.00278519
1 -> 102	0.00139366	0.00206549
...	...	...
8374 -> 9919	0.00014143	0.00102509
In the context of the challenge, the mean is a relative temporal offset associated with traversing the wormhole, and the variance is a measure of the uncertainty thereof. In other words, when a ship traverses a wormhole, the mean of that wormhole is added to its 'subjective time'. Specifically, a negative mean implies that the wormhole is sending the ship backward in time.

### jump_limit: The maximum number of jumps that any ship is allowed to make through the wormhole network.

### window: The temporal window within which all ships must arrive at the destination.

### origins: The IDs of the nodes that ships (in that order) are allowed to use as entry points to the wormhole network.

### destination: The ID of the node where all ships must rendezvous.

### delays: A list containing the initial temporal offsets of ships in that order.


## Utilities / Hints
Have a detailed look at the User Defined Problem (UDP) accessible under Evaluation code to understand how the evaluation works.

This problem has a single objective (cf. Objective). Please submit the decision vector for the decisionVector key of the JSON submission file:

[
    {
            "decisionVector": x,
            "problem": "wormhole-transportation-network",
            "challenge": "spoc-2-wormhole-transportation-network",
    }
]
To decode the information from a decision vector x into a summary printed on screen, call the .pretty(x) method.

Basic plots for solution visualisation purposes can be obtained by calling the .plot(x) method of the UDP.

A NumPy array containing an example chromosome can be uncompressed with the .example() method of the UDP and passed to the fitness() function for evaluation. Please note that this solution corresponds to a minimal working example and should not be taken as a baseline for what a competitive score should be.

For any decision vector x, the vector containing the fitness value and the equality and inequality constraint violations can be retrieved by using the .fitness() method of the UDP.

Keep in mind that the means of the wormholes can be negative, so ships can compensate for their initial delays by going not only forward, but also backward in time.

Submitting your solution to Optimise
To submit a solution (a chromosome), you can prepare a submission file by using the submission helper via

from submisson_helper import create_submission
create_submission("spoc-2-wormhole-transportation-network","wormhole-transportation-network",x,"submission_file.json","submission_name","submission_description")
and submit it.

## Dependencies
The evaluation code has been written and tested in Python 3.10.8 and depends on the following libraries:

networkx >= 3.0.0
numpy >= 1.24.2
matplotlib >= 3.6.3
loguru >= 0.6.0