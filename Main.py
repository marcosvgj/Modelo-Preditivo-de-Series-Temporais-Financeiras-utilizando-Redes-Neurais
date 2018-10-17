#!/usr/bin/python

from NNOptimization import NNOptimization
import Preprocessor
from pandas import read_csv
from NNTypes import Model
import time
import os
from pymongo import errors, MongoClient
import json


def get_csv(path):
    return read_csv(path).drop(columns=['Unnamed: 0'])


def armazenar_dados(data):
    host = 'ds155268.mlab.com'
    port = 55268
    user = 'marcosvgj'
    user_password = '*********'
    collection = 'smartbot_database_tcc'

    session = MongoClient(host, port)
    db = session[collection]
    db.authenticate(user, user_password)

    db = session[collection].get_collection('grid_search_result')

    try:
        db.insert_one(data)
        print("Data was successfully inserted in the follow Colletion: %s " % 'grid_search_result')
    except errors.OperationFailure as error:
        print("Could not apply the operation %s" % error)

    session.close()


def print_runtime(seconds, finished=False):
    seconds = int(seconds)
    status = 'has been running for'
    if finished:
        status = 'finished in'

    if seconds < 60:
        print('The script {} {} seconds'.format(status, seconds))
        return
    elif seconds < 3600:
        minutes = seconds // 60
        seconds = seconds - 60 * minutes
        print('The script {} {} minutes & {} seconds'.format(status, minutes, seconds))
        return
    else:
        hours = seconds // 3600
        minutes = (seconds - 3600 * hours) // 60
        seconds = seconds - 3600 * hours - 60 * minutes
        print('The script {} {} hours, {} minutes & {} seconds'.format(status, hours, minutes, seconds))
        return


def main():
    data_path = 'C:/Users/Marcos/Desktop/Notebooks/TCC/Notebooks/training_dataset.csv'
    output_path = 'C:/Users/Marcos/Desktop/Notebooks/TCC/Resultados/'

    data = get_csv(data_path)
    pre_processing = Preprocessor.PreProcessor(data)
    pre_processing.normalization()
    pre_processing.sliding_window(5, 10)
    pre_processing.split_train_test()
    pre_processing.split_in_out(5, 17)
    pre_processing.set_numpy_format()

    data = pre_processing.get_data()

    neural_network = Model.__subclasses__()

    for item in neural_network:
        print("Topology: " + item.__name__)
        new_model = item()
        optimization = NNOptimization(data, new_model.topology)
        optimization.start_search()
        print("Best Configuration: " + json.dumps(optimization.get_configuration(), indent=3, sort_keys=True))
        json_data = {item.__name__: optimization.get_configuration()}
        armazenar_dados(json_data)
        new_path = output_path + item.__name__

        if not os.path.exists(new_path):
            os.makedirs(new_path)
        optimization.save_score_excel(new_path + '/score.xlsx')


if __name__ == "__main__":
    start_time = time.time()
    main()
    print_runtime(time.time() - start_time)







