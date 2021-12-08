from flask import Flask

app = Flask(__name__)


@app.route('/', methods=['GET'])
def say_hello():
    hello_dict = {"hello": "dict"}
    return hello_dict


@app.route('/feed', methods=['GET'])
def get_feeds():
    return "This returns all the feeds"


@app.route('/feed/<int:feed_id>', methods=['GET'])
def get_feed(feed_id):
    return "This returns one feed by ID"


@app.route('/feed', methods=['POST'])
def add_feed():
    return "This adds a new feed."


@app.route('/feed/<int:feed_id>', methods=['PUT', 'PATCH'])
def edit_feed(feed_id):
    return "This updates a feed by ID."


@app.route('/feed/<int:feed_id>', methods=['DELETE'])
def delete_feed(feed_id):
    return "This removes a feed by ID."


if __name__ == "__main__":
    app.run(debug=True)