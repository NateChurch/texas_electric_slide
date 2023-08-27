


def determine_charge_cost(charge: dict, total_monthly_use: float) -> float:
    """
    Determine the cost of a charge for a given month based on the total monthly usage.

    :param charge: This is one charge in a plan
    :param total_monthly_use: This is the kwh used in a month
    :return: The cost of the charge for the month
    """
    charge_use = 0
    if charge['cost_unit'] == 'cents':
        charge_conversion = .01
    else:
        charge_conversion = 1

    if charge['from_kwh'] <= total_monthly_use:
        charge_use = total_monthly_use - charge['from_kwh']
        if charge['type'] == 'monthly':
            return charge_conversion * charge['cost']

    if charge['to_kwh'] < total_monthly_use:
        charge_use -= total_monthly_use - charge['to_kwh']

    if charge['type'] == 'per_kwh':
        return charge_use * charge_conversion * charge['cost']

    return 0


def determine_plan_cost(plan: dict, usage: float) -> float:
    """
    Determine the cost of a plan for a given month based on the total monthly usage by adding up the cost of each charge.
    :param plan: This is a dictionary of charges for a plan
    :param usage: This is the monthly usage
    :return: This is the total cost of the plan for the month
    """
    total_plan_charge = 0
    for charge in plan['charges']:
        charge_cost = determine_charge_cost(charge=charge, total_monthly_use=usage)
        total_plan_charge += charge_cost

    return total_plan_charge

