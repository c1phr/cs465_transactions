from multiprocessing import Pool, Process

class Manager(object):
    """
    The Manager does exactly what would be expected. Only one exists per
    system, and it maintains an array of cubbyholes, an array of agents, and
    other information about system state.
    """
    def __init__(self, num_cubbies, num_agents, max_cubby_value,
            locking_enabled=True, terminate_on="transactions",
            termination_point="10"):
        # terminate_on specifies 'transactions' or 'time', and
        # termination_point specifies (depending on the value of
        # terminate_on) the number of transactions or seconds after which to
        # terminate. 

        self.locking_enabled=locking_enabled
        self.terminate_on=terminate_on
        self.termination_point=termination_point

        self.cubbyholes = []
        for cubby in range(num_cubbies):
            cubbyholes.append(Cubby(bounded_random(0, max_cubby_value)))

        self.agents = []
        for agent in range(num_agents):
            agents.append(Agent(locking_enabled))
        
        self.pool = Pool(processes=num_agents)

    def run():
        if self.terminate_on=="time":
            time_init = process_time()


