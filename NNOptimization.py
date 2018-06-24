import pandas as pd
from sklearn.metrics import make_scorer
from sklearn.model_selection import GridSearchCV
from sklearn.metrics import mean_squared_error
from keras.wrappers.scikit_learn import KerasRegressor


class NNOptimization:
    def __init__(self, data, model):
        self.data = data
        self.search_space['neurons'] = [40, 64, 128]
        self.search_space['epochs'] = [50, 100, 150]
        self.search_space['dropout'] = [0.4, 0.5]
        self.raw_model = model
        self.scores = None
        self.configuration = None
        self.KERAS_model = KerasRegressor(build_fn=model, verbose=0)
        self.metric = make_scorer(mean_squared_error, greater_is_better=False)
        self.grid_search = GridSearchCV(estimator=self.KERAS_model
                                        , param_grid=self.search_space
                                        , n_jobs=-1
                                        , scoring=self.metric)

    def start_search(self):
        self.grid_search.fit(self.data['train_x'], self.data['train_y'])

        score_list = []

        best_result = {"Best Score": abs(self.grid_search.best_score_),
                       'Epochs': self.grid_search.best_params_['epochs'],
                       'Neurons': self.grid_search.best_params_['neurons'],
                       'Dropout': self.grid_search.best_params_['dropout']}

        means = self.grid_search.cv_results_['mean_test_score']
        std = self.grid_search.cv_results_['std_test_score']
        params = self.grid_search.cv_results_['params']

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
