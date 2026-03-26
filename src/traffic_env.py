class TrafficEnv:

    def get_state(self, counts):

        return tuple(counts)

    def reward(self, counts):

        # minimize waiting vehicles
        return -sum(counts)