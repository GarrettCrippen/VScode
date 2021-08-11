from atheletes_df import create_df

dict = {}
password_variations = []
def ap2(name,suffix):
    password_variations.append(f'{name.capitalize()}{suffix}')
    password_variations.append(f'{name}{suffix}')

#1638 variations, total = 1638*100 = alot
def transform_data(names):

    for name in names:
        transformed = ''
        for i in range(0,9):
            ap2(name,f'{i}')

            for j in range(0,9):
                ap2(name,f'{i}{j}')

                for k in range(0,9):
                    ap2(name,f'{i}{j}{k}')

transform_data(create_df()['name'])
print(len(password_variations))
