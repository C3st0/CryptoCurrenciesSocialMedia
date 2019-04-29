To run the code, open the file Jupiter file here (github we interface), then lauchn it in colab (top icon)

Two versions of the code are the following:

Only the first one is annotated.

**ColabTweetsSentimentAnalysisClean.ipynb** : runs the ANN using the "cleaned" version of the learning dataset (no stop words, lemming, stemming, ...). The code downloads it from our Kaggle repository. Then it downloads the clean tweets data we gathered and runs the classification on it. Finally, it dumps the results in a file (on colab). It needs to be downloaded from there (to use is in subsequent processes), which can be difficult as there is a file size limit to the standard collab file download procedure.

**ColabTweetsSentimentAnalysis.ipynb** : runs the code on the original version of the learning dataset.The code downloads it from the Kaggle repository. Then it downloads the original (untouched) tweets data we gathered and runs the classification on it. Finally, it dumps the results in a file (on colab). It needs to be downloaded from there. 

The final version if the jupiter version to be ran locally, used for test and development purposes.
