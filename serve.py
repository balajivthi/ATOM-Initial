from waitress import serve
from app import create_app, create_database

app = create_app()
create_database(app)

if __name__ == '__main__':
    # Change the port number in this line
    print("Starting production server on http://localhost:5001")
    serve(app, host='localhost', port=5001, threads=4)  # Use 4 threads for better performance
