#%%
from hal import HAL 
from sklearn.datasets import make_blobs
import numpy as np
import fire


def run(path, outfile, classifier = 'rf', seed=0):
    X = np.genfromtxt(path, delimiter=',')
    X = X[1:, 1:].T
    np.random.seed(seed)
    model = HAL(
        clf_type = classifier
    )  # using linear SVMs (fastest) for agglomeration. Other options are 'rf' and 'nb' (random forest, and naive bayes)
    # builds model -> will save data in file info_hal
    model.fit(X)

    # rendering of results using javascript (with optional feature naming)
    feature_name = [line.split(',')[0] for line in open(path, 'r').readlines()][1:]
    model.plot_tree(feature_name = feature_name)

    # Now that your model is fitted, can predict on data (either new or old), using a cross-validation score of 0.95
    ypred = model.predict(X, cv=0.95)
    np.savetxt(outfile + '.pred.txt', ypred)

    # The fitted model information is in directory info_hal. To reload that information for later use, just:
    model.load()

    # To load t-SNE coordinates:
    coord = model.load('tsne')
    np.savetxt(outfile + '.tsne.coord.txt', coord)

if __name__ == '__main__':
    fire.Fire(run)