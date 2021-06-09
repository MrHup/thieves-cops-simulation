from mesa import Agent, Model
from mesa.datacollection import DataCollector
from mesa.space import MultiGrid
from mesa.time import RandomActivation

from helpers import *


# THIEVES VS non-THIEVES simulation
# rules: every step, people go to the grocery shop:
# 1) a thief tries to steal each time. If another person is nearby, he has a chance to get caught
# 2) if thief gets caught, the person that caught them can either turn into a thief themselves or report the thief
# 3) once a thief is reported, they go to jail for 10 steps then turn into a normal person again

# chances of getting caught are based on random charisma points
# chances of turning into a thief are based on random income of each person
# each time someone gets out of jail, chances to turn into a thief are reduced


class HonestyModel(Model):
    def __init__(
        self, initial_normal_agents: int, initial_thieves: float, width: int, height: int
    ):
        super(HonestyModel, self).__init__()

        self.initial_normal_agents = initial_normal_agents
        self.initial_thieves = initial_thieves

        self.grid = MultiGrid(width, height, True)
        self.schedule = RandomActivation(self)
        self.running = True

        # Create agents with thief gene
        for i in range(self.initial_thieves):
            name = f"Agent_{i}"
            agent = PersonAgent(
                    name, self, charisma=self.random.randrange(100), income=self.random.randrange(100), is_thief=True
                )
            self.schedule.add(agent)
            # Add the agent to random grid cells
            self.grid.place_agent(
                agent,
                (
                    self.random.randrange(self.grid.width),
                    self.random.randrange(self.grid.height),
                ),
            )

        # Create agents with honest gene (non-existant thief gene)
        for i in range(self.initial_normal_agents):
            name = f"Agent_{self.initial_thieves + i}"
            agent = PersonAgent(
                name, self, charisma=self.random.randrange(100), income=self.random.randrange(100), is_thief=False
            )
            self.schedule.add(agent)
            # Add the agent to random grid cells
            self.grid.place_agent(
                agent,
                (
                    self.random.randrange(self.grid.width),
                    self.random.randrange(self.grid.height),
                ),
            )

        # create a data collector for statistics
        self.data_collector = DataCollector(
            model_reporters={
                "thieves": compute_thieves,
                "normal": compute_normal,
                "is_jailed": compute_jailed,
            },
            agent_reporters={
                "income": "income",
                "charisma": "charisma",
                "is_jailed": "is_jailed",
            },
        )

    def step(self):
        self.data_collector.collect(self)
        self.schedule.step()



class PersonAgent(Agent):
    def __init__(self, unique_id: str, model: Model, charisma: int, income: int, is_thief: bool):
        super().__init__(unique_id, model)
        self.income = income
        self.charisma = charisma
        self.turning_probability = get_probability_based_on_income(income)
        self.getting_caught_probability = get_probability_based_on_charisma(charisma)

        self.days_until_release = None
        self.is_thief = is_thief
        self.is_jailed = False

        if is_thief:
            self.make_thief()

    def step(self):
        self.move()

        if self.is_thief:
                self.steal()
        
        if self.is_jailed:
            self.days_until_release -= 1

            if self.is_free():
                self.out_of_jail()


    def make_thief(self):
        self.is_thief = True

    def out_of_jail(self):
        self.is_jailed = False
        self.is_thief = False # reset person back to normal
        self.turning_probability = get_probability_based_on_income(self.income) - 0.4 # reduce chance to steal again

    def is_free(self):
        if self.days_until_release == 0:
            return True

        return False
    
    def to_jail(self):
        self.is_jailed = True
        self.is_thief = False
        self.days_until_release = SETTINGS["RULES"]["STEPS_UNTIL_JAIL_EXIT"]

    def steal(self):
        # when agents are near the thief
        for nearbycell in self.model.grid.get_cell_list_contents(
            [self.pos]
        ):
            if (
                not nearbycell.is_thief
                and self.random.random() < nearbycell.turning_probability
            ):
                nearbycell.make_thief()
            
        if (self.random.random() < self.getting_caught_probability):
            self.to_jail()
                

    def move(self):
        possible_steps = self.model.grid.get_neighborhood(
            self.pos, moore=True, include_center=False
        )
        new_position = self.random.choice(possible_steps)
        self.model.grid.move_agent(self, new_position)
