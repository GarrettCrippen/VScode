from atheletes_df import create_df

def ap2(name,suffix, password_variations):
    password_variations.append(f'{name.capitalize()}{suffix}')
    password_variations.append(f'{name}{suffix}')

#1638 variations, total = 1638*100 = alot
def transform_data(names):

    atheletes = {}

    for name in names:
        name = name.replace('-','')
        password_variations = []
        for i in range(0,9):
            ap2(name,f'{i}',password_variations)

            for j in range(0,9):
                ap2(name,f'{i}{j}',password_variations)

                # for k in range(0,9):
                #     ap2(name,f'{i}{j}{k}',password_variations)

        atheletes[name]=password_variations
    
    return atheletes

