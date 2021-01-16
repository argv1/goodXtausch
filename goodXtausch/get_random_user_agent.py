from   pathlib import Path
import random

# Global settings
base_path = Path(__file__).parent.absolute()
user_agent_f = base_path / 'random_user_agent.csv'  

def get_random_user_agent():
    '''
        grab a random user agent, based on https://github.com/argv1/random_user_agent
    '''   
    with open(user_agent_f, "r") as f:
        lines = f.read().splitlines()
        lines.pop(0)
    return({'User-Agent': random.choice(lines).rsplit(',', 3)[0]})