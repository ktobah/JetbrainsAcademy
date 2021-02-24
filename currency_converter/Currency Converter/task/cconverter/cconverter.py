import requests
# write your code here!
currency_cache = {}
currency = input()

response = requests.get(f"http://www.floatrates.com/daily/{currency.lower()}.json")
if response.status_code == 200:
    response = eval(response.text)
    if currency.lower() not in ['usd', 'eur']:
        currency_cache[currency.lower()] = {"usd": response['usd']['rate'], "eur": response['eur']['rate']}
    elif currency.lower() == 'usd':
        currency_cache[currency.lower()] = {"eur": response['eur']['rate']}
    elif currency.lower() == 'eur':
        currency_cache[currency.lower()] = {"usd": response['usd']['rate']}

while True:
    target_currency = input()
    if target_currency == "":
        break
    amount = int(input())
    print("Checking the cache…")
    if target_currency in currency_cache[currency.lower()]:
        print("Oh! It is in the cache!")
        print(f"You received {amount * currency_cache[currency.lower()][target_currency.lower()]} {target_currency}.")
    else:
        print("Sorry, but it is not in the cache!")
        response = requests.get(f"http://www.floatrates.com/daily/{currency.lower()}.json")
        if response.status_code == 200:
            response = eval(response.text)
            currency_cache[currency.lower()][target_currency.lower()] = response[target_currency.lower()]['rate']
        print(f"You received {amount * currency_cache[currency.lower()][target_currency.lower()]} {target_currency}.")
