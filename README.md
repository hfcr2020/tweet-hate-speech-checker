# Tweet Hate Speech Checker
Tweet Hate Speech Checker is an application that provides an user interface to
receive short strings and predict whether it is considered hate speech or not.

## Stack
The application uses Flask to provide the `validate` API. This API loads a
deep learning model using RNN and custom classes and functions to trim the
input and vectorize the data. 
