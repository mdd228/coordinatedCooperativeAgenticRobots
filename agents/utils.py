from agent_core import Agent

class ReleaseResources(Agent):
    """Releases resources used by the robot"""
    def run(self, ctx):
        ctx.setdefault('log_a', []).append("ReleaseResources: Releasing resources")
        print("RobotA: Releasing resources")

class ReturnHome(Agent):
    """Signals robot completion"""
    def run(self, ctx):
        ctx.setdefault('log_a', []).append("ReturnHome: Returning home")
        print("RobotA: Returning home")

class ReleaseResourcesB(Agent):
    """Releases resources used by Robot B"""
    def run(self, ctx):
        ctx.setdefault('log_b', []).append("ReleaseResourcesB: Releasing resources")
        print("RobotB: Releasing resources")

class ReturnHomeB(Agent):
    """Signals Robot B completion"""
    def run(self, ctx):
        ctx.setdefault('log_b', []).append("ReturnHomeB: Returning home")
        print("RobotB: Returning home") 