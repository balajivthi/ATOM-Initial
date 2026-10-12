from app import create_app, create_database

app = create_app()

if __name__ == '__main__':
    # Create the database and tables if they don't exist
    create_database(app)
    app.run(debug=True, host=app.config['HOST'], port=app.config['PORT'])