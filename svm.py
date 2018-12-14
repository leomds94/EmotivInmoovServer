import matplotlib.pyplot as plt
from sklearn import svm
from sklearn.model_selection import train_test_split
from sklearn.metrics import confusion_matrix
import pandas as pd
import numpy as np
import itertools

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

# Load data from https://www.openml.org/d/554
dataset = pd.read_csv(file_name, header=0)

data = dataset.iloc[:,:].values

np.random.shuffle(data)

X = data[:, :14]
for i in range(len(X)):
    X[i] /= 1000
y = data[:, 14:]

# rescale the data, use the traditional train/test split
X_train, X_test, y_train, y_test = \
        train_test_split(X, y, test_size=.2, random_state=42)

classifier = svm.SVC(kernel='poly', C=1, decision_function_shape='ovr', probability=False)

classifier.fit(X_train, y_train)

y_pred = classifier.predict(X_test)

print("Training set score: %f" % classifier.score(X_train, y_train))
print("Test set score: %f" % classifier.score(X_test, y_test))

# Compute confusion matrix
if file_name == 'leomds94_eeg.csv':
    y_test_non_category = [ np.argmax(t) for t in y_test ]
    y_predict_non_category = [ np.argmax(t) for t in y_pred ]
    cnf_matrix = confusion_matrix(y_test_non_category, y_predict_non_category)
else:
    cnf_matrix = confusion_matrix(y_test, y_pred)
np.set_printoptions(precision=2)

# Plot non-normalized confusion matrix
plt.figure()
class_names = ["neutral", "grab", "rock", "cool", "thumb", "forearm"]
plot_confusion_matrix(cnf_matrix, classes=class_names,
                      title='Confusion matrix, without normalization')

plt.show()