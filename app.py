# ServiceDesk Backend Application Entry Point
# 💡 PRESENTATION HINT: "Flask application with factory pattern for scalability"
from app import create_app

# Create Flask application instance using factory pattern
app = create_app()

if __name__ == '__main__':
    # Run development server with debug mode
    app.run(debug=True)
