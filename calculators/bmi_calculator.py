'''
The function calculate_bmi takes the 
arguments body_weight expressed in kilograms and body_height expressed in centimeters.
'''


def calculate_bmi(body_weight, body_height):
    try:
        if (body_weight < 5):
            raise Exception("Body weight is less than 5kg")
        elif (body_height < 100):
            raise Exception(
                "Body height is less than 100cm or more than 300cm")
        bmi = body_weight / ((body_height / 100) ** 2)
        return round(bmi, 1)
    except Exception as e:
        return -1
