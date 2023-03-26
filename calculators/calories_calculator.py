'''
The function calculate_bmi takes the 
arguments body_weight expressed in kilograms and body_height expressed in centimeters.
'''


def calculate_for_woman(body_weight, body_height, age):
    PPM = 655.1 + 9.563 * body_weight + 1.85 * body_height - 4.676 * age
    print(PPM)
    return PPM


def calculate_for_man_and_others(body_weight, body_height, age):
    PPM = 66.5 + 13.75 * body_weight + 5.003 * body_height - 6.775 * age
    return PPM


def calculate_calories(body_weight, body_height, age, gender, PAL):
    match gender.lower():
        case 'woman':
            CPM = calculate_for_woman(body_weight, body_height, age) * PAL
        case 'man':
            CPM = calculate_for_man_and_others(
                body_weight, body_height, age) * PAL
        case _:
            CPM = calculate_for_man_and_others(
                body_weight, body_height, age) * PAL  # for nonbinary persons
    return round(CPM, 0)


def calculate_fat(CPM):
    return (round(0.25 * CPM / 9, 2), round(0.35 * CPM / 9, 2))  # 1g fat = 9kcal


def calculate_protein(CPM):
    # 1g protein = 4kcal
    return (round(0.1 * CPM / 4, 2), round(0.2 * CPM / 4, 2))


def calculate_carbohydrates(CPM):
    # 1g carbohydrates = 4kcal
    return (round(0.45 * CPM / 4, 2), round(0.65 * CPM / 4, 2))


def calculate_nutritions(body_weight, body_height, age, gender, PAL=1.2):
    if not isinstance(gender, str):
        return -1

    CPM = calculate_calories(body_weight, body_height, age, gender, PAL)
    fat = calculate_fat(CPM)
    protein = calculate_protein(CPM)
    carbohydrates = calculate_carbohydrates(CPM)
    return (CPM, fat, protein, carbohydrates)
