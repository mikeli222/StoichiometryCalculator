import re

atomic_mass = {
    "H": 1.0079, "He": 4.0026, "Li": 6.941, "Be": 9.0122,
    "B": 10.811, "C": 12.011, "N": 14.007, "O": 15.999, "F": 18.998,
    "Ne": 20.180, "Na": 22.990, "Mg": 24.305, "Al": 26.982,
    "Si": 28.086, "P": 30.974, "S": 32.065, "Cl": 35.453,
    "Ar": 39.948, "K": 39.098, "Ca": 40.078, "Sc": 44.956,
    "Ti": 47.867, "V": 50.942, "Cr": 51.996, "Mn": 54.938,
    "Fe": 55.845, "Co": 58.933, "Ni": 58.693, "Cu": 63.546,
    "Zn": 65.39, "Ga": 69.723, "Ge": 72.61, "As": 74.922,
    "Se":78.96, "Br": 79.904, "Kr": 83.80, "Rb": 85.468, "Sr": 87.62,
    "Y": 88.906, "Zr": 91.224, "Nb": 92.906, "Mo": 95.94,
    "Tc": 97.61, "Ru": 101.07, "Rh": 102.91, "Pd": 106.42,
    "Ag": 107.87, "Cd": 112.41, "In": 114.82, "Sn": 118.71,
    "Sb": 121.76, "Te": 127.60, "I": 126.90, "Xe": 131.29,
    "Cs": 132.91, "Ba": 137.33, "La": 138.91, "Ce": 140.12,
    "Pr": 140.91, "Nd": 144.24, "Pm": 145.0, "Sm": 150.36, "Eu": 151.96,
    "Gd": 157.25, "Tb": 158.93, "Dy": 162.50, "Ho": 164.93, "Er": 167.26,
    "Tm": 168.93, "Yb": 173.04, "Lu": 174.97, "Hf": 178.49, "Ta": 180.95,
    "W": 183.84, "Re": 186.21, "Os": 190.23, "Ir": 192.22, "Pt": 196.08,
    "Au": 196.08, "Hg": 200.59, "Tl": 204.38, "Pb": 207.2, "Bi": 208.98,
    "Po": 209.0, "At": 210.0, "Rn": 222.0, "Fr": 223.0, "Ra": 226.0,
    "Ac": 227.0, "Th": 232.04, "Pa": 231.04, "U": 238.03, "Np": 237.0,
    "Pu": 244.0, "Am": 243.0, "Cm": 247.0, "Bk": 247.0, "Cf": 251.0, "Es": 252.0,
    "Fm": 257.0, "Md": 258.0, "No": 259.0, "Lr": 262.0, "Rf": 261.0, "Db": 262.0,
    "Sg": 266.0, "Bh": 264.0, "Hs": 269.0, "Mt": 268.0
}


def find_mass(com):
    mass = 0
    for i in range(len(com)):
        if i == len(com)-1:
            if com[i].isdigit():
                pass
            elif com[i].isalpha():
                mass += atomic_mass[com[i]]
            break
        if com[i].isalpha():
            if com[i+1].isdigit():
                mass += atomic_mass[com[i]] * int(com[i+1])
            elif com[i+1].isalpha():
                mass += atomic_mass[com[i]]
        elif com[i].isdigit():
            pass
    return round(mass, 4)


def mass_polyatomic(com1):
    polyatomic = []
    open_paren = com1.index("(")
    closed_paren= com1.index(")")
    for i in range(open_paren+1, closed_paren):
        polyatomic.append(com1[i])
    return find_mass(polyatomic)


def molar_mass(formula):
    components = re.findall(r"[A-Z][a-z]*|[0-9]+|\(|\)", formula)
    m_mass = 0
    if "(" and ")" in components:
        poly_mass = mass_polyatomic(components)
        start_paren = components.index("(")
        end_paren = components.index(")")
        coeff = components[end_paren+1]
        mass_poly = (poly_mass*int(coeff))
        m_mass += mass_poly
        del components[start_paren:end_paren+2]
    non_poly_mass = find_mass(components)
    m_mass += non_poly_mass
    return round(m_mass, 3)

