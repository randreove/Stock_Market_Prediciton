# Stock_Market_Prediciton

Today’s stock market is a major influence on the general economy and on the individual economy, allowing companies and individual investors to invest their savings in order to make a profit. Therefore, the prediction of stock values is a very important part of this field, as it can allow to obtain a competitive advantage over competitors or to take advantage and get ahead of the market.

In the present work we have tried to find an Artificial Intelligence model that can successfully perform the task of stock price prediction for Ibex-35 companies. From a data set with the basic daily values of stock prices, it has been decided to add information from technical economic indicators, with the aim of providing more factors that influence the closing price.

For the prediction, 6 different models have been developed combining different strategies and hybrid architectures in order to obtain an accurate model. We have worked on two base models, formed by LSTM and GRU networks, commonly applied on this type of tasks, and two dimensionality reduction methods have been applied on them, such as PCA and AutoEncoder.

After training the different models and evaluating the results it has been observed that the application of PCA algorithms for data dimensionality reduction can help the model to obtain better results, both computational and train. 


**Preprocess execution order:**
1. In /Data_preprocess run EXECUTE_PYTHON_FILES.py. 
2. When it says "from which lists:" indicate "a" and press Enter
3. Repeat this step. This will automatically run all the python scripts needed to download the data from Yahoo Finance, add the technical indicators, perform the preprocessing, export preprocessed data and generate graphs.
5. Apply Model_final.ipynb on the preprocessed data located in /Data_preprocess/Data/Data_preprocessed.
