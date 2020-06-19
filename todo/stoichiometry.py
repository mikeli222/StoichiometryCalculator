from .molar_mass import molar_mass


def stoichiometry_solver(reaction, given_amount, given_units, given_formula, solving_units, solving_formula):
    parsed = reaction.split(" ")
    parsed[:] = [x for x in parsed if x not in ["=", "+", "->"]]
    # Add coefficient of 1
    i = 0
    while i < len(parsed):
        if not parsed[i].isdigit() and not parsed[i - 1].isdigit():
            parsed.insert(i, "1")
        i += 1

    def coefficient(specie):
        specie_index = parsed.index(specie)
        return int(parsed[specie_index - 1])
    if given_units == "grams":
        given_moles = given_amount / molar_mass(given_formula)
    elif given_units == "moles":
        given_moles = given_amount
    elif given_units == "molecules":
        given_moles = given_amount / 6.022E23
    solving_moles = given_moles * (coefficient(solving_formula) / coefficient(given_formula))
    if solving_units == "grams":
        results = round(solving_moles * molar_mass(solving_formula), 2)
    elif solving_units == "moles":
        results = round(solving_moles, 2)
    elif solving_units == "molecules":
        results = round(solving_moles * 6.022E23, 2)
    return [results, coefficient(given_formula), coefficient(solving_formula)]

