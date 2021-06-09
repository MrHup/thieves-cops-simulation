# Thieves vs Non Thieves simulation
Simple project that uses the mesa python3 package to simulate a game of thieves vs cops.
The population is composed of 3 types of people: thieves(red), normal(green) and jailed people(gray).

# Rules
### Every step, people go to the grocery shop:
1. a thief tries to steal each time. If another person is nearby, he has a chance to get caught
2. if thief gets caught, the person that caught them can either turn into a thief themselves or report the thief
3. once a thief is reported, they go to jail for 10 steps then turn into a normal person again

- chances of getting caught are based on random charisma points
- chances of turning into a thief are based on random income of each person
- each time someone gets out of jail, chances to turn into a thief are reduced

# Installation
Poetry is required to install the project.

## Using pip3
To install poetry:
```bash
pip3 install poetry
```

Create the environment:
```bash
poetry install
```

Furthermore, mesa library is mandatory
```bash
pip3 install Mesa
```

# Running the application
```bash
poetry run python server.py 
```