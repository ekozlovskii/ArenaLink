# ✅ Создаем ОДИН экземпляр Flask
app = Flask(__name__)
base_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))# Формируем путь к базе данных
instance_path = os.path.join(base_dir, 'instance')
db_path = os.path.join(instance_path, 'arenalink.db')
app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{db_path}'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = os.getenv('FLASK_SECRET_KEY', 'fallback_secret')