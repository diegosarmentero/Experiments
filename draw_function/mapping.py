
IDENTIFIER = 'FLASER'


class DiscreteData(object):

    def __init__(self, positions=None, meassures=None):
        self.positions = positions
        self.meassures = meassures


def get_robot_values():
    with open('data.log', 'r') as f:
        data = f.readlines()

    robot_values = []
    for d in data:
        if d.startswith(IDENTIFIER):
            values = d[
                d.find(IDENTIFIER) + len(IDENTIFIER):].strip().split()
            del values[0]
            positions = values[180:183]
            meassures = values[:180]
            discrete = DiscreteData(positions, meassures)
            robot_values.append(discrete)
    return robot_values
