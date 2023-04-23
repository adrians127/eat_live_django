'''
The function water_calculate takes the arguments age expressed in years, gender
and returning how much water does need person with this age.
If something's wrong returning -1
'''


def calculate_for_woman(age):
    if age > 10 and age <= 12:
        return 1900
    elif age > 12 and age <= 15:
        return 1950
    elif age > 15:
        return 2000


def calculate_for_man_and_others(age):
    if age > 10 and age <= 12:
        return 2100
    elif age > 12 and age <= 15:
        return 2350
    elif age > 15:
        return 2500


def water_calculate(age, gender):
    if not isinstance(gender, str):
        return -1
    if age < 13 or age > 130:
        return -1

    match gender.lower():
        case 'F':
            return calculate_for_woman(age)
        case 'M':
            return calculate_for_man_and_others(age)
        case _:
            return calculate_for_man_and_others(age)  # for nonbinary persons
