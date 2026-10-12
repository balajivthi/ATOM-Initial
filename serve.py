from waitress import serve
from app import create_app, create_database

app = create_app()
create_database(app)

if __name__ == '__main__':
    port = app.config['PORT'] or 5001
    host = app.config['HOST']
    print(f"Starting production server on http://{host}:{port}")
    serve(app, host=host, port=port, threads=4)  # Use 4 threads for better performance