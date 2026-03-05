import sympy as sp


def polar_rek(magnetude, angle_deg):
    """Return a complex number, from polar form (mag, angle_deg)"""
    img = angle_deg * sp.pi / 180
    Z = magnetude * sp.exp(sp.I * img)
    return Z.evalf()


class rek_polar:
    """Return a complex number in polar notation (mag, angle_deg) from real and imag parts"""
    def __init__(self, real=None, imag=None, Z_number=None):
        self.real = real
        self.imag = imag
        self.Z_number = Z_number

    def show_polar(self):
        if self.Z_number is None:
            Z = self.real + sp.I*self.imag
        else: Z = self.Z_number

        mag = sp.Abs(Z)
        angle_rad = sp.arg(Z)
        angle_deg = angle_rad * 180 / sp.pi
        return f'{float(mag)} angle {float(angle_deg)}'
    
    def build_comp(self):
        if self.Z_number is None:
            Z = self.real + sp.I*self.imag
        else: Z = self.Z_number

        return Z.evalf()

def polar_deg(Z):
    """Return a complex number from rektan, to mag and angle degrees"""
    mag = sp.Abs(Z)
    ang_deg = sp.arg(Z) * 180 / sp.pi
    return f'{float(mag)} angle {float(ang_deg)}'

