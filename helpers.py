SETTINGS = {
    "GRID": {"WIDTH": 15, "HEIGHT": 15},
    "POPULATION": {"INITIAL_HONEST": 100, "INITIAL_THIEVES": 4},
    "RULES": {
        "TURNING_PROBABILITY": {
            "0-15": 1,
            "15-30": 0.8,
            "30-50": 0.7,
            "50-70": 0.6,
            "70-150": 0.5,
        },
        "GETTING_CAUGHT_PROBABILITY": {
            "0-15": 0.6,
            "15-30": 0.3,
            "30-50": 0.2,
            "50-60": 0.1,
            "60-150": 0,
        },
        "STEPS_UNTIL_JAIL_EXIT": 10,
    },
}


def get_probability_based_on_income(income):
    for key in SETTINGS["RULES"]["TURNING_PROBABILITY"].keys():
        lower = int(key.split("-")[0])
        higher = int(key.split("-")[1])

        if lower <= income <= higher:
            return SETTINGS["RULES"]["TURNING_PROBABILITY"][key]

def get_probability_based_on_charisma(charisma):
    for key in SETTINGS["RULES"]["GETTING_CAUGHT_PROBABILITY"].keys():
        lower = int(key.split("-")[0])
        higher = int(key.split("-")[1])

        if lower <= charisma <= higher:
            return SETTINGS["RULES"]["GETTING_CAUGHT_PROBABILITY"][key]

def compute_normal(model):
    return sum([not agent.is_thief and not agent.is_jailed for agent in model.schedule.agents])


def compute_thieves(model):
    return sum([agent.is_thief for agent in model.schedule.agents])


def compute_jailed(model):
    return sum([agent.is_jailed for agent in model.schedule.agents])