import pytest
from recommender import Recommender


def test_recommender_loads_and_returns_structure():
    r = Recommender('recommendation_model.pkl')
    # expect the object to have recommend_collaborative and recommend_content
    assert hasattr(r, 'recommend_collaborative')
    assert hasattr(r, 'recommend_content')

    # call methods with likely values and ensure dict returned
    out1 = r.recommend_content('test', 3)
    assert isinstance(out1, dict)

    out2 = r.recommend_collaborative('17850', 3)
    assert isinstance(out2, dict)
