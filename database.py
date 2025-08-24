from flask import Flask, request
from flask_restful import Api, Resource, reqparse, abort, fields, marshal_with, marshal
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
api = Api(app)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///nhl_players.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

class PlayerModel(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    full_name = db.Column(db.String(100), nullable=False)
    age = db.Column(db.Integer, nullable=False)
    height = db.Column(db.String(20), nullable=False)
    weight = db.Column(db.Integer, nullable=False)
    position = db.Column(db.String(50), nullable=False)
    jersey_number = db.Column(db.String(10), nullable=False)

    def __repr__(self):
        return f"Player(id={self.id}, name={self.full_name}, position={self.position})"

with app.app_context():
    db.create_all()

player_put_args = reqparse.RequestParser()
player_put_args.add_argument("full_name", type=str, required=True, help="Player's full name is required")
player_put_args.add_argument("age", type=int, required=True, help="Player's age is required")
player_put_args.add_argument("height", type=str, required=True, help="Player's height is required")
player_put_args.add_argument("weight", type=int, required=True, help="Player's weight is required")
player_put_args.add_argument("position", type=str, required=True, help="Player's position is required")
player_put_args.add_argument("jersey_number", type=str, required=True, help="Jersey number is required")

player_update_args = reqparse.RequestParser()
player_update_args.add_argument("full_name", type=str, help="Player's full name")
player_update_args.add_argument("age", type=int, help="Player's age")
player_update_args.add_argument("height", type=str, help="Player's height")
player_update_args.add_argument("weight", type=int, help="Player's weight")
player_update_args.add_argument("position", type=str, help="Player's position")
player_update_args.add_argument("jersey_number", type=str, help="Jersey number")

resource_fields = {
    'id': fields.Integer,
    'full_name': fields.String,
    'age': fields.Integer,
    'height': fields.String,
    'weight': fields.Integer,
    'position': fields.String,
    'jersey_number': fields.String
}

class Player(Resource):
    @marshal_with(resource_fields)
    def get(self, player_id):
        result = PlayerModel.query.filter_by(id=player_id).first()
        if not result:
            abort(404, message=f"Could not find player with ID {player_id}")
        return result

    @marshal_with(resource_fields)
    def put(self, player_id):
        args = player_put_args.parse_args() if request else None
        return self.create_or_update_player(player_id, args)

    def create_or_update_player(self, player_id, player_data, update=False):
        
        if not player_data:
            abort(400, message="Player data is required")
            
        if not update and PlayerModel.query.filter_by(id=player_id).first():
            return {'message': f"Player ID {player_id} already exists"}, 409
            
        if update:
            player = PlayerModel.query.filter_by(id=player_id).first()
            if not player:
                return {'message': f"Player ID {player_id} doesn't exist"}, 404
            for field in ['full_name', 'age', 'height', 'weight', 'position', 'jersey_number']:
                if player_data.get(field) is not None:
                    setattr(player, field, player_data[field])
        else:
            player = PlayerModel(
                id=player_id,
                full_name=player_data['full_name'],
                age=player_data['age'],
                height=player_data['height'],
                weight=player_data['weight'],
                position=player_data['position'],
                jersey_number=player_data['jersey_number']
            )
            db.session.add(player)
        
        db.session.commit()
        return player, 200 if update else 201

    @marshal_with(resource_fields)
    def patch(self, player_id):
        args = player_update_args.parse_args() if request else None
        return self.create_or_update_player(player_id, args, update=True)

    def delete(self, player_id):
        player = PlayerModel.query.filter_by(id=player_id).first()
        if not player:
            abort(404, message=f"Player ID {player_id} doesn't exist")
        db.session.delete(player)
        db.session.commit()
        return '', 204

class PlayerList(Resource):
    @marshal_with(resource_fields)
    def get(self):
        return PlayerModel.query.all()
        
    def post(self, players_data=None):
        # Get data either from request or direct parameter
        if players_data is None:
            if not request:
                abort(400, message="Direct data input required")
            players_data = request.get_json()
        
        if not players_data or not isinstance(players_data, list):
            abort(400, message="Invalid data format. Expected a list of players.")
            
        added_players = []
        errors = []
        player_resource = Player()
        
        for index, player_data in enumerate(players_data):
            try:
                # Generate a unique ID for each player
                player_id = player_data.get('id', index + 1)
                
                # Validate required fields
                required_fields = ['full_name', 'age', 'height', 'weight', 'position', 'jersey_number']
                if not all(field in player_data for field in required_fields):
                    errors.append(f"Missing required fields in player at index {index}")
                    continue
                
                result, status_code = player_resource._create_or_update_player(
                    player_id=player_id,
                    player_data=player_data,
                    update=False
                )
                
                if status_code == 201:
                    added_players.append(result)
                else:
                    errors.append(f"Failed to add player {player_data['full_name']}: {result.get('message', 'Unknown error')}")
                    
            except Exception as e:
                errors.append(f"Error processing player at index {index}: {str(e)}")
        
        response = {
            "message": f"Successfully added {len(added_players)} players",
            "added_players": [marshal(p, resource_fields) for p in added_players],
            "errors": errors
        }
        return response, 201 if added_players else 400

api.add_resource(Player, "/player/<int:player_id>")
api.add_resource(PlayerList, "/players")

if __name__ == "__main__":
    app.run(debug=True)