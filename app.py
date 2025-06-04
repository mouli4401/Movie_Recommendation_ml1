from flask import Flask, render_template, request
import pickle

app = Flask(__name__)

# Load data and similarity matrix
movies = pickle.load(open('indian_movies.pkl', 'rb'))
similarity = pickle.load(open('similarity.pkl', 'rb'))

def recommend(movie_name):
    movie_name = movie_name.lower()
    matches = movies[movies['title'].str.lower().str.contains(movie_name)]
    
    if matches.empty:
        return ["Movie not found. Try another."]
    
    index = matches.index[0]
    sim_scores = list(enumerate(similarity[index]))
    sim_scores = sorted(sim_scores, key=lambda x: x[1], reverse=True)[1:6]
    
    recommendations = [movies.iloc[i[0]].title for i in sim_scores]
    return recommendations

@app.route('/', methods=['GET', 'POST'])
def home():
    results = []
    if request.method == 'POST':
        movie = request.form['movie']
        results = recommend(movie)
    return render_template('index.html', recommendations=results)

if __name__ == '__main__':
    app.run(debug=True)
