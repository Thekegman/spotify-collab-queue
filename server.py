from flask import Flask, request, send_from_directory, render_template
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
@app.route('/queue')
def send_queue():
    up_next = music_queue.get_queue()
    if up_next:
        text_str = "UP NEXT:\n"
        for i, track in enumerate(up_next):
            text_str += "{}. {}\n".format(i+1,track['name'])
        output_list = text_str[:-1].split('\n')
    else:
        output_list = ["0 Songs in queue."]
    html =  render_template("text_window.html",text =output_list )
    return html
@app.route('/clear_queue')
def send_clear():
    music_queue.clear()
    return "cleared"

@app.route('/skip')
def send_skip():
    music_queue.skip()
    return "skipped"

@app.route('/', methods=['GET'])
def root():
    if 'name' in request.args:
        print(request.args.get('name'))
        response_text = music_queue.add(request.args.get('name'))
        html =  render_template("text_window.html",text = response_text.split("\n"))
        return html
    else:
        return app.send_static_file('index.html')
	

if __name__ == "__main__":
    music_queue = play_a_song.MusicQueue()
    app.run(debug=False,host='0.0.0.0')
