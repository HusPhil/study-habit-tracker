from flask import Blueprint, request, jsonify
from models.flashcard.flashcard_manager import FlashcardManager
from models.content.linkable_content import LinkableContent

test_routes = Blueprint("test_routes", __name__)  # Define Blueprint
@test_routes.route('/route_tester', methods=['POST'])
def route_tester():
    print(request.form)
    return jsonify({
        'message': 'Route tester endpoint'
    })

@test_routes.route('/create_flashcard', methods=['GET'])
def route_flashcard_test():
    print(request.form)
    my_link: str = "https://www.googlscascsace.com/iojascjnaskcj"

    if not LinkableContent.verify_link(my_link):    
        return jsonify({    
            'error': 'link not valid'
        })
    
    FlashcardManager.create(1, "Test flashcard kom", my_link)

    return jsonify({
        'message': 'Route tester endpoint'
    })
    