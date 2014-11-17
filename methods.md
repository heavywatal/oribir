Materials and methods
=====================

Usage
-----

Origami Bird Simulator (OBS) starts from the time an Origami Bird population splits into to two separated populations.
The application window has three tabs.
In the first and second tabs, the user observes the evolution of two populations respectively.
The user can alter the parameters (environment, mutation rate, and population size, observation period) for each tab.
The environment denotes the abundance of oases and can be chosen from three options: rich, medium, and poor.
Figure 3a shows the example where the oasis-poor environment is chosen.
When "Lock" button is pressed, the parameters are locked and the simulation gets ready to start.
Ten individuals that are chosen randomly from the population are displayed on the right side.
After the evolutionary simulation, the test subject for crossing experiment is selected by clicking the individual in this panel.
The user repeats these steps in the second tab (Figure 3b shows the example where the user choose the oasis-rich environment).
In the "Crossing Experiment" tab, the selected individuals from the two populations are displayed.
The pair tries to mate when the "Cross" button is pressed.
Children are born if they succeed (Figure 3c) otherwise the animation of copulation failure is displayed (Figure 3d).

**Definition of genotype and phenotype**:
An individual has a forewing and a hindwing, each of which has two loci with four alleles (nucleotides).
The wing sizes are calculated by scaling them to decimal numbers
(i.e., `AA`: 0, `AT`: 1, `AG`:2, `AC`:3, `TA`:4, ..., `CG`: 14, `CC`: 15)
and by averaging the values of two chromosomes.
For example, the individual with genotype `[AATT, GGCC]` develops a forewing from heterozygotic `AA:GG` and its size is $(0 + 10) / 2= 5$.
When this individual mates and reproduces, possible zygotes are not only `[AATT]` and `[GGCC]`, but also `[AATC]` and `[GATT]` because of recombination.
Other traits such as head clips and wing color have not been implemented yet.

**Flight distance**:
We assume that the flight distance is determined only by the size of wings and calculated as $\mbox{hindwing} - \mbox{forewing} + 15$.
In other words, the flight distance increases with increasing hindwing size and with decreasing forewing size.
This assumption is based on the observation in the experiments of Yamanoi (2010),
where the students were encouraged to throw Origami Bird with constant power so that the effect of throwing motion was minimized.

**Fitness function**:
We assume that the optimal flight distance increases with the decreasing oases in an environment.
The Gaussian function is adopted as a fitness function and normalized so that the individual with the optimal flight distance gets the maximum fitness $1.0$ (Lande 1975; Wagner 1989; Johnson and Barton 2005).
The fitness of individual $i$ is defined as
$$
W_i = \exp \Big(- \frac {(x_i - x_o)^2} {2\sigma^2} \Big),
$$
where $x_i$ is the flight distance divided by the maximum distance $30$,
$x_o$ is the optimal value in each environment ($0.03$ for oasis-rich, $0.5$ for intermediate, and $0.97$ for oasis-poor),
and $\sigma$ is fixed to $0.5$ (Figure 4).


**Mutation rate**:
The default mutation rate is $10^{-2}$ per locus per generation.
Although this is much higher than the estimated values in real organisms,
it is necessary to shorten the waiting time to get evolutionary outcome
and makes no qualitative difference for our purpose here.
The same value is assigned to the recombination rate.
The user can alter the value between $10^{-3}$ and $10^{-1}$.

**Mating and reproduction**:
A population with $N$ individuals makes $N/2$ parent pairs.
Each pair lays 20 eggs if they can copulate, otherwise no egg.
Population size is constant and $N$ children survive to the next reproduction.
Roulette selection is conducted on the basis of the relative fitness of each individual.
The survival probability of individual $i$ can be described as
$$
P_i = \frac {W_i} {\sum^{}_j W_j}.
$$

**Reproductive isolation**:
We assume post-mating, prezygotic barriers on the basis of wing sizes.
First, the differences in forewing size and hindwing size need to be both smaller than five.
A male try to put his head through the partner's hindwing from behind if her hindwing is larger than her forewing (Figure 5a).
In that case, his forewing (Figure 3c left) needs to be smaller than the partner's hindwing (Figure 3c right).
To the contrary, a male try to put the partner's tail through his forewing from the front if her hindwing is smaller than her forewing (Figure 5b).
Then, the male's forewing needs to be larger than the partner's hindwing.
