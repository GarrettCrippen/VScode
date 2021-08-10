password_variations = []
#1638 variations, total = 1638*100 = alot
def transform_data():
    name_test = 'ronald-mcdonald'
    transformed = ''
    for i in range(0,9):
        password_variations.append(f'{name_test}{i}')
        password_variations.append(f'{name_test.capitalize()}{i}')

        for j in range(0,9):
            password_variations.append(f'{name_test}{i}{j}')
            password_variations.append(f'{name_test.capitalize()}{i}')

            for k in range(0,9):
                password_variations.append(f'{name_test}{i}{j}{k}')
                password_variations.append(f'{name_test.capitalize()}{i}')

transform_data()
print(len(password_variations))
