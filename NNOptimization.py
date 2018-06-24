import pandas as pd
from sklearn.metrics import make_scorer
from sklearn.model_selection import GridSearchCV
from keras.wrappers.scikit_learn import KerasRegressor
from numpy import square
from numpy import subtract


def mean_squared_error(y, y_pred):
    return square(subtract(y, y_pred)).mean()


class NNOptimization:
    def __init__(self, data, model):
        self.data = data
        self.search_space = {'neurons': [40, 64, 128], 'epochs': [50, 100, 150], 'dropout': [0.4, 0.5]}
        self.raw_model = model
        self.scores = None
        self.configuration = None
        self.KERAS_model = KerasRegressor(build_fn=model, verbose=0)
        self.metric = make_scorer(mean_squared_error, greater_is_better=False)

    def start_search(self):
        grid_search = GridSearchCV(estimator=self.KERAS_model
                                   , param_grid=self.search_space
                                   , n_jobs=2
                                   , scoring=self.metric)
        grid_search.fit(self.data['train_x'], self.data['train_y'])

        score_list = []

        best_result = {"Best Score": abs(grid_search.best_score_),
                       'Epochs': grid_search.best_params_['epochs'],
                       'Neurons': grid_search.best_params_['neurons'],
                       'Dropout': grid_search.best_params_['dropout']}

        means = grid_search.cv_results_['mean_test_score']
        std = grid_search.cv_results_['std_test_score']
        params = grid_search.cv_results_['params']

        for mean, stdev, param in zip(means, std, params):
            score_list.append({"RMSE Medio": abs(mean),
                               'RMSE Std': stdev,
                               'Epochs': param['epochs'],
                               'Neurons': param['neurons'],
                               'Dropout': param['dropout']})

        self.scores = pd.DataFrame(score_list)
        self.configuration = best_result

    def save_score_excel(self, excel_file_name):
        self.scores.to_excel(excel_file_name)

    def get_configuration(self):
        return self.configuration
