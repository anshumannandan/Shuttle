import pandas


def get_country_list():
    file = pandas.read_csv('files/distances.csv')
    data = file.to_csv().strip()
    data = data.split('\n')[0].strip()[3:]
    country_list = data.split(',')
    return country_list