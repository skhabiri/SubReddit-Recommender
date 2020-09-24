import logging
import random
import pickle

from fastapi import APIRouter
import pandas as pd
from pydantic import BaseModel, Field, validator

log = logging.getLogger(__name__)
router = APIRouter()
loaded_model = pickle.load(open('./app/api/rfclsi_pickle', 'rb'))

def prediction_est(model, input):
  """
  input: text string or list as input
  model: grid search trained model
  returns a pandas series containing the the recommended subreddit names
  """
  if isinstance(input, str):
    input = [input]
  # probability of each class
  proba = model.predict_proba(input)

  # index of the highest probable classes in descending order
  index_proba = [i[0] for i in sorted(enumerate(proba[0]), key=lambda x:x[1])][::-1]
  # Alternative way
  # idx_max = proba[0].argsort()[::-1]

  # get the most probable class names
  return pd.Series(model.classes_[index_proba][:15])


class Item(BaseModel):
    """Use this data model to parse the request body JSON."""

    post_title: str = Field(..., example='banjo')
    post_content: str = Field(..., example='content')
    Image: int = Field(..., example=0)
    Video: int = Field(..., example=0)
    External_link: int = Field(..., example=0)

    def to_df(self):
        """Convert pydantic object to pandas dataframe with 1 row."""
        return pd.DataFrame([dict(self)])

@router.post('/predict')
async def predict(item: Item):
    """
    ### Request Body
    - `post_title`: reddit post title string
    - `post_content`: reddit post content string
    - `Image`: boolean integer for image posts
    - `Video`: boolean integer for video posts
    - `External_link`: boolean integer for external links

    ### Response
    - `prediction`: list of strings, 5 subreddits
    """

    reddit_input = item.post_title + ' ' + item.post_content

    pred = prediction_est(loaded_model, reddit_input)
    
    return {
        'prediction': ", ".join(pred[:5]),
    }
