from NNOptimization import NNOptimization
import NNTypes
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

    neural_network = NNTypes

    nntypes = [NNTypes.lstm_type_1, NNTypes.lstm_type_2,
               NNTypes.lstm_type_3, NNTypes.mlp_type_1,
               NNTypes.mlp_type_2, NNTypes.mlp_type_3]

    optimization = NNOptimization(data, NNTypes.lstm_type_1)
    optimization.start_search()
    optimization.save_score_excel('C:/Users/Marcos/Desktop/Notebooks/TCC/Resultados/teste')


