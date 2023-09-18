from flask import Flask,render_template,request
import pickle
import requests
import json

movies=pickle.load(open('movie_list.pkl','rb'))
similarity=pickle.load(open('similarity.pkl','rb'))

app=Flask(__name__)

def fetch_poster(movie_id):
    url = "https://api.themoviedb.org/3/movie/{}?api_key=63b6b9cc24aab69e989db4c0c6967eae&language=en-US".format(movie_id)
    data = requests.get(url)
    data = data.json()
    poster_path = data['poster_path']
    full_path = "https://image.tmdb.org/t/p/w500/" + poster_path
    return full_path

def recommend(movie):
    index = movies[movies['title'] == movie].index[0]
    distances = sorted(list(enumerate(similarity[index])), reverse=True, key=lambda x: x[1])
    recommended_movie_names = []
    recommended_movie_posters = []
    for i in distances[1:6]:
        # fetch the movie poster
        movie_id = movies.iloc[i[0]].movie_id
        recommended_movie_posters.append(fetch_poster(movie_id))
        recommended_movie_names.append(movies.iloc[i[0]].title)

    return recommended_movie_names,recommended_movie_posters


@app.route('/',methods=['POST','GET'])
def home():
        movie_list = movies['title'].values
        if request.method=='POST':
                movie_name=request.form["movies"]
                to_watch=recommend(movie_name)
                rec_movie= to_watch[0]
                poster= to_watch[1]
                return  render_template("prediction.html",to_watch=to_watch,rec_movie=rec_movie,poster=poster,movie_list=movie_list)
        else:
            return render_template("index.html",movie_list=movie_list)
@app.route("/prediction")        
def prediction():
     return render_template("prediction.html")
     


if __name__=='__main__':
    app.run(debug=True)
