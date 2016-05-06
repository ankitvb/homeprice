Neural network based price predictor

An artificial neural network was trained used to generate price predictions for a property based on its salient features such as location, date of purchase, type of property, whether it was new construction and whether it was bought outright or backed by a loan. 

Why neural network? Neural networks have been shown to perform as well or better than other techniques for multi-variate regression type problems, the class to which our prediction problem here belongs. 

The open-source deep learning library by Nervana Systems Inc called <a href=“neon.nervanasys.com/“>Neon</a> was used in this work. The input feature vector consisted of the parameters mentioned above. Non-numerical parameters were encoded using one-hot encoding, a <a href=“http://fastml.com/converting-categorical-data-into-numbers-with-pandas-and-scikit-learn/“>standard practice</a> in deep learning for such parameters. The <a href=“https://data.gov.uk/dataset/land-registry-monthly-price-paid-data”>Price Paid dataset</a> for U.K. from 2015 was used for training and testing. The split between training, validation and testing was 60-20-20. The dataset was cleaned to remove any entries for which the above parameters were not available or were out of bounds. Further, extreme outliers with prices over 20,000,000 and under 10,000 were excluded. Early stopping was used to prevent overfitting. The errors on the three sets are given below.

Error on training set: 0.23
Error on validation set: 0.27
Error on test set: 0.26

These errors were measured as the normalized L1 error: &Sigma;|y<sub>i</sub>-t<sub>i</sub>|/&Sigma;t<sub>i</sub> 
where y is the predicted output from the network and t is the target.

As can be appreciated, the level of error is quite high for this to be a commercially viable application. The shortcomings are twofold, in terms of the model as well as data. 

What is still missing in terms of method for a good prediction

What is still missing in terms of data for a good prediction
- need more data, curse of dimensionality
 