import math

def sampleToAngle(n):
    """
    Function that takes the sample difference between 2 mics
    and returns the angle away that the sound source is.
    Arguments: Number of Samples (n)
    Returns: Angle of source (theta)
    """
    if n > 42.695:
        x = 42.695
    elif n < -42.695:
        x = -42.695
    else:
        x = n
    A = 340.29/(44100*0.0254)
    denom = math.sqrt(20905*A**2*x**2 - A**4 * x**4)
    numer = 1872
    theta = math.acos(denom/numer)
    if n  < 0:
        theta = -theta
    return theta

if __name__ == "__main__":
    print(math.degrees(sampleToAngle(-33)))
