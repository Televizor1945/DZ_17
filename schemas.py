from marshmallow import Schema, fields

# Схема для получения полей сложной структуры
class MovieSchema(Schema):
    id = fields.Int()
    title = fields.Str()
    description = fields.Str()
    trailer = fields.Str()
    year = fields.Int()
    rating = fields.Float()
    genre = fields.Str()
    genre_id = fields.Int()
    director_id = fields.Int()

# Создам` экземпляры схемы
movie_schema = MovieSchema() #для одного поля
movies_schema = MovieSchema(many=True) # для нескольких полей