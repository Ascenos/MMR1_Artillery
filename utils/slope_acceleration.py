import numpy as np



def slope_x_acceleration(y1, y2, x, acc):
    """\
    Calculates the acceleration caused by a slope.
    Args:
        y1 (float, numpy array): left y value.
        y2 (float, numpy array): right y value.
        x   (float, numpy array): distance between values.
        y1 and x must be same shape as y2 or float.
        acc                     (float): acceleration of the object.

    Returns:
        same type as y2: contains acceleration towards to positive x-axis.
    """
    # Calculate y distance:
    y = y2 - y1
    # Calculate degree
    degree = np.arctan(y / x)
    # Calculate acceleration in direction of x-axis.
    acceleration = acc * np.cos(degree)

    return acceleration


def slope_downwards_x_acceleration(y1, y2, x, gravity = 10):
    """\
    Calculates the acceleration caused by a slope.
    Args:
        y1 (float, numpy array): left y value.
        y2 (float, numpy array): right y value.
        x   (float, numpy array): distance between values.
        y1 and x must be same shape as y2 or float.
        gravity                 (float): gravitational acceleration of the object.

    Returns:
        same type as y2: contains acceleration towards to positive x-axis.
    """
    # Calculate y distance:
    y = y2 - y1
    # Calculate degree
    degree = np.arctan(y / x)
    # Calculate acceleration in direction of slope
    acc = gravity * np.sin(degree)
    # Calculate acceleration in direction of x-axis
    acceleration = acc * np.cos(degree)

    return acceleration