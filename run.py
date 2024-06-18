import random

"""
Global variables
"""

X_AXIS = 10	
Y_AXIS = 5

def generate_grid(x, y):
    """
    generates a list of lists based on x and y inputs.
    """
    y_axis = []
    i = 0
    while y > i:
        i +=1
        x_axis = []
        j = 0
        while x > j:
            x_axis.append('^')
            j +=1
        y_axis.append(x_axis)

    return y_axis
   

ocean = generate_grid(X_AXIS, Y_AXIS)
print(ocean)
