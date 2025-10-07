from flask import Flask

# Create a Flask web server instance
app = Flask(__name__)

# Define a route for the root URL ("/")
@app.route('/')
def hello_world():
    return 'Hello, World!'

# Run the app on host 0.0.0.0 (accessible from outside the container)
# and on port 5000
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
