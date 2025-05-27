from pyclassify.utils import read_config
from pyclassify import kNN
import random
import argparse

def read_file(filename):
    X = []
    y = []
    with open(filename) as f:
        for line in f:
            values = line.split(',')
            y.append(0 if values[-1][0] == 'b' else 1)
            X.append([float(i) for i in values[:-1]])
    return X, y

def parse_command_line_arguments():
    parser = argparse.ArgumentParser()
    parser.add_argument('--config', type=str, default="experiments/config")
    return parser.parse_args()


def main(filename):
    kwargs = read_config(filename)
    data_file = kwargs['dataset']
    k = kwargs['k']
    x, y = read_file(data_file)
    idx_shuffle = [i for i in range(len(x))]
    idx_shuffle = random.sample([i for i in range(len(x))], len(x))
    x = [x[i] for i in idx_shuffle]
    y = [y[i] for i in idx_shuffle]
    test_size = int(len(x) * .2)
    x_train, x_test = x[:test_size], x[test_size:]
    y_train, y_test = y[:test_size], y[test_size:]

    knn = kNN(k)
    knn((x_train, y_train), x_test)
    print(f"Accuracy: {(sum([i == j for i, j in zip(y_test,
                                                    knn.predicted)])/len(x_test)): .2f}")


if __name__ == "__main__":
    parser = parse_command_line_arguments()
    main(parser.config)