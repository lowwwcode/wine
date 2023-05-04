from datetime import datetime
from pprint import pprint

from dateutil.relativedelta import relativedelta
from http.server import HTTPServer, SimpleHTTPRequestHandler
from jinja2 import Environment, FileSystemLoader, select_autoescape
import pandas
import collections
env = Environment(
    loader=FileSystemLoader('.'),
    autoescape=select_autoescape(['html', 'xml'])
)


def right_ending_of_year(_year):
    reminder = _year % 10
    if _year == 0 or reminder == 0 or reminder >= 5 or _year in range(11, 19):
        return 'лет'
    elif reminder == 1:
        return 'год'
    elif ((_year % 100) >= 10) and ((_year % 100) < 20):
        return 'лет'
    elif _year % 10 > 4:
        return 'лет'
    else:
        return 'года'


collection = pandas.read_excel('wine2.xlsx', keep_default_na=False).to_dict(orient='records')

products_by_categories = collections.defaultdict(list)

for product in collection:
    products_by_categories[product["Категория"]].append(product)

pprint(products_by_categories)

template = env.get_template('templates/index_template.html')
age_of_company = datetime.now() - relativedelta(years=1920)


rendered_output = template.render(age=age_of_company.year,
                                  year=right_ending_of_year(age_of_company.year),
                                  products_by_categories=products_by_categories)

with open('index.html', 'w', encoding="utf8") as file:
    file.write(rendered_output)

server = HTTPServer(('0.0.0.0', 8000), SimpleHTTPRequestHandler)
server.serve_forever()
