from NNOptimization import NNOptimization
from NNTypes import NNTypes
from Preprocessor import PreProcessor
from pandas import read_csv


def get_csv(path):
    return read_csv(path).drop(columns=['Unnamed: 0'])


if __name__ == "__main__":
    path = 'C:/Users/Marcos/Desktop/Notebooks/TCC/Notebooks/training_dataset.csv'
    data = get_csv(path)

    pre_processing = PreProcessor(data)
    pre_processing.normalization()
    pre_processing.sliding_window(5, 10)
    pre_processing.split_train_test()
    pre_processing.split_in_out(5, 17)
    pre_processing.set_numpy_format()

    data = pre_processing.get_data()

    neural_network = NNTypes()
    nn_types = [NNTypes.mlp_type_1, NNTypes.mlp_type_2,
                NNTypes.mlp_type_3, NNTypes.lstm_type_1,
                NNTypes.lstm_type_2, NNTypes.lstm_type_3]

    for j in nn_types:
        optimization = NNOptimization(data, j)
        optimization.start_search()
        print(j.__name__ + ":" + optimization.get_configuration())
        optimization.save_score_excel(str(j.__name__))

