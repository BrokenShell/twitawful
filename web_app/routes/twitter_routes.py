from flask import Blueprint, render_template
from web_app.models import db, User, Tweet
from web_app.services.twitter_service import api as twitter_api_client
from web_app.services.basilica_service import connection as basilica_api_client


twitter_routes = Blueprint("twitter_routes", __name__)


@twitter_routes.route("/users/<screen_name>")
def get_user(screen_name=None):
    print(screen_name)

    twitter_user = twitter_api_client.get_user(screen_name)
    statuses = twitter_api_client.user_timeline(screen_name,
                                                tweet_mode="extended",
                                                count=150)
    print("STATUSES COUNT:", len(statuses))
    db_user = User.query.get(twitter_user.id) or User(id=twitter_user.id)
    db_user.screen_name = twitter_user.screen_name
    db_user.name = twitter_user.name
    db_user.location = twitter_user.location
    db_user.followers_count = twitter_user.followers_count
    db.session.add(db_user)
    db.session.commit()
    all_tweet_texts = [status.full_text for status in statuses]
    embeddings = list(
        basilica_api_client.embed_sentences(all_tweet_texts, model="twitter"))
    print("NUMBER OF EMBEDDINGS", len(embeddings))

    counter = 0
    for status in statuses:
        print(status.full_text)
        print("----")
        db_tweet = Tweet.query.get(status.id) or Tweet(id=status.id)
        db_tweet.user_id = status.author.id
        db_tweet.full_text = status.full_text
        embedding = embeddings[counter]
        print(len(embedding))
        db_tweet.embedding = embedding
        db.session.add(db_tweet)
        counter += 1
    db.session.commit()
    return render_template("user.html", user=db_user, tweets=statuses)
