import argparse

MONTHS_IN_YEAR:int = 12


if __name__ == '__main__':
    parser = argparse.ArgumentParser("MortgageSaver", description="This program will calculate the difference between two interest rates and the amount of time it will take to payoff a refinance if closing costs are provided.")

    parser.add_argument("amount", help="The amount of the loan.", type=float)
    parser.add_argument("initial", help="The interest rate before refinancing.", type=float)
    parser.add_argument("final", help="The interest rate after refinancing.", type=float)
    parser.add_argument("--refi", help="The costs to complete the refinance.", type=float, default=None)
    parser.add_argument("--term", help="The total length of the load. Defaults to 30 years or 360 months.", type=int, default=30)

    args = parser.parse_args()

    term_length_months = args.term * MONTHS_IN_YEAR

    rate_initial: float = args.initial / 100.
    rate_final: float = args.final / 100.

    monthly_growth_initial: float = 1. + rate_initial / MONTHS_IN_YEAR
    monthly_growth_final: float = 1. + rate_final / MONTHS_IN_YEAR

    monthly_payment_initial: float = float(args.amount) * rate_initial / (float(MONTHS_IN_YEAR) * (1.-(1./monthly_growth_initial) ** term_length_months))
    monthly_payment_final: float = float(args.amount) * rate_final / (float(MONTHS_IN_YEAR) * (1.-(1./monthly_growth_final) ** term_length_months))
    monthly_payment_difference: float = monthly_payment_initial - monthly_payment_final

    print("*** Monthly Payment ***")
    print("Initial    : ${:.2f}".format(monthly_payment_initial))
    print("Final      : ${:.2f}".format(monthly_payment_final))
    print("Difference : ${:.2f}".format(monthly_payment_difference))

    if args.refi == None:
        exit(0)

    payoff_length_months: float = args.refi / float(monthly_payment_difference)
    payoff_length_years: float = payoff_length_months / MONTHS_IN_YEAR

    print("\n*** Refinance ***")
    print("Months : {:.1f}".format(payoff_length_months))
    print("Years  : {:.2f}".format(payoff_length_years))
