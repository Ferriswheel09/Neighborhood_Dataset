# ml-final-project

## Instructions for navigating the repository

The model itself can be found in [`model.ipynb`](model.ipynb). The rest of the `.py` files represent the web scrapers and data shapers. The final data can be found in [`output3.csv`](output3.csv).

## Setting up the virtual environment

As stated in the report, there is a dependency conflict with `word2vec` and `numpy`. Installing `word2vec` requires `gcc` (which is not obtainable through `pip`). In addition, `word2vec` uses a deprecated version of `numpy`. In order to be compatible with the current version, one line in the `word2vec` files needs to be changed (an instance of `np.float` needs to become simply `float`). That file can be found on line 209 of [this file](venv/lib/python3.10/site-packages/word2vec/wordvectors.py) after you have created your environment. If that link does not work, then you can run the model notebook and the error message should direct you to `wordvectors.py:209` where you can make the change.
