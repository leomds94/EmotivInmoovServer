import matplotlib.pyplot as plt
from sklearn.neural_network import MLPClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import confusion_matrix
import pandas as pd
import numpy as np
import itertools
import time

def plot_confusion_matrix(cm, classes,
                          normalize=False,
                          title='Confusion matrix',
                          cmap=plt.cm.Blues):
    if normalize:
        cm = cm.astype('float') / cm.sum(axis=1)[:, np.newaxis]
        print("Matriz de confusão normalizada")
    else:
        print('Matriz de confusão, sem normalização')

    print(cm)

    plt.imshow(cm, interpolation='nearest', cmap=cmap)
    plt.title(title)
    plt.colorbar()
    tick_marks = np.arange(len(classes))
    plt.xticks(tick_marks, classes, rotation=45)
    plt.yticks(tick_marks, classes)

    fmt = '.2f' if normalize else 'd'
    thresh = cm.max() / 2.
    for i, j in itertools.product(range(cm.shape[0]), range(cm.shape[1])):
        plt.text(j, i, format(cm[i, j], fmt),
                 horizontalalignment="center",
                 color="white" if cm[i, j] > thresh else "black")

    plt.ylabel('Rótulos verdadeiros')
    plt.xlabel('Rótulos de predição')
    plt.tight_layout()

file_name = 'leomds94_eeg_gesture.csv'
multi_output = False

# Load data from https://www.openml.org/d/554
dataset = pd.read_csv(file_name, header=0)

data = dataset.iloc[:, :].values

np.random.shuffle(data)

X = data[:, :14]
for i in range(len(X)):
    X[i] /= 100

class_names = ["Neutro", "Agarrar", "Rock", "Hang Loose", "Legal", "Pulso"]
y = data[:, 14]

X_train, X_test, y_train, y_test = \
    train_test_split(X, y, test_size=.2, random_state=42)

mlp = MLPClassifier(activation="relu", hidden_layer_sizes=(50,30), max_iter=10000, alpha=1,
                                solver='lbfgs', verbose=False, tol=1e-10)
            
start = time.time()
mlp.fit(X_train, y_train)
y_pred = mlp.predict(X_test)
end = time.time()
print("Iter number: " + str(mlp.n_iter_))
print("Tempo de treinamento: " + str(round(end - start, 2)) + " segundos")
            
print("Training set score: %f" % mlp.score(X_train, y_train))
print("Test set score: %f" % mlp.score(X_test, y_test))
            
            # Compute confusion matrix
if multi_output and file_name == 'leomds94_eeg.csv':
    y_test_non_category = [ np.argmax(t) for t in y_test ]
    y_predict_non_category = [ np.argmax(t) for t in y_pred ]
    cnf_matrix = confusion_matrix(y_test_non_category, y_predict_non_category)
else:
    cnf_matrix = confusion_matrix(y_test, y_pred)
    np.set_printoptions(precision=2)
            
plt.figure()
            
plot_confusion_matrix(cnf_matrix, classes=class_names,
                                  title='Matriz de confusão')
            
plt.show()