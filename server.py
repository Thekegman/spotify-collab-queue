from flask import Flask, request, send_from_directory
import play_a_song
# set the project root directory as the static folder, you can set others.
app = Flask(__name__, static_url_path='')

@app.route('/js/<path:path>')
def send_js(path):
    return send_from_directory('js', path)
@app.route('/css/<path:path>')
def send_css(path):
    return send_from_directory('css', path)

@app.route('/fonts/<path:path>')
def send_fonts(path):
    return send_from_directory('fonts', path)

@app.route('/', methods=['GET'])
def root():
	if 'name' in request.args:
		print(request.args.get('name'))
		return play_a_song.im_feeling_lucky(request.args.get('name'))
	else:
		return app.send_static_file('index.html')
	
	
if __name__ == "__main__":
    app.run(debug=False,host='0.0.0.0')