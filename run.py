from app import create_app
from app.config.settings import Config

app = create_app(Config)

if __name__ == '__main__':
    app.run(debug=True)