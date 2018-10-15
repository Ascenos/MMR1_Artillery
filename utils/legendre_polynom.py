from numpy import zeros, negative, delete, prod, flipud
from numpy.polynomial.polynomial import Polynomial

def legendre_polynom(x, y):
    """
    Args:
        x (numpy array): x values of points.
        y (numpy array): y values of points.
    Returns:
        Polynomial: returns y values for x values.
    """
    # Number of x values.
    length = len(x)
    def legendre_part(k):
        """
        Args:
            k (int): position.
        Returns:
            numpy array: Legendre-Polynom of position k
        """
        # Generate empty array containing the polynom
        output_polynom = zeros(length)
        
        def add(value, pivot, n):
            """
            Turns polynom in style ((x-1) * (x+1) * ...)
            into polynom of style (a_0 + a_1 * x + ... + a_n * x^n)
            Args:
                value (float): Current base value.
                pivot     (int): First possible value to multiply to the base value. x[0] * x[2] * x[3] <- 4
                n           (int): Number of values multiplied, marks the position of the polynom array.
            Returns:
                void: output_polynom is edited.
            """
            for i in range(pivot, length-1, 1):
                output_polynom[n] += value * numerator[i]
                add(value * numerator[i], i + 1, n + 1)

        # If the legendre polynoms y(k) is 0 return 0.
        if y[k] == 0:
            return output_polynom
        # Else generte the Legendre-Polynom
        else:
            # Legendre-Polynom, x missing in numerator
            numerator = negative(delete(x, k))
            denominator = x[k] + numerator
            # Set first value to the height of y(k) devided by the product of the denominators.
            output_polynom[0] = y[k] / prod(denominator)
            add(output_polynom[0], 0, 1)
            return output_polynom

    # Generate empty polynomial.
    polynom = zeros(length)
    # Add Legendre-Polynoms to the polynom
    for k in range(length):
        polynom += legendre_part(k)
    # Turn polynom into an object.
    return Polynomial(flipud(polynom))
