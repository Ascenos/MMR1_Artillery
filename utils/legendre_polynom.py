from numpy import zeros, negative, delete, prod, flipud
from numpy.polynomial.polynomial import Polynomial



def legendre_polynom(x, y):
    length = len(x)
    def legendre_part(k):
        output_polynom = zeros(length)
        # Adds combinations for x^n
        def add(value, pivot, n):
            for i in range(pivot, length-1, 1):
                # Type: x[0] * x[2] * x[3], rising order
                output_polynom[n] += value * numerator[i]
                add(value * numerator[i], i + 1, n + 1)
        if y[k] == 0:
            return output_polynom
        else:
            # Legendre-Polynom, x missing in numerator
            numerator = negative(delete(x, k))
            denominator = x[k] + numerator
            output_polynom[0] = y[k] / prod(denominator)
        add(output_polynom[0], 0, 1)
        return output_polynom
    polynom = zeros(length)
    for k in range(length):
        polynom += legendre_part(k)
    return Polynomial(flipud(polynom))
