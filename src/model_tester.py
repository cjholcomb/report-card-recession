from src.dictionaries import *

import pandas as pd
import io
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

from sklearn.decomposition import PCA
from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import train_test_split, cross_val_score


from sklearn.model_selection import GridSearchCV

from sklearn.linear_model import LogisticRegression as LRC
from sklearn.neighbors import KNeighborsClassifier as KNN
from sklearn.tree import DecisionTreeClassifier as DTC
from sklearn.ensemble import RandomForestClassifier as RFC
from sklearn.ensemble import GradientBoostingClassifier as GBC
from sklearn.svm import SVC
# import xgboost.XGBClassifier as XGBC

import xgboost as XGB

from sklearn.linear_model import LinearRegression as LRR
from sklearn.neighbors import KNeighborsRegressor as KNR
from sklearn.tree import DecisionTreeRegressor as DTR
from sklearn.ensemble import RandomForestRegressor as RFR
from sklearn.ensemble import GradientBoostingRegressor as GBR
from sklearn.svm import SVR
# import xgboost.XGBRegressor as XGBR

from sklearn.metrics import confusion_matrix
from sklearn.metrics import roc_auc_score
from sklearn.metrics import accuracy_score
from sklearn.metrics import precision_score
from sklearn.metrics import recall_score
from sklearn.metrics import f1_score
from sklearn.metrics import r2_score

def train_split(arget):
    '''
    Imports and splits the dataset according to designated target.

    References in test_regressors and test_classifiers

    params:target, str, one of ['recovery', 'delta', 'decline']
    returns: four dataframes, X_train, X_test, y_train, y_test'''

    df = pd.read_json('data/training_dataset.json')
    df = df.dropna()
    X = df.loc[:,features].values
    y_target = df.loc[:,[target]].values * 1
    # y_target = y_target.reshape(len(y_target),)
    X_train, X_test, y_train, y_test = train_test_split(X, y_target, test_size=.2, stratify = y_target)
    scaler = StandardScaler()
    scaler.fit(X_train)
    X_train = scaler.transform(X_train)
    X_test = scaler.transform(X_test)
    return X_train, X_test, y_train, y_test

def instan_dumb_classifiers():
    ''' creates seven types of classifier models with default parameters. Used for comparison to tuned models.
    Intended for delta or decline as target.

    params = None
    returns = list of instanstiated classifier models.'''
    models = []
    models.append(LRC())
    models.append(DTC())
    models.append(KNN())
    models.append(RFC())
    models.append(GBC())
    models.append(SVC())
    models.append(XGB.XGBClassifier())
    return models

def instan_dumb_regressors():
    ''' creates seven types of regressor models with default parameters. Used for comparison to tuned models.
    Intended for delta or decline as target.

    params = None
    returns = list of instanstiated classifier models.'''
    models = []
    models.append(LRR())
    models.append(DTR())
    models.append(KNR())
    models.append(RFR())
    models.append(GBR())
    models.append(SVR())
    models.append(XGB.XGBRegressor())
    return models

def instan_tuned_classifiers():
    ''' creates seven types of models with tuned parameters. Used for comparison to dumb models.

    params = None
    returns = list of instanstiated classifier models.'''
    models = []
    models.append(LRC(C=0.1, class_weight=None, dual=False, fit_intercept=False,
                    intercept_scaling=1, l1_ratio=None, max_iter=500,
                    multi_class='auto', n_jobs=None, penalty='none',
                     solver='sag', tol=0.0001, verbose=0,
                    warm_start=False))
    models.append(DTC(ccp_alpha=0.0, criterion='gini',
                        max_depth=None, max_features='auto', max_leaf_nodes=None,
                        min_impurity_decrease=0.0, min_impurity_split=0,
                        min_samples_leaf=1, min_samples_split=2,
                        min_weight_fraction_leaf=0, presort='deprecated',
                         splitter='best'))
    models.append(KNN(algorithm='ball_tree', leaf_size=10, metric='manhattan',
                      metric_params=None, n_jobs=None, n_neighbors=1, p=1,
                      weights='uniform'))
    models.append(RFC(bootstrap=True, ccp_alpha=0.0, class_weight=None,
                        criterion='gini', max_depth=15, max_features='auto',
                        max_leaf_nodes=None, max_samples=None,
                        min_impurity_decrease=0.0, min_impurity_split=None,
                        min_samples_leaf=10, min_samples_split=2,
                        min_weight_fraction_leaf=0.0, n_estimators=100,
                        n_jobs=None, oob_score=False, verbose=0,
                        warm_start=False))
    models.append(GBC(ccp_alpha=0.0, criterion='friedman_mse', init=None,
                            learning_rate=0.1, loss='deviance', max_depth=3,
                            max_features='auto', max_leaf_nodes=None,
                            min_impurity_decrease=0.0, min_impurity_split=None,
                            min_samples_leaf=1, min_samples_split=2,
                            min_weight_fraction_leaf=0.0, n_estimators=100,
                            n_iter_no_change=None, presort='deprecated',
                            subsample=1.0, tol=0.0001,
                            validation_fraction=0.1, verbose=0, warm_start=True))
    models.append(SVC(C=0.1, break_ties=False, cache_size=200, coef0=0.0,
                        decision_function_shape='ovo', degree=1, gamma='scale', kernel='rbf',
                        max_iter=100, probability=True, shrinking=True, tol=0.001,
                        verbose=False))
    models.append(XGB.XGBClassifier(base_score=0.5, booster='gbtree', colsample_bylevel=1,
               colsample_bynode=1, colsample_bytree=1, eta=0.1, gamma=5,
               learning_rate=0.1, max_delta_step=0, max_depth=10,
               min_child_weight=10, missing=None, n_estimators=100, n_jobs=1,
               nthread=None, objective='binary:logistic', 
               reg_alpha=0, reg_lambda=1, sampling_method='uniform',
               scale_pos_weight=1, seed=None, silent=None, subsample=0.7,
               tree_method='auto', verbosity=1))
    return models

