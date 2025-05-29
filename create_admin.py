from app import create_app, db
from app.models import User

app = create_app()
with app.app_context():
    db.create_all()
    if not User.query.filter_by(username='').first():
        user = User(username='', password_hash='')
        db.session.add(user)
        db.session.commit()
        print('Адміна створено!')
    else:
        print('Адмін вже існує!')
