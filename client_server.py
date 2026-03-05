from flask import Flask, send_from_directory, request, jsonify
import paho.mqtt.client as mqtt

# Client web server that serves the web frontend and provides /publish
MQTT_BROKER = "test.mosquitto.org"
MQTT_PORT = 1883
MQTT_TOPIC = "client18"

app = Flask(__name__)


@app.route('/')
def index():
    return send_from_directory('client_app/web', 'index.html')


@app.route('/<path:filename>')
def static_files(filename):
    return send_from_directory('client_app/web', filename)


@app.route('/publish', methods=['GET', 'POST'])
def publish_one():
    if request.method == 'GET':
        return '''\
            <html><body>
            <h3>Publish test</h3>
            <form method="post">
              ID: <input name="id"><br>
              <input type="submit" value="Publish">
            </form>
            </body></html>
        '''

    ident = None
    if request.form:
        ident = request.form.get('id')
    elif request.json:
        ident = request.json.get('id')
    if not ident:
        return jsonify({'error': 'no id provided'}), 400
    broker = request.form.get('broker') or MQTT_BROKER
    mqtt_port = int(request.form.get('mqtt_port') or MQTT_PORT)
    topic = request.form.get('topic') or MQTT_TOPIC
    username = request.form.get('username') or None
    password = request.form.get('password') or None
    try:
        client = mqtt.Client()
        if username:
            client.username_pw_set(username, password)
        client.connect(broker, mqtt_port, 60)
        client.publish(topic, payload=str(ident))
        client.disconnect()
    except Exception as e:
        return jsonify({'error': 'mqtt error: ' + str(e)}), 500
    return jsonify({'sent': 1, 'topic': topic, 'broker': broker})


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5001, debug=True)