def instan_tuned_regressors():
    ''' creates seven types of models with tuned parameters. Used for comparison to dumb models.

    params = None
    returns = list of instanstiated classifier models.'''
    models = []
    models.append(LRR(class_weight=None, dual=False, fit_intercept=False,
                    intercept_scaling=1, l1_ratio=None, max_iter=500,
                    multi_class='auto', n_jobs=None, penalty='none',
                     solver='sag', tol=0.0001, verbose=0,
                    warm_start=False))
    models.append(DTR(ccp_alpha=0.0, criterion='gini',
                        max_depth=None, max_features='auto', max_leaf_nodes=None,
                        min_impurity_decrease=0.0, min_impurity_split=0,
                        min_samples_leaf=1, min_samples_split=2,
                        min_weight_fraction_leaf=0, presort='deprecated',
                         splitter='best'))
    models.append(KNR(algorithm='ball_tree', leaf_size=10, metric='manhattan',
                      metric_params=None, n_jobs=None, n_neighbors=1, p=1,
                      weights='uniform'))
    models.append(RFR(bootstrap=True, ccp_alpha=0.0, class_weight=None,
                        criterion='gini', max_depth=15, max_features='auto',
                        max_leaf_nodes=None, max_samples=None,
                        min_impurity_decrease=0.0, min_impurity_split=None,
                        min_samples_leaf=10, min_samples_split=2,
                        min_weight_fraction_leaf=0.0, n_estimators=100,
                        n_jobs=None, oob_score=False, verbose=0,
                        warm_start=False))
    models.append(GBR(ccp_alpha=0.0, criterion='friedman_mse', init=None,
                            learning_rate=0.1, loss='deviance', max_depth=3,
                            max_features='auto', max_leaf_nodes=None,
                            min_impurity_decrease=0.0, min_impurity_split=None,
                            min_samples_leaf=1, min_samples_split=2,
                            min_weight_fraction_leaf=0.0, n_estimators=100,
                            n_iter_no_change=None, presort='deprecated',
                            subsample=1.0, tol=0.0001,
                            validation_fraction=0.1, verbose=0, warm_start=True))
    models.append(SVR(C=0.1, break_ties=False, cache_size=200, coef0=0.0,
                        decision_function_shape='ovo', degree=1, gamma='scale', kernel='rbf',
                        max_iter=100, probability=True, shrinking=True, tol=0.001,
                        verbose=False))
    models.append(XGB.XGBRegressor(base_score=0.5, booster='gbtree', colsample_bylevel=1,
               colsample_bynode=1, colsample_bytree=1, eta=0.1, gamma=5,
               learning_rate=0.1, max_delta_step=0, max_depth=10,
               min_child_weight=10, missing=None, n_estimators=100, n_jobs=1,
               nthread=None, objective='binary:logistic', 
               reg_alpha=0, reg_lambda=1, sampling_method='uniform',
               scale_pos_weight=1, seed=None, silent=None, subsample=0.7,
               tree_method='auto', verbosity=1))
    return models



def fit_models(models, target, X_train, X_test, y_train, y_test):
    for model in models:
        model.fit(X_train, y_train)
    return models
()
def test_classifiers(models, target):
    dct = {}  
    for model in models:
        y_predict = model.predict(X_test)
        dct[model] = {}
        dct[model]['AUC'] = roc_auc_score(y_test, y_predict) 
        dct[model]['Accuracy'] = accuracy_score(y_test, y_predict)
        dct[model]['Precision'] = precision_score(y_test, y_predict)
        dct[model]['Recall'] = recall_score(y_test, y_predict)
        dct[model]['f1'] = f1_score(y_test, y_predict)
        cf_matrix = confusion_matrix(y_test, y_predict )
        dct[model]['Confusion Matrix'] = (cf_matrix)
    return dct

def test_regressors(models, target):
    dct = {}  
    for model in models:
        dct[model] = {}
        dct[model]['AUC'] = r2_score(y_test, model.predict(X_test))
    return dct

if __name__ == '__main__':
    X_train, X_test, y_train, y_test = train_split('recovery')


