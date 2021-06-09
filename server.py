from mesa.visualization.modules import CanvasGrid
from mesa.visualization.ModularVisualization import ModularServer
from mesa.visualization.modules import ChartModule

from models import HonestyModel
from helpers import SETTINGS


def agent_portrayal(agent):
    portrayal = {"Shape": "circle", "Filled": "true", "r": 0.5}

    if agent.is_thief:
        portrayal["Color"] = "red"
        portrayal["Layer"] = 0
    elif agent.is_jailed:
        portrayal["Color"] = "gray"
        portrayal["Layer"] = 2
    else:
        portrayal["Color"] = "green"
        portrayal["Layer"] = 1

    return portrayal


grid = CanvasGrid(
    agent_portrayal, SETTINGS["GRID"]["WIDTH"], SETTINGS["GRID"]["HEIGHT"], 500, 500
)

chart = ChartModule(
    [
        {"Label": "thieves", "Color": "Red"},
        {"Label": "normal", "Color": "Green"},
        {"Label": "is_jailed", "Color": "Gray"},
    ],
    data_collector_name="data_collector",
)

server = ModularServer(
    HonestyModel,
    [grid, chart],
    "Honesty Model",
    {
        "initial_normal_agents": SETTINGS["POPULATION"]["INITIAL_HONEST"],
        "initial_thieves": SETTINGS["POPULATION"]["INITIAL_THIEVES"],
        "width": SETTINGS["GRID"]["WIDTH"],
        "height": SETTINGS["GRID"]["HEIGHT"],
    },
)

server.port = 8002
server.launch()
