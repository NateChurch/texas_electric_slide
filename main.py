import yaml
import csv
from energy_calc import *

CURRENT_DATA_DIRECTORY = './data/'
PRICES_PATH = CURRENT_DATA_DIRECTORY + 'energy_prices.yaml'
# ENERGY_USAGE_PATH = CURRENT_DATA_DIRECTORY + 'yearlyUsageData_unittest.csv'
ENERGY_USAGE_PATH = CURRENT_DATA_DIRECTORY + 'yearlyUsageData.csv'
OUTPUT_PATH = CURRENT_DATA_DIRECTORY + 'output.csv'
PBI_OUTPUT_PATH = CURRENT_DATA_DIRECTORY + 'pbi_output.csv'

with open(ENERGY_USAGE_PATH, "r") as f:
    for i in range(4):
        f.readline()

    energy_usages = list()
    csv_reader = csv.DictReader(f)
    for row in csv_reader:
        energy_usages.append(row)

with open(PRICES_PATH, "r") as f:
    prices = yaml.load(f, Loader=yaml.FullLoader)

output = dict()
monthly_header = ''
plan_name = 'existing'
print('existing')
output['existing'] = {
    'by_month': {},
    'total_usage': 0,
    'total_cost': 0,
    'avg_monthly': 0,
    'avg_usage': 0
}
for energy_usage in energy_usages:
    if energy_usage['YEAR'] == '':
        continue

    month_name = energy_usage['YEAR'] + '-' + energy_usage['MONTH']
    monthly_header += f",{month_name}_cost, {month_name}_usage"
    # function goes here

    total_monthly_use = float(energy_usage['MONTH_USAGE (kWh)'])
    output[plan_name]['total_usage'] += total_monthly_use

    total_monthly_charge = float(energy_usage['MONTH_COST ($)'])
    output[plan_name]['total_cost'] += total_monthly_charge
    output[plan_name]['by_month'][month_name] = {
        'charge': total_monthly_charge,
        'usage': total_monthly_use,
        'cost_per_kwh': total_monthly_charge / total_monthly_use
    }

output[plan_name]['avg_monthly'] = output[plan_name]['total_cost'] / len(energy_usages)
output[plan_name]['avg_usage'] = output[plan_name]['total_usage'] / len(energy_usages)

for plan in prices:

    plan_name = plan['provider'] + '_' + plan['name']
    print(f"{plan_name}")
    output[plan_name] = {
        'by_month': {},
        'total_usage': 0,
        'total_cost': 0,
        'avg_monthly': 0,
        'avg_usage': 0
    }
    for energy_usage in energy_usages:
        total_monthly_use = float(energy_usage['MONTH_USAGE (kWh)'])
        output[plan_name]['total_usage'] += total_monthly_use

        total_monthly_charge = determine_plan_cost(plan=plan, usage=total_monthly_use)
        output[plan_name]['total_cost'] += total_monthly_charge
        month_name = energy_usage['YEAR'] + '-' + energy_usage['MONTH']

        output[plan_name]['by_month'][month_name] = {
            'charge': total_monthly_charge,
            'usage': total_monthly_use,
            'cost_per_kwh': total_monthly_charge / total_monthly_use
        }

    output[plan_name]['avg_monthly'] = output[plan_name]['total_cost'] / len(energy_usages)
    output[plan_name]['avg_usage'] = output[plan_name]['total_usage'] / len(energy_usages)

header_row = f"plan_name,total_cost,total_usage,avg_monthly,avg_usage{monthly_header}\n"

with open(OUTPUT_PATH, 'wt') as f:
    f.writelines(header_row)
    for plan_key, plan_value in output.items():
        row_string = ""
        for month_key, month_value in plan_value['by_month'].items():
            row_string += f",{month_value['charge']},{month_value['usage']}"

        f.writelines(
            f"{plan_key},{plan_value['total_cost']},{plan_value['total_usage']},{plan_value['avg_monthly']},{plan_value['avg_usage']}{row_string}\n")

with open(PBI_OUTPUT_PATH, 'wt') as f:
    f.writelines(f"plan,month,charge,usage,per_kwh\n")
    for plan_key, plan_value in output.items():
        row_string = ""
        for month_key, month_value in plan_value['by_month'].items():
            row_string = f"{plan_key},{month_key},{month_value['charge']},{month_value['usage']},{month_value['cost_per_kwh']}\n"
            f.writelines(row_string)
