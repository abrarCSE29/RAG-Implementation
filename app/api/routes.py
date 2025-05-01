from flask import Blueprint, request, jsonify
from app.services.rag_service import RAGService
from pathlib import Path
from werkzeug.utils import secure_filename
import os


api_bp = Blueprint('api', __name__)
rag_service = RAGService()

@api_bp.before_app_request
def initialize_rag():
    file_paths = [
        "app/data/documents/doc1.txt",
        "app/data/documents/doc2.txt",
        "app/data/documents/doc3.txt",
        "app/data/documents/CI.pdf",
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

@api_bp.route('/documents', methods=['GET'])
def get_documents():
    try:
        # Define the documents directory path
        docs_dir = Path("app/data/documents")
        
        # Get all files with .txt or .pdf extension
        documents = []
        if docs_dir.exists():
            for file in docs_dir.iterdir():
                if file.suffix.lower() in ['.txt', '.pdf']:
                    documents.append(file.name)
        
        return jsonify({
            'documents': documents,
            'count': len(documents)
        })
    except Exception as e:
        return jsonify({'error': f"Error fetching documents: {str(e)}"}), 500
    
@api_bp.route('/embed', methods=['POST'])
def embed_documents():
    try:
        # Check if files were uploaded
        if 'files' not in request.files:
            return jsonify({'error': 'No files provided'}), 400

        uploaded_files = request.files.getlist('files')
        
        # Validate files
        if not uploaded_files:
            return jsonify({'error': 'No files selected'}), 400

        # Create documents directory if it doesn't exist
        docs_dir = Path("app/data/documents")
        docs_dir.mkdir(parents=True, exist_ok=True)

        # Save files and collect paths
        saved_files = []
        for file in uploaded_files:
            if file.filename:
                # Secure the filename
                filename = secure_filename(file.filename)
                file_path = docs_dir / filename
                print(f"Saving file to {file_path}")
                # Save the file
                file.save(str(file_path))
                saved_files.append(str(file_path))

        # Initialize RAG service with new documents
        try:
            print(f"Initializing RAG service with files: {saved_files}")
            rag_service.initialize(saved_files)
            
            return jsonify({
                'message': 'Documents embedded successfully',
                'files': [Path(f).name for f in saved_files],
                'count': len(saved_files)
            }), 200
            
        except Exception as e:
            # Clean up saved files if embedding fails
            for file_path in saved_files:
                try:
                    print(f"Removing file {file_path} due to error: {str(e)}")
                except:
                    pass
            raise Exception(f"Error embedding documents: {str(e)}")

    except Exception as e:
        return jsonify({'error': str(e)}), 500