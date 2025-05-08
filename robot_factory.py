import inspect
import importlib.util
import os
from agent_core import Robot, Router, Agent
from typing import List, Type, Dict

def _import_module_from_file(module_name, file_path):
    spec = importlib.util.spec_from_file_location(module_name, file_path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module

class RobotFactory:
    """Factory for creating robots with automatically discovered agents"""
    
    def __init__(self, agents_dir: str = "agents"):
        self.agents_dir = agents_dir
        self.agent_classes: Dict[str, Type] = {}
        self._discover_agents()
    
    def _discover_agents(self):
        """Discovers all agent classes in the agents directory"""
        agent_files = [f for f in os.listdir(self.agents_dir) if f.endswith('.py') and f != '__init__.py']
        for file_name in agent_files:
            module_name = file_name[:-3]
            file_path = os.path.join(self.agents_dir, file_name)
            module = _import_module_from_file(f"{self.agents_dir}.{module_name}", file_path)
            for name, obj in inspect.getmembers(module):
                if (
                    inspect.isclass(obj)
                    and hasattr(obj, "__module__")
                    and obj.__module__.startswith(self.agents_dir)
                    and issubclass(obj, Agent)
                    and obj is not Agent
                ):
                    self.agent_classes[name] = obj
        print("Discovered agent classes:", list(self.agent_classes.keys()))
    
    def create_robot(self, name: str, agent_names: List[str]) -> Robot:
        """Creates a robot with the specified agents"""
        agent_classes = []
        for agent_name in agent_names:
            if agent_name in self.agent_classes:
                agent_classes.append(self.agent_classes[agent_name])
            else:
                raise ValueError(f"Agent {agent_name} not found")
        robot_class = type(f"{name}Robot", (Robot,), {
            'pipeline': agent_classes
        })
        return robot_class

class RobotB(Robot):
    """Custom RobotB that loops to process all words sent by Robot A."""
    def run(self):
        try:
            while True:
                # Reset per-word context
                self.context['word'] = None
                self.context['reversed_word'] = None
                self.context['is_pal'] = None

                # Receive a word from Robot A
                agent = self.pipeline[0](self.router)  # ReceiveWordB
                agent.run(self.context)
                word = self.context.get('word')
                print(f"[RobotB] Loop received word: {word}")
                if word == 'STOP' or word is None:
                    print("[RobotB] Received STOP or None, breaking loop.")
                    break  # No more words to process

                # Run the rest of the pipeline for this word
                for agent_class in self.pipeline[1:4]:  # ReverseText, CompareOriginal, SendResultB
                    agent = agent_class(self.router)
                    agent.run(self.context)
                # Post-processing for this word
                for agent_class in self.pipeline[4:]:
                    agent = agent_class(self.router)
                    agent.run(self.context)
        except Exception as e:
            print(f"Error in RobotB execution: {str(e)}")
            self.context['error'] = str(e)
            self.context['done'] = True

# Example usage:
if __name__ == "__main__":
    factory = RobotFactory()
    
    # Create Robot A
    robot_a = factory.create_robot("A", [
        "LoadInput", "ToLower", "RemovePunct", "RemoveSpaces",
        "SplitWords", "TrimWords", "SendWord", "ReceiveResult",
        "HasMoreWords", "SortPalindromes", "JoinWithComma",
        "DuplicateOutput", "CapitalizeAll", "FormatFinal",
        "LogResult", "ReleaseResources", "ReturnHome"
    ])
    
    # Create Robot B
    robot_b = factory.create_robot("B", [
        "ReceiveWordB", "ReverseText", "CompareOriginal",
        "SendResultB", "LogCheck", "ReleaseResourcesB", "ReturnHomeB"
    ])
    
    # Create router and robots
    router = Router()
    a = robot_a(router)
    b = robot_b(router)
    
    # Set input and run
    a.context['input'] = "Madam Arora teaches malayalam"
    a.start()
    b.start()
    a.join()
    b.join() 