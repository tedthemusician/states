def get_states():
    with open('states.txt', 'r') as f:
        states = f.read().split('\n')[:-1]
    return [state.replace(' ', '_') for state in states]

