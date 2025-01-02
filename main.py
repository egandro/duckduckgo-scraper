from flask import Flask, jsonify, abort
from duckduckgo_search import DDGS
from duckduckgo_search.exceptions import DuckDuckGoSearchException
import time
import random
import os

app = Flask(__name__)

class MaxRetriesExceededException(Exception):
    """Custom exception for exceeding maximum retries."""
    pass

def ddgs_text(query, max):
    ddgs = DDGS()
    # region="us-en", timelimit="y",
    res = ddgs.text(keywords=query, max_results=max)
    result = []
    if isinstance(res, list) and len(res) > 0:
        result = [
            item['href']
            for item in res
            if 'href' in item and item['href'] is not None and item['href'] != ""
        ]
    return result

def scraper(query, max=1):
    max_retries = 5
    retry_count = 0

    while retry_count < max_retries:
        try:
            result = ddgs_text(query,max)
            break
        except DuckDuckGoSearchException as e:
            retry_count += 1
            if retry_count >= max_retries:
                raise MaxRetriesExceededException(f"Maximum retries reached: {e}")
            else:
                sleep_time = random.randint(2, 30)
                print(f"Caught an exception: {e} - Retrying in {sleep_time} seconds...")
                time.sleep(sleep_time)
    return result

@app.route('/scrape/<string:query>')
def scrape(query):
    result = scraper(query)
    return jsonify(result)

@app.route('/scrape/<int:max>/<string:query>')
def scrape_with_max(max, query):
    if not isinstance(max, int):
        abort(400, description="Invalid value for 'max'. It must be an integer.")

    result = scraper(query,max)
    return jsonify(result)

@app.errorhandler(404)
def not_found(error):
    return jsonify({'error': 'Not found'}), 404

if __name__ == '__main__':
    port = os.getenv('PORT', 5000)
    #app.run(port=port, debug=True)
    app.run(host='0.0.0.0', port=port)