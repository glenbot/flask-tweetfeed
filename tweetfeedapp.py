import re
import feedparser
from datetime import datetime
from flask import Flask, Markup, render_template, request
from forms import SearchForm

# init the flask app
app = Flask(__name__)
app.debug = True

# site settings
SITE_URL = 'http://127.0.0.1:5000'

# feed settings
BASE_FEED_URL = 'http://search.twitter.com/search.atom?q=%s'

# context processors
@app.context_processor
def contxt_proc():
    contexts = {
        'STATIC_URL': '/static',
        'SITE_NAME':'Tweetfeed'        
    }
    return contexts

# template filters
@app.template_filter('twitterize')
def twitterize_filter(tweet):
    # add links to hashtags
    hash_url = r'<a href="%s/?q=\1">#\1</a>' % SITE_URL
    hash_pattern = re.compile('#([^\W\s]+)')
    tweet = re.sub(hash_pattern, hash_url, tweet)    
    
    # add links to @ replies
    reply_url = r'<a href="http://twitter.com/\1">@\1</a>'
    reply_pattern = re.compile('@([^\W\s]+)')
    tweet = re.sub(reply_pattern, reply_url, tweet)
    
    # safe to return tweet as html
    return Markup(tweet)

@app.template_filter('humanize_date')
def humanize_date_filter(date):
    date = datetime(*date[:-3])
    return date.strftime("%A, %b %d %Y @ %I:%M")

# url handlers
@app.route("/", methods=['GET'])
def index():
    entries = None
    form = SearchForm(request.args)
    if request.method == 'GET' and form.validate():
        data = form.q.data
        if data:
            # query has to use + and not space to
            # pull correct data
            data = data.replace(' ','+')
        feed_url = BASE_FEED_URL % data
        f = feedparser.parse(feed_url)
        entries = f.entries
    return render_template('index.html', form=form, entries=entries)

@app.errorhandler(404)
def page_not_found(error):
    return render_template('404.html'), 404

@app.errorhandler(500)
def page_app_error(e):
    return render_template('500.html'), 500

if __name__ == "__main__":
    app.run(host='0.0.0.0') #server is publicly available