import requests
from flask import current_app
from models import db
from models.article import Article

def fetch_and_store_news(country="in", category="general"):
    """
    Optional helper. Call from a Flask context:
    with app.app_context(): fetch_and_store_news()
    """
    api_key = current_app.config.get("NEWSAPI_KEY", "")
    if not api_key or api_key == "replace_me":
        print("NEWSAPI_KEY missing. Skipping fetch.")
        return []

    url = "https://newsapi.org/v2/top-headlines"
    params = {"country": country, "category": category, "apiKey": api_key}

    resp = requests.get(url, params=params, timeout=15)
    if resp.status_code != 200:
        print("Error fetching news:", resp.text)
        return []

    data = resp.json()
    articles = data.get("articles", [])
    stored = []

    for item in articles:
        title = (item.get("title") or "").strip()
        content = (item.get("description") or "No description").strip()
        source = (item.get("source", {}).get("name") or "Unknown").strip()
        if not title:
            continue

        # de-dup by title+source
        if Article.query.filter_by(title=title, source=source).first():
            continue

        # Save under a default user (e.g., system user with id 1)
        article = Article(title=title, content=content, source=source, user_id=1)
        db.session.add(article)
        stored.append(article)

    db.session.commit()
    print(f"Stored {len(stored)} articles")
    return stored
