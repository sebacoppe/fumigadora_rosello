from flask_mysqldb import MySQL,MySQLdb

mysql = MySQL()


def init_app(app):
    try:
        app.config['MYSQL_HOST'] = 'localhost'
        app.config['MYSQL_USER'] = 'root'
        app.config['MYSQL_PASSWORD'] = ''
        app.config['MYSQL_DB'] = 'fumigadora_rosello'
        mysql.init_app(app)
        print("✅ Conexión a MySQL inicializada correctamente.")
    except Exception as e:
        print("❌ Error al conectar con MySQL:", e)


def get_cursor():
    return mysql.connection.cursor()


def get_dict_cursor():
    return mysql.connection.cursor(MySQLdb.cursors.DictCursor)


