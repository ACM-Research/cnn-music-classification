import os
import librosa
import youtube_dl
from flask import Flask, request, render_template
from tensorflow import keras
from werkzeug.utils import secure_filename

app = Flask(__name__)

@app.route("/", methods=['GET', 'POST'])
def home():
    if request.method == 'POST':
        if 'song' in request.files:
            if not request.files['song']:
                return 'No song found'
            file = request.files['song']
            filename = secure_filename(file.filename)
            file.save('static/' + filename)
        elif 'youtube_url' in request.form:
            filename = secure_filename(request.form['youtube_url'] + '.mp3')
            ytdl_options = {
                'format': 'bestaudio/best',
                'postprocessors': [{
                    'key': 'FFmpegExtractAudio',
                    'preferredcodec': 'mp3',
                    'preferredquality': '192',
                }],
                'outtmpl': 'static/' + filename
            }
            with youtube_dl.YoutubeDL(ytdl_options) as ytdl:
                try:
                    ytdl.download([request.form['youtube_url']])
                except:
                    return 'An error occurred. Either the link is invalid or the download failed. If you are sure the link is correct, retry using the same link.'
        else:
            return 'No song found'
        try:
            predictions = predict('static/' + filename)
        except:
            return 'Invalid audio file. Please upload a valid mp3 file.'
        return render_template('results.html', filename=filename, predictions=predictions, enumerate=enumerate)
    return render_template('prompt.html')

model = keras.models.load_model('trained_model')

SR = 22050
TOTAL_SAMPLES = 29 * SR
NUM_SLICES = 10
SAMPLES_PER_SLICE = int(TOTAL_SAMPLES / NUM_SLICES)

genre_dict = {
    0 : "blues",
    1 : "classical",
    2 : "country",
    3 : "disco",
    4 : "hiphop",
    5 : "jazz",
    6 : "metal",
    7 : "pop",
    8 : "reggae",
    9 : "rock",
}

def predict(filepath):
    song, sampling_rate = librosa.load(filepath)
    start_sample = len(song) // 2
    end_sample = start_sample + SAMPLES_PER_SLICE

    mfcc = librosa.feature.mfcc(y=song[start_sample:end_sample], sr=sampling_rate, n_mfcc=13).T.reshape((1, 125, 13, 1))

    prediction = model.predict(mfcc)[0]

    res_dict = {}
    for i, confidence in enumerate(prediction):
        res_dict[genre_dict[i]] = confidence
    
    return dict(reversed(sorted(res_dict.items(), key=lambda item: item[1])))

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=os.environ.get('PORT', 5000))