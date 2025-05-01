from flask import Blueprint, request, jsonify
from app.services.rag_service import RAGService

api_bp = Blueprint('api', __name__)
rag_service = RAGService()

@api_bp.before_app_request
def initialize_rag():
    file_paths = [
        "app/data/documents/doc1.txt",
        "app/data/documents/doc2.txt",
        "app/data/documents/doc3.txt",
    ]
    rag_service.initialize(file_paths)

@api_bp.route('/query', methods=['POST'])
def query():
    data = request.get_json()
    question = data.get('question')
    
    if not question:
        return jsonify({'error': 'Question is required'}), 400
        
    try:
        response = rag_service.query(question)
        return jsonify({'response': response})
    except Exception as e:
        return jsonify({'error': str(e)}), 500