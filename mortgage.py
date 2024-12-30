import argparse
import decimal
from types import NoneType

MONTHS_IN_YEAR:int = 12
DOLLAR_QUANTIZE = decimal.Decimal('.01')

def dollar(f, round=decimal.ROUND_CEILING):
    """
    This function rounds the passed float to 2 decimal places.
    """
    if not isinstance(f, decimal.Decimal):
        f = decimal.Decimal(str(f))
    return f.quantize(DOLLAR_QUANTIZE, rounding=round)

class Mortgage:
    def __init__(self, interest, months, amount):
        self._interest = float(interest)
        self._months = int(months)
        self._amount = dollar(amount)

    def rate(self):
        return self._interest

    def month_growth(self):
        return 1. + self._interest / MONTHS_IN_YEAR

    def apy(self):
        return self.month_growth() ** MONTHS_IN_YEAR - 1

    def loan_years(self):
        return float(self._months) / MONTHS_IN_YEAR

    def loan_months(self):
        return self._months

    def amount(self):
        return self._amount

    def monthly_payment(self):
        pre_amt = float(self.amount()) * self.rate() / (float(MONTHS_IN_YEAR) * (1.-(1./self.month_growth()) ** self.loan_months()))
        return dollar(pre_amt, round=decimal.ROUND_CEILING)

    def total_value(self, m_payment):
        return m_payment / self.rate() * (float(MONTHS_IN_YEAR) * (1.-(1./self.month_growth()) ** self.loan_months()))

    def annual_payment(self):
        return self.monthly_payment() * MONTHS_IN_YEAR

    def total_payout(self):
        return self.monthly_payment() * self.loan_months()

    def monthly_payment_schedule(self):
        monthly = self.monthly_payment()
        balance = dollar(self.amount())
        rate = decimal.Decimal(str(self.rate())).quantize(decimal.Decimal('.000001'))
        while True:
            interest_unrounded = balance * rate * decimal.Decimal(1)/MONTHS_IN_YEAR
            interest = dollar(interest_unrounded, round=decimal.ROUND_HALF_UP)
            if monthly >= balance + interest:
                yield balance, interest
                break
            principle = monthly - interest
            yield principle, interest
            balance -= principle

def print_summary(m):
    print('{0:>25s}:  {1:>12.6f}'.format('Rate', m.rate()))
    print('{0:>25s}:  {1:>12.6f}'.format('Month Growth', m.month_growth()))
    print('{0:>25s}:  {1:>12.6f}'.format('APY', m.apy()))
    print('{0:>25s}:  {1:>12.0f}'.format('Payoff Years', m.loan_years()))
    print('{0:>25s}:  {1:>12.0f}'.format('Payoff Months', m.loan_months()))
    print('{0:>25s}:  {1:>12.2f}'.format('Amount', m.amount()))
    print('{0:>25s}:  {1:>12.2f}'.format('Monthly Payment', m.monthly_payment()))
    print('{0:>25s}:  {1:>12.2f}'.format('Annual Payment', m.annual_payment()))
    print('{0:>25s}:  {1:>12.2f}'.format('Total Payout', m.total_payout()))

if __name__ == '__main__':
    parser = argparse.ArgumentParser("MortgageSaver", description="This program will calculate the difference between two interest rates and the amount of time it will take to payoff a refinance if closing costs are provided.")

    parser.add_argument("amount", help="The amount of the loan.", type=float)
    parser.add_argument("initial", help="The interest rate before refinancing.", type=float)
    parser.add_argument("final", help="The interest rate after refinancing.", type=float)
    parser.add_argument("--refi", help="The costs to complete the refinance.", type=float)
    parser.add_argument("--term", help="The total length of the load. Defaults to 30 years or 360 months.", type=int, default=30)

    args = parser.parse_args()

    monthly_payment_initial: float = Mortgage(interest=args.initial / 100, amount=args.amount, months=args.term * MONTHS_IN_YEAR).monthly_payment()
    monthly_payment_final: float = Mortgage(interest=args.final / 100, amount=args.amount, months=args.term * MONTHS_IN_YEAR).monthly_payment()
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
