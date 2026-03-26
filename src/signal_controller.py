import time
from config import BASE_GREEN, YELLOW_TIME, MAX_GREEN

class SignalController:

    def __init__(self):

        self.lane = 0
        self.state = "GREEN"
        self.last_switch = time.time()

        self.green_time = BASE_GREEN

        # emergency handling
        self.emergency_active = False
        self.emergency_timer = 0

    def update(self, counts, ambulances, rl_lane):

        now = time.time()

        # 🚑 EMERGENCY OVERRIDE
        if True in ambulances:

            if not self.emergency_active:
                self.lane = ambulances.index(True)
                self.state = "GREEN"
                self.emergency_timer = 10  # fixed green time
                self.last_switch = now
                self.emergency_active = True

        if self.emergency_active:

            remaining = self.emergency_timer - (now - self.last_switch)

            if remaining <= 0:
                self.emergency_active = False
                self.last_switch = now

            return self.lane, self.state, int(max(remaining, 0))

        # 🚦 NORMAL LOGIC

        # GREEN → YELLOW
        if self.state == "GREEN":

            if now - self.last_switch > self.green_time:
                self.state = "YELLOW"
                self.last_switch = now

        # YELLOW → NEXT LANE
        elif self.state == "YELLOW":

            if now - self.last_switch > YELLOW_TIME:

                # 🔥 HYBRID DECISION (NO RANDOM BEHAVIOR)

                # if RL strongly prefers another lane
                if counts[rl_lane] > counts[self.lane] + 2:
                    self.lane = rl_lane
                else:
                    # otherwise follow fixed rotation
                    self.lane = (self.lane + 1) % 4

                # dynamic green time
                self.green_time = min(BASE_GREEN + counts[self.lane], MAX_GREEN)

                self.state = "GREEN"
                self.last_switch = now

        # ⏱️ TIMER CALCULATION
        if self.state == "GREEN":
            remaining = self.green_time - (now - self.last_switch)
        else:
            remaining = YELLOW_TIME - (now - self.last_switch)

        return self.lane, self.state, int(max(remaining, 0))