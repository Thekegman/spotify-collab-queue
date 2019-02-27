from flask import Flask, request, send_from_directory, render_template, session, redirect, url_for
import play_a_song
# set the project root directory as the static folder, you can set others.
app = Flask(__name__, static_url_path='')
app.secret_key = "super secret key"

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
        text_str = "UP NEXT\n"
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
    return redirect(url_for('send_view', text="cleared"), code=303)

@app.route('/skip')
def send_skip():
    music_queue.skip()
    return redirect(url_for('send_view', text="skipped"), code=303)

@app.route('/view')
def send_view():
    Text = request.args.get('text',"")
    return render_template("plain.html",text =Text )

@app.route('/undo', methods=['POST'])
def send_undo():
    print("undo")
    music_queue.drop(session.pop('last_track'))
    return redirect(url_for('root'), code=303)

@app.route('/', methods=['GET', 'POST'])
def root():
    if 'name' in request.form and request.method == 'POST':
        print(request.form.get('name'))
        response_text, added_track_obj = music_queue.add(request.form.get('name'))
        session['last_track'] = added_track_obj
        html =  render_template("added_track_view.html",text = response_text.split("\n"))
        return html
    else:
        return app.send_static_file('index.html')
    
music_queue = play_a_song.MusicQueue()
    
if __name__ == "__main__":
    app.run(debug=False,host='0.0.0.0')
