import random

def get_random_user_agent(user_agent_f):
    '''
        grab a random user agent, based on https://github.com/argv1/random_user_agent
    '''   
    with open(user_agent_f, "r") as f:
        lines = f.read().splitlines()
        lines.pop(0)
    return({'User-Agent': random.choice(lines).rsplit(',', 3)[0]})