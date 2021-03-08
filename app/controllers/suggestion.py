from re import search
from app import (
    app, 
    Resource, 
    reqparse,
    jwt_required,
    get_jwt_identity)
from app.models.suggestion import Suggestion    

class SuggestionResource(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('title',type=str, required=True, help="this field cannot be left blank")
    parser.add_argument('description', type=str, required=True, help="this field cannot be left blank")
    
    #parametro buscas e paginação
    part_params = reqparse.RequestParser()
    part_params.add_argument('title',type=str, required=False)
    part_params.add_argument('limit',type=int, required=False)
    part_params.add_argument('offset',type=int, required=False)
    
    def get(self):
        parameter_data = SuggestionResource.part_params.parse_args()
        
        if parameter_data['limit'] == None:
            parameter_data['limit'] = 8
        
        if parameter_data['offset'] == None:
            parameter_data['offset'] = 0
            
        limit = parameter_data['limit']
        pages = parameter_data['offset'] * parameter_data['limit']
        
   
        if parameter_data['title']:
            suggestions = Suggestion.query.filter_by(title=parameter_data['title']).limit(limit).offset(pages)
            data = []
            for suggestion in suggestions:
                data.append(suggestion.json())
            return {'suggestions': data}
        
        suggestions = Suggestion.query.limit(limit).offset(pages)
        data = []
        for suggestion in suggestions:
            data.append(suggestion.json())
        return {'suggestions': data}
    
    @jwt_required()
    def post(self):
        data = SuggestionResource.parser.parse_args()
        data['user_id'] = get_jwt_identity()
        
        suggestion = Suggestion(**data)
        
        try:
            suggestion.save_suggestion()
            return {'message': 'suggestion has been created successfully.'}, 201
        except:
            return {'message': 'An error occurred creating the suggestion.'}, 500
        

class SuggestionsDetailResource(Resource):  
    parser = reqparse.RequestParser()
    parser.add_argument('title',type=str, required=True, help="title field cannot be left blank")
    parser.add_argument('description', type=str, required=True, help="description field cannot be left blank")
    
    def get(self, id):
        suggestion = Suggestion.find_by_suggestion(id)
        if suggestion:
            return {'suggestions': suggestion.json()}
        return {'message': 'suggestion not found'}, 404
    
    @jwt_required()
    def put(self, id):
        data = SuggestionResource.parser.parse_args()
        user_id = get_jwt_identity()
        suggestion = Suggestion.find_by_suggestion(id)
        if suggestion.user_id == user_id:
            try:
                suggestion.update_suggestion(**data)
                suggestion.save_suggestion()
                return suggestion.json(), 200
            except:
                return {'message': 'An error occurred update the suggestion.'}, 500
        return {'message': 'suggestion not found'}, 404

    @jwt_required()
    def delete(self, id):
        suggestion = Suggestion.find_by_suggestion(id)
        user_id = get_jwt_identity()
        
        if suggestion.user_id == user_id:
            try:
                suggestion.delete_suggestion()
                return {'suggestions': 'suggestion successfully deleted'}, 200
            except:
                return {'message': 'An error occurred deleted the suggestion.'}, 500
        return {'message': 'suggestion not found'}, 404

