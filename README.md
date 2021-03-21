# SubReddit Recommender
This project takes a text as a string or multiple texts in an iterable format such as ndarray or list, and returns a list of recommended Subreddit categories from a list of categories that the model is trained on.
### Virtual environment
This project uses conda as virtual environment. To see a list of conda env enter `conda env list`. To activate env for this project with all the necessary packages use `conda activate SubReddit`. To see the list of installed ipykernels use: `jupyter kernelspec list`. 
After activating the environment launch jupyter lab with `jupyter lab`, and make sure to select `subreddit` kernel from the pull down menu.

Here is a list of files related to the project:
1. praw_db.py:
Connects to PRAW python API for Reddit. Pulls some information from 1000 posts in each of the 44 selected subreddit categories.
The pulled information includes: subreddit name, subreddit id, title, and post body. The pulled information are stored in subreddit_db.sqlite3 .
2. redditmodel_db2.ipynb:
The database contains 51610 rows and 4 columns. We select 100 post for each of 44 Subreddit categories and train different models based on the reduced dataset. The reason for using the smaller dataset is to limit the size of serialized model for heroku app deployment. Here is the list of serialized trained models:
- Spacy embedding vectorizer + KNeighborsClassifier:
  - The dataset is split into training and validation sets. The achieved accuracy is 31% while the baseline is 2.3%. In anticipation of possible issue with running Spacy in the app, the model serialization has been done in 3 steps:
    - preprocess(query, nlp): Takes the text inqury and the spacy model (could be unpickled one), and returns a 300 dimension vectorized embedding representing the post (nlppickle)
    - prediction_spacy(model, input): Feeds the embedding into the trained KNN model and returns a nested list of nearest neighbors distances and their respective indices from the trained data frame (knnpickle)
    - postprocess(kn, df_ser, n): Uses the predicted output and the serialized pandas series as the lookup table and returns n nearest neighbors for the query post (namedf.pkl)
 - A pipeline of TfidfVectorizer + TruncatedSVD + RandomForestClassifier(): Latent Semantic Indexing
  - The benefit of this approach is easier deployment as we only need one smaller pickle. It utilizes the entire sampled dataset, we performed hyperparameter tunning using GridSearchCV(). The accuracy of the trained model is 19%.
- Spacy embedding vectorizer + GradientBoostClassifier:
  - This is a mixed of previous approaches. It used Spacy embedding to improve the accuracy and it also uses RandomizedSearchCV() to perform limitted hyper parameter tunning.The accuracy of the model is 51%.

