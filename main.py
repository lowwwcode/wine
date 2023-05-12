from datetime import datetime
from pprint import pprint

from dateutil.relativedelta import relativedelta
from http.server import HTTPServer, SimpleHTTPRequestHandler
from jinja2 import Environment, FileSystemLoader, select_autoescape
import pandas
import collections


def right_ending_of_year(_year):
    last_digit = _year % 10
    last_two_digits = _year % 100
    if last_two_digits in (11, 12, 13, 14):
        return 'лет'
    if last_digit == 1:
        return 'год'
    elif last_digit in (2, 3, 4):
        return 'года'
    else:
        return 'лет'


def main():
    env = Environment(
        loader=FileSystemLoader('.'),
        autoescape=select_autoescape(['html', 'xml'])
    )

    age_of_company = datetime.now() - relativedelta(years=1920)

    products_raw = pandas.read_excel('wine2.xlsx', keep_default_na=False).to_dict(orient='records')
    print(products_raw)
    products_by_categories = collections.defaultdict(list)
    for product in products_raw:
        products_by_categories[product["Категория"]].append(product)

    prices = []
    for product in products_raw:
        prices.append(product['Цена'])
    min_price = min(prices)

    template = env.get_template('templates/index_template.html')
    rendered_output = template.render(age=age_of_company.year,
                                      year=right_ending_of_year(age_of_company.year),
                                      products_by_categories=products_by_categories,
                                      min_price=min_price)

    with open('index.html', 'w', encoding="utf8") as file:
        file.write(rendered_output)

    server = HTTPServer(('0.0.0.0', 8000), SimpleHTTPRequestHandler)
    server.serve_forever()


if __name__ == '__main__':
    main()
