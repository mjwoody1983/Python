# Betting Model
## Introduction
This was a starting point on a Poisson distribution using historical football data, the aim being to determine the probable number of goals scored in a game.

The Poisson distribution allows us to measure the probability of independent events occuring within a period of time. The way this is modelled in the python script is to take items such as defensive strength, attacking strength, league variables and turn these events into a probability.

Please note, this is a simple starting point, I have moved this model on since I started working on it in 2017, bookmaker models are also further advanced than this as they have access to more data, teams of developers and also get to set the price.

## Metrics
Below are a small sample of some of the calculations included. They help to form the relative attacking and defensive strengths of a team.

* Average Goals Home
* Average Goals Away
* Home Goals / League Average Home (There are different interpretations of this)
* Away Goals / League Average Away 

## Historic Predictions
From this starting point, using psycopg2, I started to persist this data over time to measure the accuracy of the predictions and see if there was the possibility to place value bets as a result. 
