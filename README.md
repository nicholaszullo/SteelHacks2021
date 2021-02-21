# SteelHacks2021 Project -- FlowChess

## Inspiration
We are both avid chess players and have always been interested in building an engine. Nick is currently in an ML/NN class in undergrad, and we decided that now might be a good time to give it a go. Chess engines (chess computers) are hugely important for reaching a better understanding of chess, and chess provides an excellent sandbox for training algorithms to play.

The name "FlowChess" is a tribute to the great Magnus Nielsen from the show Dark, and World Chess Champion Magnus Carlsen.

## What it does
FlowChess combines a Monte Carlo Tree Search with a neural net in order to make gameplay decisions. It plays itself n number of times, and the resulting play model is saved for use. For the sake of observation, a tracer GUI was constructed using tkinter in Python for viewing chess games, so we could get an intuitive sense for how the engine was playing.

## How we built it
We used Pytorch with CUDA as the engine to construct the chess computer. The GUI was constructed using Tkinter for python.

## Challenges we ran into
One challenge we ran into was with compute time. Even using the GPU, we had a difficult time doing a meaningful amount of training using a laptop.

## Accomplishments that we're proud of
We are proud that our engine follows all chess rules (no illegal moves) and that we can show its performance using a GUI

## What we learned
We learned about the Monte Carlo Tree Search, and how it can be used to solve certain problems. We learned about the differences between conventional and ML chess engines, and how rapidly chess games diverge (many board permutations in chess).

## What's next for FlowChess
It is our plan to continue developing our engine training algorithm and to try and train it with more compute power and see what happens.
