# app.py

from flask import Flask, request, jsonify
from flask_restx import Api, Resource
from flask_sqlalchemy import SQLAlchemy
from schemas import movie_schema, movies_schema
from models import *

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['RESTX_JSON'] = {'ensure_ascii': False, 'indent': 3}

db = SQLAlchemy(app)

api = Api(app)
movie_ns = api.namespace('movies')

# Возвращает список всех фильмов наше БД
@movie_ns.route("/")
class MoviesView(Resource):

    def get(self): # получение списка сущностей
        movie_with_genre_and_director = db.session.query(Movie.id, Movie.title, Movie.description, Movie.rating, Movie.trailer, Genre.name.label('genre'), Director.name.label('director')).join(Genre).join(Director)
        # представление возвращает только фильмы с определенным режиссером и жанром по запросу типа: /movies/?director_id=2&genre_id=4
        director_id = request.args.get('director_id')
        genre_id = request.args.get('genre_id')
        if director_id:
            movie_with_genre_and_director = movie_with_genre_and_director.filter(Movie.director_id == director_id)
        if genre_id:
            movie_with_genre_and_director = movie_with_genre_and_director.filter(Movie.genre_id == genre_id)

        all_movies = movie_with_genre_and_director.all()

        return movies_schema.dump(all_movies), 200

    def post(self): # создание новой записи
        req_json = request.json
        new_movie = Movie(**req_json)
        with db.session.begin():
            db.session.add(new_movie)
        return f"Объект c id {new_movie.id} создан!", 201

#Возвращает информацию по конкретному фильму (movie_id)
@movie_ns.route("/<int:movie_id>")
class MovieView(Resource):

    def get(self, movie_id: int): # получаем фильм по movie_id, который задаём сами
        movie = db.session.query(Movie).get(movie_id)
        if movie:
            return jsonify(movie_schema.dump(movie))
        return "Такого фильма нет", 404

    def patch(self, movie_id: int): # частичное обновление (не всех полей) сущности по movie_id (обновляем выборочные поля)
        movie = db.session.query(Movie).get(movie_id)
        if not movie:
            return "Такого фильма нет", 404

        req_json = request.json
        if 'title' in req_json:
            movie.title = req_json['title']
        elif 'description' in req_json:
            movie.description = req_json['description']
        elif 'trailer' in req_json:
            movie.trailer = req_json['trailer']
        elif 'year' in req_json:
            movie.year = req_json['year']
        elif 'rating' in req_json:
            movie.rating = req_json['rating']
        elif 'genre_id' in req_json:
            movie.genre_id = req_json['genre_id']
        elif 'director_id' in req_json:
            movie.director_id = req_json['director_id']
        db.session.add(movie)
        db.session.commit()
        return f"Объект c id {movie_id} обновлён!", 201

    def put(self, movie_id: int): # обновляем все поля сущности по movie_id
        movie = db.session.query(Movie).get(movie_id)
        if not movie:
            return "Такого фильма нет", 404

        req_json = request.json
        movie.title = req_json['title']
        movie.description = req_json['description']
        movie.trailer = req_json['trailer']
        movie.year = req_json['year']
        movie.rating = req_json['rating']
        movie.genre_id = req_json['genre_id']
        movie.director_id = req_json['director_id']
        db.session.add(movie)
        db.session.commit()
        return f"Объект c id {movie_id} обновлён!", 201

    def delete(self, movie_id: int): # обновляем сущность из наше БД по movie_id
        movie = db.session.query(Movie).get(movie_id)
        if not movie:
            return "Такого фильма нет", 404
        db.session.delete(movie)
        db.session.commit()
        return f"Объект c id {movie_id} удалён!", 204

if __name__ == '__main__':
    app.run(debug=True)
