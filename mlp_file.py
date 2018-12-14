from sklearn.neural_network import MLPClassifier
from sklearn.model_selection import train_test_split
import pandas as pd
import numpy as np
import time
import matplotlib.pyplot as plt
from sklearn.metrics import confusion_matrix
import helper

file_name = 'leomds94_eeg_gesture.csv'

class_names = ["Neutro", "Agarrar", "Rock", "Hang Loose", "Legal", "Pulso"]


mlp = MLPClassifier(activation='tanh', hidden_layer_sizes=(26,20), max_iter=10000, alpha=1,
                    solver='lbfgs', verbose=False, tol=1e-8)

def train_mlp():
    dataset = pd.read_csv(file_name, header=0)

    data = dataset.iloc[:, :].values

    np.random.shuffle(data)

    X = data[:, :14]
    for i in range(len(X)):
        X[i] /= 100

    y = data[:, 14:]

    X_train, X_test, y_train, y_test = \
        train_test_split(X, y, test_size=.2, random_state=42)

    print("vai")
    start = time.time()
    mlp.fit(X, y.ravel())
    end = time.time()
    print("Iter number: " + str(mlp.n_iter_))
    print("Tempo de treinamento: " + str(round(end - start, 2)) + " segundos")
    y_pred = mlp.predict(X_test)
    print("Training set score: %f" % mlp.score(X_train, y_train))
    print("Test set score: %f" % mlp.score(X_test, y_test))

    cnf_matrix = confusion_matrix(y_test, y_pred)
    np.set_printoptions(precision=2)
    plt.figure()
    helper.plot_confusion_matrix(cnf_matrix, classes=class_names,
                          title='Matriz de confusão')
    plt.show()

    
def run_mlp(eeg_values):
    for i in range(len(eeg_values)):
        eeg_values[i] /= 100
    return mlp.predict([eeg_values])
