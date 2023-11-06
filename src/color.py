from math import floor


def get_rainbow_array(length: int, low: int, high: int):
    """
    :param length:
    :param low:
    :param high:
    """
    
    cycle = [[high, low, low],
             [high, high, low],
             [low, high, low],
             [low, high, high],
             [low, low, high],
             [high, low, high]]

    array = []

    for i in range(length):
        cycle_pos = i / length * (len(cycle) - 1)
        cycle_start = floor(cycle_pos)
        error = cycle_pos - cycle_start

        arr = []
        for j in range(len(cycle[cycle_start])):
            arr.append(int(cycle[cycle_start][j] + error * (cycle[cycle_start + 1][j] - cycle[cycle_start][j])))

        array.append(arr)

    return array
