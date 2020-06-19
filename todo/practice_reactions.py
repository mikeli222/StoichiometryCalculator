g_a = 3

reactions = {
    1: {
        'reaction': 'KClO3 = KCl + O2',
        'given_units': 'moles',
        'given_formula': 'KClO3',
        'solving_units': 'grams',
        'solving_formula': 'O2',
    },
    2: {
        'reaction': '3 AgNO3 + AlCl3 = 3 AgCl + Al(NO3)3',
        'given_units': 'grams',
        'given_formula': 'AlCl3',
        'solving_units': 'grams',
        'solving_formula': 'AgNO3',
    },
    3: {
        'reaction': '2 H2 + O2 = 2 H2O',
        'given_units': 'moles',
        'given_formula': 'O2',
        'solving_units': 'grams',
        'solving_formula': 'H2O',
    },
    4:{
        'reaction': 'N2 + 3 H2 = 2 NH3',
        'given_units': 'moles',
        'given_formula': 'N2',
        'solving_units': 'moles',
        'solving_formula': 'NH3',
    },
    5:{
        'reaction': 'Mg + 2 HCl = MgCl2 + H2',
        'given_units': 'grams',
        'given_formula': 'Mg',
        'solving_units': 'moles',
        'solving_formula': 'H2',
    }
}

def get_reaction(y, x):
    g_a = x
    reactions = {
        1: {
            'prompt': f'{g_a} mol of KClO<sub>3</sub> decomposes. How many grams of O2 will be produced?'
        },
        2: {
            'prompt': f'Calculate the mass of AgCl that can be prepared from {g_a} g of AlCl3 and sufficient AgNO3, using this equation:  3 AgNO<sub>3</sub> + AlCl<sub>3</sub> -> 3 AgCl + Al(NO3)<sub>3</sub>'
        },
        3: {
            'prompt': f'How many grams of H<sub>2</sub>O are produced when {g_a} moles of oxygen are used?'
        },
        4: {
            'prompt': f'If we have {g_a} mol of N<sub>2</sub> reacting with sufficient H<sub>2</sub>, how many moles of NH<sub>3</sub> will be produced?'
        },
        5: {
            'prompt': f'{g_a} grams of magnesium reacts with hydrochloric acid according to this balanced reaction: '
                      f'<br> Mg(s) + 2 HCl(aq) = MgCl<sub>2</sub>(aq) + H<sub>2</sub>(g)\n'
                      f'<br>How many moles of hydrogen gas will be produced?'
        }
    }
    return reactions[y]['prompt']