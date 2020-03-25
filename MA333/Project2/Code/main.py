# -*- encode: utf-8 -*-
from analysis import calc_accuracy, dimensionality_reduction
from cfgs import CFGS
from data import day_train, day_test, hour_train, hour_test, time_train, time_test
from debug import debug
from plot import visualize_data
from progress import bar
from regressor import regressors
from timer import Timer
from warn import ignore_warnings


# y's tag
y_tags = ["CASCOL", "REGCOL", "CNTCOL"]
# train and test data(hour or day)
trains = [day_train, hour_train, time_train]
tests  = [day_test,  hour_test, time_test]
index  = 0
# result container
result = dict()
# if process dimensionality reduction
dec_flag = True
# if visualize data
vis_flag = True


if vis_flag:
    visualize_data(trains, is_train=True)
    visualize_data(tests, is_train=False)

for y_tag in y_tags:
    result[y_tag] = dict()
    result[y_tag]["info"] = dict()

    # train and test data
    train_x = trains[index][0]
    train_y = trains[index][-1][CFGS["DATA"][y_tag]]

    test_x = tests[index][0]
    test_y = tests[index][-1][CFGS["DATA"][y_tag]]

    # dimensionality reduction
    if dec_flag:
        decomodel,train_x_ = dimensionality_reduction(train_x, n_dim=6, method="TruncatedSVD")
        test_x_ = decomodel.transform(test_x)
    else:
        train_x_,test_x_ = train_x, test_x

    # sklearn model
    best_score = 0.0
    best_model = None
    fit_time   = 0.0
    pred_time  = 0.0
    for regressor in bar(regressors):
        with Timer() as t:
            model = regressor()
            model.fit(train_x_, train_y)
        fit_time = t.toc()
        y_true = test_y.to_numpy().astype(float)
        with Timer() as t:
            y_pred = model.predict(test_x_)
        pred_time = t.toc()
        accuracy = calc_accuracy(y_true, y_pred, display=True)

        result[y_tag]["info"][regressor] = {
            "r2_score":  accuracy["score"]["r2_score"],
            "fit_time":  fit_time,
            "pred_time": pred_time,
        }
        if result[y_tag]["info"][regressor]["r2_score"] > best_score:
            best_score = result[y_tag]["info"][regressor]["r2_score"]
            best_model = model
    result[y_tag]["best"] = {
        "r2_score": best_score,
        "model":    best_model,
    }

debug(locals())
