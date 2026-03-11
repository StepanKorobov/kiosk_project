from database.database import Base, get_session, User


def create_tables():
    """Функция создания БД"""

    with get_session() as session:
        Base.metadata.create_all(bind=session)


def add_user(username, telegram_id):
    with get_session() as session:
        user = User(username=username, telegram_id=telegram_id, blocked=False)
        session.add(user)
        session.commit()


# def get_all_kiosks_address():
#     with get_session() as session:
#         kiosks = session.query(Kiosks).all()
#         return kiosks
