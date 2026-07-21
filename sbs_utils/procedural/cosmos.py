import sbs
from sbs_utils.agent import Agent
from sbs_utils.procedural.query import is_grid_object_id, is_space_object_id
from ..helpers import FrameContext

"""
Functions to the engine
"""

def sim_create() -> None:
    """ Creates a new simulation
    """
    grid_object_ids = [agent_id for agent_id in Agent.all if is_grid_object_id(agent_id)]
    space_object_ids = [agent_id for agent_id in Agent.all if is_space_object_id(agent_id)]
    FrameContext.context.sbs.create_new_sim()
    for grid_object_id in grid_object_ids:
        Agent.remove_id(grid_object_id)
    for space_object_id in space_object_ids:
        Agent.remove_id(space_object_id)

def sim_pause() -> None:
    """pauses the simulation
    """    
    FrameContext.context.sbs.pause_sim()



def sim_resume() -> None:
    """resume the simulation
    """    
    FrameContext.context.sbs.resume_sim()

