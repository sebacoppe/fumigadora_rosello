from app import app, db

with app.app_context():
    db.drop_all()
    db.create_all()
    print("✅ Base de datos reiniciada correctamente.")
# se ejecuta con python reset_db.py
