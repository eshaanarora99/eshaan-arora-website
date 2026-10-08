import matplotlib.pyplot as plt

def get_coupon():
    while True:
        value = input("Please enter the coupon rate percentage for this bond as a whole number (i.e., for 6% enter 6): ")
        try:
            return float(value) / 100
        except ValueError:
            print("Please enter a valid coupon rate!")

def get_TTM():
    while True:
        value = input("Please enter the term to maturity (TTM) for this bond in years: ")
        try:
            return float(value)
        except ValueError:
            print("Please enter a valid term to maturity!")


def get_APR():
    while True:
        value = input("Please enter the APR for this bond as a whole number (i.e., for 6% enter 6): ")
        try:
            return float(value) / 100
        except ValueError:
            print("Please enter a valid APR!")

def get_par():
    while True:
        value = input("This program will infer a par value of $1,000.00. If you would like to modify this, please enter a new par value. If you would like to accept the default setting, hit Enter: ")
        if value == '':
            value = 1000
            return value
        else:
            try:
                return float(value)
            except ValueError:
                print("Please enter a valid Par Value!")


def get_compounding():
    compounding_lookup = {'annual' : 1, 'semiannual' : 2, 'quarterly' : 4, 'monthly' :12, 'daily' : 365}

    while True:
        value = input("Please enter the compounding frequency of this bond (i.e., annual, semiannual, quarterly, monthly, or daily.) Else, hit Enter to accept the default of semiannual compounding.").lower()
        if value == '':
            value = compounding_lookup['semiannual']
            return value
        elif value in compounding_lookup:
            return compounding_lookup[value]
        else:
            print("Please enter a valid input (annual, semiannual, quarterly, monthly, or daily).")


def get_bondVal(coupon, ttm, apr, par, freq):
    bond_value = 0
    for i in range(1, int(ttm * freq) + 1):
        bond_value += (coupon * par / freq) / (1 + apr / freq) ** i
    bond_value += par / (1 + apr / freq) ** (ttm * freq)
    return bond_value

def get_graph(coupon, ttm, par, freq):
    yields = [i / 100 for i in range(1, 21)]
    bond_values = [get_bondVal(coupon, ttm, y, par, freq) for y in yields]

    plt.figure(figsize=(10, 6))
    plt.plot(yields, bond_values, marker='o')
    plt.title('Bond Value vs. Yield')

    plt.xticks(ticks=yields, labels=[f'{int(y*100)}%' for y in yields])

    plt.xlabel('Yield (%)')
    plt.ylabel('Bond Value ($)')
    plt.grid(True)
    plt.show()

def main():
    couponRate = get_coupon()
    TTM = get_TTM()
    APR = get_APR()
    Par = get_par()
    compoundRate = get_compounding()

    bond_value = get_bondVal(couponRate, TTM, APR, Par, compoundRate)

    print("The calculated bond value is $", round(bond_value, 2))

    get_graph(couponRate, TTM, Par, compoundRate)


if __name__ == "__main__":
    main()
