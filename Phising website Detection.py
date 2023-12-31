# -*- coding: utf-8 -*-
"""Phishing.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/13zxPDAPTOBA0pmiUIYmFJBPDNS91V6sK

# Pre-processing

## Loading and cleaning the data

Download the dataset from [Kaggle link](https://www.kaggle.com/datasets/akashkr/phishing-website-dataset) and download as ```dataset.csv```.
"""

import pandas as pd
import numpy as np

df = pd.read_csv('dataset.csv')
df

df.info()

df.describe()

df.isnull().sum()

# Remove duplicates
df = df.drop_duplicates()

# Handle missing values
df = df.dropna()

col=df.columns
for i in col:
     if  i!='index':
        print(i,df[i].unique())

import matplotlib.pyplot as plt

plt.hist(df.Result)

c1 = df[ df['Result'] == -1]['index'].count()
c2 = df[ df['Result'] == 1]['index'].count()

print('no. of Result with value -1 is :' , c1)
print('no. of Result with value 1 is :' , c2)

"""## Dimensionality Reduction"""

#to find the correlation between attributes
df_corr = df.corr()
df_corr

df_corr.Result.size

#drop the column that have correlation less than 0.03

columns = df_corr.Result[df_corr.Result.abs() > 0.03].index
print(columns.size ,columns, sep = '\n')

df_new  = df[columns]
df_new

X = df_new.iloc[:, :-1].values
Y = df_new.Result.values

"""## Train Test Split"""

from sklearn.model_selection import train_test_split
X_train, X_test, Y_train, Y_test  = train_test_split(X, Y, test_size = 0.3, random_state =23)
print(f'X_train.shape = {X_train.shape} \nX_test.shape = {X_test.shape} \nY_train.shape = {Y_train.shape} \nY_test.shape = {Y_test.shape}')

"""# Classification"""

#plot roc_curve

def plot_roc(Y_true, prediction, label) :
  fpr,tpr,thresh = roc_curve(Y_true,prediction)
  plt.title('ROC curve')
  plt.plot(fpr,tpr,'g',label = label)
  plt.xlabel("False positive rate")
  plt.ylabel("True positive rate")
  plt.grid()
  plt.legend()

from sklearn.metrics import confusion_matrix, ConfusionMatrixDisplay
import itertools

# This function prints and plots the confusion matrix

def plot_confusion_matrix(cm, classes, normalize = False, title='Confusion matrix', cmap = plt.cm.Blues) :

    if normalize :
        cm = cm.astype('float') / cm.sum(axis = 1)[:, np.newaxis]
        print('Normalized Confusion matrix')
    else:
        print(cm)

    plt.imshow(cm, interpolation='nearest', cmap = cmap)
    plt.title(title)
    plt.colorbar()
    tick_marks = np.arange(len(classes))
    plt.xticks(tick_marks, classes, rotation=45)
    plt.yticks(tick_marks, classes)

    fmt = '.2f' if normalize else 'd'
    thresh = cm.max() / 2

    for i, j in itertools.product(range(cm.shape[0]), range(cm.shape[1])) :
        plt.text(j, i, format(cm[i, j], fmt),
                horizontalalignment = 'center',
                color = 'white' if cm[i, j] > thresh else 'black')
    plt.tight_layout()
    plt.ylabel('True Label')
    plt.xlabel('Predicted label')
    plt.show()

"""## Random Forest"""

from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import precision_score, recall_score, f1_score, classification_report,accuracy_score,roc_curve,auc, confusion_matrix

#RFC model
rfc = RandomForestClassifier()
rfc = rfc.fit(X_train, Y_train)
prediction_rfc = rfc.predict(X_test)

# Calculate accuracy , precision, recall, and f1-score
precision_rf = precision_score(Y_test, prediction_rfc)
recall_rf = recall_score(Y_test,prediction_rfc)
f1_rf = f1_score(Y_test, prediction_rfc)
accuracy_rf = accuracy_score(Y_test, prediction_rfc)

# Print the results
print("Accuracy:",accuracy_rf)
print('Precision:', precision_rf)
print('Recall:', recall_rf)
print('F1-score:', f1_rf)

plot_roc(Y_test, prediction_rfc, 'RF classifier')

cm_rfc = confusion_matrix(Y_test, prediction_rfc, labels = [1, -1])
plot_confusion_matrix(cm_rfc, ['PhishingURL', 'NotPhishingURL'], normalize=False)

"""## K Nearest Neigbour"""

from sklearn.neighbors import KNeighborsClassifier

knn = KNeighborsClassifier()
knn = knn.fit(X_train, Y_train)
prediction_knn = knn.predict(X_test)

# Calculate accuracy , precision, recall, and f1-score
precision_knn = precision_score(Y_test, prediction_knn)
recall_knn = recall_score(Y_test,prediction_knn)
f1_knn = f1_score(Y_test, prediction_knn)
accuracy_knn = accuracy_score(Y_test, prediction_knn)
# Print the results
print("Accuracy:",accuracy_knn)
print('Precision:', precision_knn)
print('Recall:', recall_knn)
print('F1-score:', f1_knn)

plot_roc(Y_test, prediction_knn, 'KNN classifier')

cm_knn = confusion_matrix(Y_test, prediction_knn, labels = [1, -1])
plot_confusion_matrix(cm_knn, ['PhishingURL', 'NotPhishingURL'], normalize=False)

"""## Naive Bayes"""

from sklearn.naive_bayes import GaussianNB

gaus = GaussianNB()
gaus.fit(X_train, Y_train)
prediction_gaus = gaus.predict(X_test)


# Calculate accuracy , precision, recall, and f1-score
precision_nb = precision_score(Y_test, prediction_gaus, labels = [1, -1])
recall_nb = recall_score(Y_test,prediction_gaus, labels = [1, -1])
f1_nb = f1_score(Y_test, prediction_gaus, labels = [1, -1])
accuracy_nb = accuracy_score(Y_test, prediction_gaus)
# Print the results
print("Accuracy:",accuracy_nb)
print('Precision:', precision_nb)
print('Recall:', recall_nb)
print('F1-score:', f1_nb)

?precision_score

plot_roc(Y_test, prediction_gaus, 'Naive Bayes classifier')

tn, fp, fn, tp = confusion_matrix(Y_test, prediction_gaus).ravel()
print(tp, fp, fn, tn)
x = tp / (tp + fp)
print(x)

cm_gaus = confusion_matrix(Y_test, prediction_gaus)
plot_confusion_matrix(cm_gaus, ['PhishingURL', 'NotPhishingURL'], normalize=False)

plt.title('ROC curve')

fpr,tpr,thresh = roc_curve(Y_test, prediction_rfc)
plt.plot(fpr,tpr,label = 'Random Forest')

fpr,tpr,thresh = roc_curve(Y_test, prediction_knn)
plt.plot(fpr,tpr,label = 'KNN')

fpr,tpr,thresh = roc_curve(Y_test, prediction_gaus)
plt.plot(fpr,tpr,label = 'Naive Bayes')

plt.xlabel("False positive rate")
plt.ylabel("True positive rate")
plt.grid()
plt.legend()

