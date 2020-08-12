import flask
import datetime
import threading


# app
app = flask.Flask(__name__)


# init
def init():
    words_dict = {}
    stats_dict = {}
    words_counter = 0
    with open("words_clean.txt") as f:
        for line in f:
            word = line.rstrip()
            key = ''.join(sorted(word))
            words_dict.setdefault(key, set()).add(word)
            words_counter += 1
    stats_dict["words_counter"] = words_counter
    stats_dict["requests_counter"] = 0
    stats_dict["processing_timer"] = 0
    return words_dict, stats_dict


words, stats = init()
lock = threading.Lock()


def stat_function(activity_stats):
    def decorator(f):
        def wrapper(*args, **kwargs):
            begin = datetime.datetime.now()
            ret = f(*args, **kwargs)
            end = datetime.datetime.now()
            timer = end - begin
            with lock:
                activity_stats["requests_counter"] += 1
                activity_stats["processing_timer"] += int(timer.total_seconds()*1000*1000)
            return ret
        return wrapper
    return decorator


@app.route('/api/v1/stats')
def api_stats():
    with lock:
        words_counter = stats["words_counter"]
        requests_counter = stats["requests_counter"]
        processing_timer = stats["processing_timer"]
        response = {
            "totalWords": words_counter,
            "totalRequests": requests_counter,
            "avgProcessingTimeNs": processing_timer // requests_counter if requests_counter != 0 else 0,
        }
    return flask.jsonify(response)


@app.route('/api/v1/similar')
@stat_function(stats)
def api_similar():
    word = flask.request.args.get('word')
    key = ''.join(sorted(word))
    similar_words = words.get(key, set())
    if word in similar_words:
        similar_words.remove(word)
    response = {
        "similar": list(similar_words)
    }
    return flask.jsonify(response)