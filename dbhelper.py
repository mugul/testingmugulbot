import sqlite3
####

class DBHelper:
    def __init__(self, dbname="telebot.sqlite"):
        self.dbname = dbname
        self.conn = sqlite3.connect(dbname)

    def setup(self):
        stmt = "CREATE TABLE IF NOT EXISTS contactos (owner text, nombre text, apellido text, organizacion text, nacionalidad text, cedula text, codarea text, celular text)"
        # Se crean indices para todos los valores
        nombreIndex = "CREATE INDEX IF NOT EXISTS nombreIndex ON contactos (owner,nombre)"
        apellidoIndex = "CREATE INDEX IF NOT EXISTS apellidoIndex ON contactos (owner,apellido)"
        organizacionIndex = "CREATE INDEX IF NOT EXISTS organizacionIndex ON contactos (owner,organizacion)"
        cedulaIndex = "CREATE INDEX IF NOT EXISTS cedulaIndex ON contactos (owner,cedula,nacionalidad)"
        celularIndex = "CREATE INDEX IF NOT EXISTS celularIndex ON contactos (owner,celular,codarea)"

        self.conn.execute(stmt)
        self.conn.execute(nombreIndex)
        self.conn.execute(apellidoIndex)
        self.conn.execute(organizacionIndex)
        self.conn.execute(cedulaIndex)
        self.conn.execute(celularIndex)
        self.conn.commit()


    def add_item(self, owner, nombre, apellido, organizacion, nacionalidad, cedula, codarea, celular):
        stmt = "INSERT INTO contactos (owner, nombre, apellido, organizacion, nacionalidad, cedula, codarea, celular) VALUES (?, ?, ?, ?, ?, ?, ?, ?)"
        args = (owner, nombre, apellido, organizacion, nacionalidad, cedula, codarea, celular)
        self.conn.execute(stmt, args)
        self.conn.commit()

    # def delete_item(self, item_text):
    #     stmt = "DELETE FROM contactos WHERE description = (?)"
    #     args = (item_text, )
    #     self.conn.execute(stmt, args)
    #     self.conn.commit()

    def get_contactos(self, owner):
        stmt = "SELECT nombre,apellido FROM contactos where owner = (?)"
        args = (owner, )
        return [x[0]+" "+x[1] for x in self.conn.execute(stmt, args)]

    def get_info_contacto(self, owner,nombre,apellido):
        stmt = "SELECT * FROM contactos WHERE owner = (?) AND nombre = (?) AND apellido = (?)"
        args = (owner, nombre, apellido, )
        c = self.conn.cursor()
        c.execute(stmt, args)
        return c.fetchone()