import multiprocessing
from multiprocessing import Manager as man
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
        self.num_agents = multiprocessing.cpu_count()
        self.num_cubbies = num_cubbies
        self.manager = man()
        #self.termination_point = multiprocessing.Value(int, termination_point)
        self.termination_point = int(termination_point)

        self.cubbyholes = self.manager.list()
        for cubby in range(num_cubbies):
            self.cubbyholes.append(Cubby(int(initial_cubby_value)))

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
                    this_agent_process = multiprocessing.Process(target=self.modify_cubbyhole, args=(self.cubbyholes, ))
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
                    this_agent_process = multiprocessing.Process(target=self.modify_cubbyhole, args=(self.cubbyholes, ))
                    agent_processes.append(this_agent_process)
                    this_agent_process.start()
                    run_counter += 1

                # Make sure we wait for processes to finish before running again
                for elem in agent_processes:
                    proc = agent_processes.pop()
                    proc.join()

                for cub in self.cubbyholes:
                    print("Cub: " + str(cub.get_value()))

    # I tried putting this in here, to see if it would fix the problem. Not sure that we need it here
    def modify_cubbyhole(self, cubbies, delta_upper_bound=50):
        # The calling process should indicate which cubbyholes to modify,
        # but the Agent will automatically select a value by which to change
        # the cubbyholes' values.
        cubby_a = randint(0, self.num_cubbies-1) #cubby_array[randint(0, self.num_cubbies-1)]
        cubby_b = randint(0, self.num_cubbies-1) #cubby_array[randint(0, self.num_cubbies-1)]
        delta_value_a = randint(0, delta_upper_bound)
        delta_value_b = delta_value_a * (-1)
        print(multiprocessing.current_process())

        if self.locking_enabled:
            # Hold up here until both locks are free
            while cubbies[cubby_a].get_lock() and cubbies[cubby_b].get_lock() == True:
                print("Waiting")
                time.sleep(0.001)

            # Critical section
            cubbies[cubby_a].set_lock()
            cubbies[cubby_b].set_lock()
            print("Cubby Pre: " + str(cubbies[cubby_b].get_value()))
            cubbies[cubby_a].change_value(delta_value_a)
            cubbies[cubby_b].change_value(delta_value_b)
            print("Delta: " + str(delta_value_a))
            print("Cubby Post: " + str(cubbies[cubby_b].get_value()))
            cubbies[cubby_a].release_lock()
            cubbies[cubby_b].release_lock()

        else:
            # Change values without locking
            cubbies[cubby_a].change_value(delta_value_a)
            cubbies[cubby_b].change_value(delta_value_b)