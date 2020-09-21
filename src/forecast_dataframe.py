from src.produce_datasets import *
from src.model_tester import *
from src.dictionaries import *


if __name__ == '__main__':
    df_2020 = feature_space('2020')
    df_2020 = df_2020[df_2020['10'] != 0]
    for column in features:
        if column not in df_2020.columns:
            df_2020[column] = 0


def recovery_model():
    df = pd.read_json('data/training_dataset.json')
    X = df.loc[:,features].values
    X_prime = df_2020.loc[:,features].values
    y_recovery = df.loc[:,['recovery']].values * 1
    y_delta = df.loc[:,['delta']].values * 1
    y_decline = df.loc[:,['decline']].values * 1    
    X_train, X_test, y_train, y_test = train_test_split(X, y_recovery, test_size=.2, stratify = y_recovery)
    scaler = StandardScaler()
    scaler.fit(X_train)
    X_train = scaler.transform(X_train)
    X_test = scaler.transform(X_test)
    X_prime = scaler.transform(X_prime)
    recovery_model = RFC(bootstrap=True, ccp_alpha=0.0, class_weight=None,
                        criterion='gini', max_depth=15, max_features='auto',
                        max_leaf_nodes=None, max_samples=None,
                        min_impurity_decrease=0.0, min_impurity_split=None,
                        min_samples_leaf=10, min_samples_split=2,
                        min_weight_fraction_leaf=0.0, n_estimators=100,
                        n_jobs=None, oob_score=False, verbose=1,
                        warm_start=False)
    recovery_model.fit(X_train, y_train)
    recov_predict =  recovery_model.predict(X_prime)                    
    recov_likelihood = recovery_model.predict_proba(X_prime)
    df_2020['recov_predict'] = recov_predict
    df_2020['recov_likelihood'] = recov_likelihood[:,1:]
    df_2020.to_json('data/prediction_2020.json')
    return df_2020

