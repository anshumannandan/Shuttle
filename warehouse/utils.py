import pandas
from authentication.utils import CustomError
from joblib import load
import numpy as np


def return_file_content():
    file = pandas.read_csv('files/distances.csv')
    return file.to_csv().strip()

data = return_file_content()


def get_country_list():
    global data
    tdata = data.split('\n')[0].strip()[3:]
    country_list = tdata.split(',')
    return country_list


def get_distance(con1, con2):
    global data
    condata = get_country_list()
    f1 = f2 = None
    for i in range(len(condata)):
        if condata[i] == con1:
            f1 = i+1
        if condata[i] == con2:
            f2 = i+2
    if f1 is None or f2 is None:
        raise CustomError('either of the countries in invalid')
    distance = data.split('\n')[f1].strip()[2:].split(',')[f2]
    return distance


model = load('./Savedmodels/mlmodels.joblib')

def predicted_price(quantity, volume, distance):
    fields = ([[quantity, volume, distance]])
    field= np.array(fields).reshape((1,-1))
    freight = model.predict(field)
    return freight[0]
