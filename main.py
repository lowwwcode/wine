import argparse
import collections
import os
from datetime import datetime
from http.server import HTTPServer, SimpleHTTPRequestHandler

import pandas
from dateutil.relativedelta import relativedelta
from jinja2 import Environment, FileSystemLoader, select_autoescape


def is_dir_path(string):
    if os.path.isdir(string):
        return string
    else:
        raise NotADirectoryError(string)


def get_right_ending_of_year(_year):
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

    parser = argparse.ArgumentParser()
    parser.add_argument('-path', dest='path', default='wine.xlsx')
    parser.add_argument('-ip', dest='ip_address', default='0.0.0.0')
    parser.add_argument('-port', dest='port', default=8000)
    args = parser.parse_args()

    path_to_excel_file = os.path.normpath(args.path)

    env = Environment(
        loader=FileSystemLoader('.'),
        autoescape=select_autoescape(['html', 'xml'])
    )

    age_of_company = datetime.now() - relativedelta(years=1920)

    parsed_products_from_excel = pandas.read_excel(path_to_excel_file, keep_default_na=False).to_dict(orient='records')

    products_by_categories = collections.defaultdict(list)

    for product in parsed_products_from_excel:
        products_by_categories[product["Категория"]].append(product)

    min_price = min([product['Цена'] for product in parsed_products_from_excel])

    template = env.get_template('templates/index_template.html')
    rendered_output = template.render(age=age_of_company.year,
                                      year=get_right_ending_of_year(age_of_company.year),
                                      products_by_categories=products_by_categories,
                                      min_price=min_price)

    with open('index.html', 'w', encoding="utf8") as file:
        file.write(rendered_output)

    server = HTTPServer((args.ip_address, int(args.port)), SimpleHTTPRequestHandler)
    server.serve_forever()


if __name__ == '__main__':
    main()
