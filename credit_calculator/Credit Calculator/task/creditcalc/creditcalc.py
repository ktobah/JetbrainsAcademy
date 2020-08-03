import sys
import math
import argparse

parser = argparse.ArgumentParser()
parser.add_argument("--type", help="specify the type of calculation", type=str)
parser.add_argument("--payment", help="the monthly payment", type=float)
parser.add_argument("--principal", help="the principal payment", type=float)
parser.add_argument("--interest", help="the interest rate", type=float)
parser.add_argument("--periods", help="periods required", type=int)
args = parser.parse_args()

if (not args.type or args.type not in ['annuity', 'diff']) \
        or (args.type == 'diff' and args.payment) \
        or (not args.interest) \
        or len(sys.argv) < 4 \
        or (args.principal and args.principal < 0) \
        or (args.principal and args.principal < 0) \
        or (args.payment and args.payment < 0) \
        or (args.interest and args.interest < 0) \
        or (args.periods and args.periods < 0):
    print('Incorrect parameters')
else:
    credit_interest = args.interest / (12 * 100)
    if args.type == 'annuity':
        # if choice != "p":
        #     credit_principal = float(input('Enter credit principal: '))
        # if choice in ["n", "p"]:
        #     monthly_payment = float(input('Enter monthly payment: '))
        # if choice != "n":
        #     periods = int(input('Enter count of periods: '))

        if args.payment and args.principal:
            n = math.ceil(
                math.log((args.payment / (args.payment - credit_interest * args.principal)), 1 + credit_interest))
            years = n // 12
            months = n % 12
            if years == 0:
                print(f'You need {months} months to repay this credit!')
            elif months == 0:
                print(f'You need {years} years to repay this credit!')
            else:
                print(f'You need {years} years and {months} months to repay this credit!')
            print(f'Overpayment = {args.principal - math.ceil(args.payment * n)}')
        elif args.payment and args.periods:
            c_principal = math.floor(args.payment / (
                    (credit_interest * math.pow(1 + credit_interest, args.periods)) / (
                        math.pow(1 + credit_interest, args.periods) - 1)))
            print(f'Your credit principal = {c_principal}!')
            print(f'Overpayment = {math.ceil((args.payment * args.periods) - c_principal)}')
        else:
            annuity = math.ceil((args.principal * credit_interest) / (1 - math.pow(1 + credit_interest, - args.periods)))
            print(f'Your annuity payment = {annuity}!')
            print(f'Overpayment = {math.ceil((annuity * args.periods) - args.principal)}')
    elif args.type == 'diff':
        all_payments = 0
        for i in range(args.periods):
            diff_payment = math.ceil((args.principal / args.periods) + (
                        credit_interest * (args.principal - ((args.principal * (i + 1 - 1)) / args.periods))))
            all_payments += diff_payment
            print(f'Month {i + 1}: paid out {diff_payment}')
        print(f'Overpayment = {args.principal - all_payments}')
