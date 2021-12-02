# -*- coding: utf-8 -*-
"""Heart Disease.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/12o899G1Y62rvarRt8TQqwHkB2OxDeuHv
"""

# Commented out IPython magic to ensure Python compatibility.
import numpy as np
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
# % matplotlib inline

heart_df = pd.read_csv('/content/heart.csv')

heart_df.head()

heart_df.columns

heart_df.describe

sns.heatmap(heart_df.isnull(),yticklabels=False,cbar=False,cmap='viridis')

"""It means none of the data is missing.

"""

sns.set_style('whitegrid')
sns.countplot(x='HeartDisease', data=heart_df, palette='rocket')

sns.set_style('whitegrid')
sns.countplot(x='HeartDisease', data=heart_df, hue= 'Sex', palette='rocket')

"""In general, males have higher chances of having a heart disease."""

sns.set_style('whitegrid')
sns.countplot(x='HeartDisease', data=heart_df, hue= 'ExerciseAngina', palette='rocket')

sns.set_style('whitegrid')
sns.countplot(x='HeartDisease', data=heart_df, hue= 'ST_Slope', palette='rocket')

sns.set_style('whitegrid')
sns.countplot(x='HeartDisease', data=heart_df, hue= 'FastingBS', palette='rocket')

sns.distplot(heart_df['Age'].dropna(),kde=False,color='darkred',bins=30)

heart_df['ST_Slope'].unique()

heart_df['ChestPainType'].unique()

"""'Age', 'Sex', 'ChestPainType', 'RestingBP', 'Cholesterol', 'FastingBS',
       'RestingECG', 'MaxHR', 'ExerciseAngina', 'Oldpeak', 'ST_Slope',
       'HeartDisease'
"""

heart_df['RestingECG'].unique()

RestingECG = pd.get_dummies(heart_df['RestingECG'],drop_first=True)
ChestPainType = pd.get_dummies(heart_df['ChestPainType'],drop_first=True)
ST_Slope = pd.get_dummies(heart_df['ST_Slope'],drop_first=True)
Sex = pd.get_dummies(heart_df['Sex'],drop_first=True)
ExerciseAngina = pd.get_dummies(heart_df['ExerciseAngina'],drop_first=True)

heart_df.drop(['ST_Slope', 'ChestPainType', 'RestingECG', 'Sex', 'ExerciseAngina'],axis=1,inplace=True)
heart_df = pd.concat([heart_df, Sex, ST_Slope, ChestPainType, RestingECG, ExerciseAngina],axis=1)
heart_df.head()

heart_df.count()

from sklearn.model_selection import train_test_split

X_train, X_test, y_train, y_test = train_test_split(heart_df.drop('HeartDisease',axis=1), 
                                                    heart_df['HeartDisease'], test_size=0.25, 
                                                    random_state=101)

from sklearn.linear_model import LogisticRegression

logmodel = LogisticRegression()
logmodel.fit(X_train,y_train)
y_pred_log = logmodel.predict(X_test)

from sklearn.ensemble import RandomForestClassifier
clf=RandomForestClassifier(n_estimators=275)
clf.fit(X_train,y_train)
y_pred_clf = clf.predict(X_test)

from sklearn.metrics import classification_report

print(classification_report(y_test,y_pred_log))

print(classification_report(y_test,y_pred_clf))

heart_df['Oldpeak'].unique()

from sklearn.preprocessing import MinMaxScaler
scaler = MinMaxScaler()
X_train = scaler.fit_transform(X_train)
X_test = scaler.transform(X_test)

import tensorflow as tf
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense, Activation,Dropout
from tensorflow.keras.constraints import max_norm
from tensorflow.keras.callbacks import EarlyStopping

model = Sequential()

# input layer
model.add(Dense(128,  activation='relu'))
model.add(Dropout(0.5))

# hidden layer
model.add(Dense(64, activation='relu'))
model.add(Dropout(0.4))

# hidden layer
model.add(Dense(32, activation='relu'))
model.add(Dropout(0.3))

# output layer
model.add(Dense(units=1,activation='sigmoid'))

# Compile model
model.compile(loss='binary_crossentropy',
              optimizer=tf.keras.optimizers.Adam(learning_rate=0.00007),
              metrics=['binary_accuracy'])

early_stop = EarlyStopping(monitor='binary_accuracy', mode='max', verbose=1, patience=10)

model.fit(x=X_train, 
          y=y_train, 
          epochs=150,
          batch_size=16,
          validation_split = 0.1, 
          callbacks=[early_stop]
          )

prob = model.predict(X_test)

y_pred_NN=np.where(prob[:,] > 0.5, 1, 0)

y_pred_NN[:5]

print(classification_report(y_test,y_pred_NN))

