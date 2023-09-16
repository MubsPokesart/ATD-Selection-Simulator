# NBA All-Time Draft Selection Simulator

A weighted randomness model for drafting 500+ basketball players from 1960 to the present day in a snake draft system that incorporates community-created data.

## Technologies Used
```sh
Language: Python
Libraries: random, csv, statistics
```

## Overview

### Main Idea
The whole idea of this program is that it's aimed to simulate the solo drafting of a team of 5-10 players. it utilizes baseline fit checks, a database of previous draft positions, and weighted randomness to simulate what players would be available for a person in a Historical NBA draft similar to the ones hosted in the [Historical NBA Drafts Community]([URL](
discord.gg/hdnba)) by utilizing their [database of previous drafts]([url](https://docs.google.com/spreadsheets/d/1ts62gSSJd8o2nF6OhpJV1lc_OrIMdMsCo7aLxYT2qRU/edit)https://docs.google.com/spreadsheets/d/1ts62gSSJd8o2nF6OhpJV1lc_OrIMdMsCo7aLxYT2qRU/edit). 

### How the picking algorithm actually works

It essentially utilizes an ADP sample in order to run a weighted randomness model with other factors, having a certain amount of players considered to run the weighted randomness selection model. It decides between 2 eligible players until pick 30, 4 until pick 90, 6 until pick 140, and 8 for the rest of the draft onwards.

The word 'eligible players' is used here as there are checks to make sure that two centers don't get placed together, though there is some level of ball dominance that is in the works to be taken into account. 

The formula is ``selection value = ((ADP - current selection) + (faller rating)) * (positional value * positional scarcity)`` where the lowest value in the sample is the most likely to be picked.
- Average Draft Position and the Current Selection is self-explanatory 
- Faller Rating == standard deviation of a player's pick history, essentially simulating the fact that certain players fall more than others. For example, a player like George Gervin who fluctuates a lot has a draft sample of ``83, 101, 106, 88, 105, 77, 92, 105, 99, 94, 100``, which averages out to ``95.45454545`` has a faller rating of ``9.1588371270954`` which can decrease the likelihood of being picked.
- Positional Value is how valuable the position of a player is. My values are  ``'Guard': 1.25, 'Wing': .75, 'Forward': 1, 'Big': 1.5`` and the algorithm here makes it so picking up a Guard/Wing is more valuable than picking up a big man. It goes ``Wing/Forward = 0.7, Wing = .75, Guard/Wing = .8, Forward =  1, Forward/Big = 1, Guard =  1.25, Big = 1.5`` where a smaller value is better.
- Positional scarcity essentially calculates how many players of similar positions are available around that ADP. If say Wings are scarce, it is more likely to take a wing.

Here's it in practice.

```
Pick 13:
Players considered: Kawhi Leonard, Dwyane Wade, David Robinson

[Player = ((Average Draft Position - Current Pick) + Standard Deviation of Player Sample (faller rating)) * (Position Value * Scarcity (set at 1 for this))]

Position Values are:
Wing/Forward = 0.7
Wing = .75
Guard/Wing = .8
Forward =  1
Forward/Big = 1
Guard =  1.25
Big = 1.5 

Back to sim:
Kawhi Leonard = ((14.54545455 - 13) + 1.809068067) * (.7 * 1) = 2.34816583
Dwayne Wade = ((14.8 - 13) + 2.043961296) * (1.25 * 1) = 4.80495162
David Robinson = ((16.45454545 - 13) + 2.339386089) * (1.5 * 1) = 8.69089731

Reverse the weights (so the lower value gets higher weighted)
15.8440148 - 2.34816583 = 13.495849, 15.8440148 - 4.80495162 = 11.0390632, 15.8440148 - 8.69089731 = 7.15311749
(13.495849 + 11.0390632 + 7.15311749) = sum of those weights

In this case, the program has a (13.495849 / (13.495849 + 11.0390632 + 7.15311749)) * 100  - 42% chance of picking Kawhi Leonard, a (11.0390632 / (13.495849 + 11.0390632 + 7.15311749)) * 100 - 34% chance of picking Dwayne Wade, and a (7.15311749 / (13.495849 + 11.0390632 + 7.15311749)) 22% chance of picking David Robinson.```
