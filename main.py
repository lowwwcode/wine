import json
from datetime import datetime
from pprint import pprint

from dateutil.relativedelta import relativedelta
from http.server import HTTPServer, SimpleHTTPRequestHandler
from jinja2 import Environment, FileSystemLoader, select_autoescape
import pandas

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


df_from_excel = pandas.read_excel('wine.xlsx',
                                  na_values='',
                                  keep_default_na=False,
                                  names=['title', 'grade', 'price', 'image'])
parsed_wines = df_from_excel.to_json(orient='records', force_ascii=False)
json_wines = json.loads(parsed_wines)

template = env.get_template('templates/index_template.html')
age_of_company = datetime.now() - relativedelta(years=1920)


rendered_output = template.render(age=age_of_company.year,
                                  year=right_ending_of_year(age_of_company.year),
                                  json_wines=json_wines)

with open('index.html', 'w', encoding="utf8") as file:
    file.write(rendered_output)

server = HTTPServer(('0.0.0.0', 8000), SimpleHTTPRequestHandler)
server.serve_forever()
