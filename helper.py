import itertools
import numpy as np
import matplotlib.pyplot as plt

def finger_translate_mlp(finger):
    if finger == 'thumb':
        return [1, 0, 0, 0, 0, 0]
    elif finger == 'index':
        return [0, 1, 0, 0, 0, 0]
    elif finger == 'middle':
        return [0, 0, 1, 0, 0, 0]
    elif finger == 'ring':
        return [0, 0, 0, 1, 0, 0]
    elif finger == 'pinky':
        return [0, 0, 0, 0, 1, 0]
    elif finger == 'forearm':
        return [0, 0, 0, 0, 0, 1]
    elif finger == 'neutral':
        return [0, 0, 0, 0, 0, 0]

def gesture_translate_mlp(finger):
    if finger == 'neutral':
        return [0]
    elif finger == 'grab':
        return [1]
    elif finger == 'rock':
        return [2]
    elif finger == 'cool':
        return [3]
    elif finger == 'thumb':
        return [4]
    elif finger == 'forearm':
        return [5]

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
