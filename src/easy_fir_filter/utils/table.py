from tabulate import tabulate


def show_coefficients_table(coefficients: list[float]):
    data = [[i + 1, value] for i, value in enumerate(coefficients)]
    headers = ["n", "value"]

    return tabulate(data, headers=headers, tablefmt="fancy_grid")
