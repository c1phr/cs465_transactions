import multiprocessing
from random import randint
import time
from src.agent import Agent
from src.cubby import Cubby


class Manager(object):
    """
    The Manager does exactly what would be expected. Only one exists per
    system, and it maintains an array of cubbyholes, an array of agents, and
    other information about system state.
    """
    def __init__(self, num_cubbies, initial_cubby_value, locking_enabled=True, terminate_on="transactions", termination_point=10):
        # terminate_on specifies 'transactions' or 'time', and
        # termination_point specifies (depending on the value of
        # terminate_on) the number of transactions or seconds after which to
        # terminate. 

        self.locking_enabled = locking_enabled
        self.terminate_on = terminate_on
        self.termination_point = termination_point
        self.num_agents = multiprocessing.cpu_count()

        self.cubbyholes = []
        for cubby in range(num_cubbies):
            self.cubbyholes.append(Cubby(initial_cubby_value))

        self.agents = []
        for agent in range(self.num_agents):
            self.agents.append(Agent(num_cubbies, self.locking_enabled))

        self.agent_processes = []

    print("before run manager")
    def run(self):
        agent_processes = []

        if self.terminate_on == "time":
            print("manager if")
            start_time = time.clock() # Get current time
            end_time = int(start_time) + int(self.termination_point)
            while time.clock() < end_time:
                for this_agent in self.agents:
                    this_agent_process = multiprocessing.Process(target=this_agent.run, args=(self.cubbyholes, ))
                    agent_processes.append(this_agent_process)
                    this_agent_process.start()

                # Make sure we wait for processes to finish before running again
                for elem in agent_processes:
                    proc = agent_processes.pop()
                    proc.join()

        else:
            print("manager else")
            run_counter = 0
            while run_counter < self.termination_point:
                for this_agent in self.agents:
                    this_agent_process = multiprocessing.Process(target=this_agent.run, args=(self.cubbyholes, ))
                    agent_processes.append(this_agent_process)
                    this_agent_process.start()
                    run_counter += 1

                # Make sure we wait for processes to finish before running again
                for elem in agent_processes:
                    proc = agent_processes.pop()
                    proc.join()

