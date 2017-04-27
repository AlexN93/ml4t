"""
Test a learner.  (c) 2015 Tucker Balch
"""

import pandas as pd
import numpy as np
import math
import RTLearner as rt

if __name__ == "__main__":
    input_file = 'ripple.csv'
    data = pd.read_csv('data/' + input_file)
    data = np.array(data)

    if input_file == 'Istanbul.csv':
        data = np.delete(data, np.s_[0], axis=1)

    train_rows = math.floor(0.6 * data.shape[0])
    test_rows = data.shape[0] - train_rows

    # separate out training and testing data
    trainX = data[:train_rows, 0:-1]
    trainY = data[:train_rows, -1]
    testX = data[train_rows:, 0:-1]
    testY = data[train_rows:, -1]

    learner = rt.RTLearner(leaf_size=50, verbose=False)  # create a LinRegLearner
    learner.addEvidence(trainX, trainY)  # train it

    # evaluate in sample
    predY = learner.query(trainX)  # get the predictions
    rmse = math.sqrt(((trainY - predY) ** 2).sum() / trainY.shape[0])
    print
    print "In sample results"
    print "RMSE: ", rmse
    c = np.corrcoef(predY, y=trainY)
    print "corr: ", c[0, 1]

    # evaluate out of sample
    predY = learner.query(testX)  # get the predictions
    rmse = math.sqrt(((testY - predY) ** 2).sum() / testY.shape[0])
    print
    print "Out of sample results"
    print "RMSE: ", rmse
    c = np.corrcoef(predY, y=testY)
    print "corr: ", c[0, 1]