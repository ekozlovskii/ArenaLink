from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from sqlalchemy.orm import relationship




db = SQLAlchemy()

# Таблица пользователей (User)

class User(db.Model):
    __tablename__ = 'user'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    login = db.Column(db.String(100), nullable=False, unique=True)
    name = db.Column(db.String(100), nullable=False)
    password = db.Column(db.String(100), nullable=False)
    role = db.Column(db.String(50), nullable=False)  # 'fan' или 'organizer'
    email = db.Column(db.String(255), nullable=True)  # Email теперь опциональный
    contact = db.Column(db.String(255), nullable=True)  # Только для организаторов
    file = db.Column(db.String(255), nullable=True)  # Файл для подтверждения статуса организатора
    notification_preference = db.Column(db.Enum('email', 'telegram', 'vk', 'none', name='notification_enum'), default='none')
    date_create = db.Column(db.DateTime, default=datetime.utcnow)
    date_update = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    def __repr__(self):
        return f'<User {self.name} ({self.role})>'


# Таблица уведомлений (Notifications)
class Notification(db.Model):
    __tablename__ = 'notification'

    notification_id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    message = db.Column(db.Text)
    delivery_method = db.Column(db.Enum('email', 'telegram', 'vk', name='delivery_method_enum'))
    status = db.Column(db.Enum('sent', 'failed', 'pending', name='status_enum'), default='pending')
    date_sent = db.Column(db.DateTime, nullable=True)
    date_create = db.Column(db.DateTime, default=datetime.utcnow)
    date_update = db.Column(db.DateTime, onupdate=datetime.utcnow)

    user = db.relationship('User', backref=db.backref('notifications', lazy=True))


# Таблица матчей (Matches)
# class Match(db.Model):
#     match_id = db.Column(db.Integer, primary_key=True)
#     team_home = db.Column(db.String(100))
#     team_away = db.Column(db.String(100))
#     date_time = db.Column(db.DateTime)
#     location = db.Column(db.String(200))
#     created_by = db.Column(db.Integer, db.ForeignKey('user.id'))
#     date_create = db.Column(db.DateTime, default=datetime.utcnow)
#     date_update = db.Column(db.DateTime, onupdate=datetime.utcnow)

#     created_by_user = db.relationship('User', backref=db.backref('matches', lazy=True))
class Match(db.Model):
    __tablename__ = 'match'

    match_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    match_name = db.Column(db.String(200), nullable=False)  # Название матча
    date_time = db.Column(db.DateTime, nullable=False)  # Дата и время
    stadium_name = db.Column(db.String(200), nullable=False)  # Название стадиона
    stadium_plan = db.Column(db.String(255), nullable=False)  # Путь к загруженной схеме стадиона
    match_type = db.Column(db.Enum('friendly', 'tournament', name='match_type_enum'), nullable=False)  # Тип матча
    ticket_quantity = db.Column(db.Integer, nullable=False)  # Количество билетов
    ticket_price = db.Column(db.Numeric(10, 2), nullable=False)  # Цена билетов
    created_by = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)  # ID организатора
    date_create = db.Column(db.DateTime, default=datetime.utcnow)  # Дата создания
    date_update = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)  # Дата обновления

    created_by_user = db.relationship('User', backref=db.backref('matches', lazy=True))

    def __repr__(self):
        return f'<Match {self.match_name} at {self.stadium_name}>'


# Таблица билетов (Tickets)
class Ticket(db.Model):
    ticket_id = db.Column(db.Integer, primary_key=True)
    match_id = db.Column(db.Integer, db.ForeignKey('match.match_id'))
    sector = db.Column(db.String(100), nullable=True)
    row = db.Column(db.Integer, nullable=True)
    seat = db.Column(db.Integer, nullable=True)
    price = db.Column(db.Numeric, nullable=True)
    current_owner = db.Column(db.Integer, db.ForeignKey('user.id'))
    status = db.Column(db.Enum('available', 'sold', 'reserved', name='ticket_status_enum'))
    date_create = db.Column(db.DateTime, default=datetime.utcnow)
    date_update = db.Column(db.DateTime, onupdate=datetime.utcnow)

    match = db.relationship('Match', backref=db.backref('tickets', lazy=True))
    owner = db.relationship('User', backref=db.backref('owned_tickets', lazy=True))


# Таблица заказов (Orders)
class Order(db.Model):
    order_id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    ticket_id = db.Column(db.Integer, db.ForeignKey('ticket.ticket_id'))
    status = db.Column(db.Enum('paid', 'cancelled', name='order_status_enum'))
    date_create = db.Column(db.DateTime, default=datetime.utcnow)
    date_update = db.Column(db.DateTime, onupdate=datetime.utcnow)

    user = db.relationship('User', backref=db.backref('orders', lazy=True))
    ticket = db.relationship('Ticket', backref=db.backref('orders', lazy=True))

# История изменений пользователя (User_History)
class UserHistory(db.Model):
    user_history_id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    field_changed = db.Column(db.String(100))
    old_value = db.Column(db.Text)
    new_value = db.Text
    changed_by = db.Column(db.Integer, db.ForeignKey('user.id'))
    date_create = db.Column(db.DateTime, default=datetime.utcnow)

    user = db.relationship('User', foreign_keys=[user_id], backref=db.backref('history', lazy=True))
    changed_by_user = db.relationship('User', foreign_keys=[changed_by], backref=db.backref('changes_made', lazy=True))


# История билетов (Ticket_History)
class TicketHistory(db.Model):
    ticket_history_id = db.Column(db.Integer, primary_key=True)
    ticket_id = db.Column(db.Integer, db.ForeignKey('ticket.ticket_id'))
    previous_owner = db.Column(db.Integer, db.ForeignKey('user.id'))
    new_owner = db.Column(db.Integer, db.ForeignKey('user.id'))
    status = db.Column(db.Enum('available', 'sold', 'returned', name='ticket_status_enum'))
    date_create = db.Column(db.DateTime, default=datetime.utcnow)

    ticket = db.relationship('Ticket', backref=db.backref('history', lazy=True))
    previous_owner_user = db.relationship('User', foreign_keys=[previous_owner])
    new_owner_user = db.relationship('User', foreign_keys=[new_owner])


# Таблица изображений (Images)
class Image(db.Model):
    image_id = db.Column(db.Integer, primary_key=True)
    entity_type = db.Column(db.Enum('match', 'user', name='entity_type_enum'))
    entity_id = db.Column(db.Integer)
    url = db.Column(db.Text)
    date_create = db.Column(db.DateTime, default=datetime.utcnow)
    date_update = db.Column(db.DateTime, onupdate=datetime.utcnow)