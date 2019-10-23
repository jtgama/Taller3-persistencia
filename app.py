from flask import Flask, render_template, request, redirect, url_for, flash
from flask_mysqldb import MySQL



app = Flask(__name__)
app.config['MYSQL_HOST'] = 'localhost' 
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = ''
app.config['MYSQL_DB'] = 'participantesp'
mysql = MySQL(app)

app.secret_key = "mysecretkey"

@app.route('/')
def Index():
    curs = mysql.connection.cursor()
    curs.execute('SELECT * FROM participantes')
    dato = curs.fetchall()
   
    return render_template('index.htm', participantes =  dato)

@app.route('/add_partici', methods=['POST'])
def add_partici():
    if request.method == 'POST':
        cedula =request.form['cedula']
        nombre = request.form['nombre']
        actividad = request.form['actividad']
        imagen = request.form['imagen']
        estrato= request.form['estrato']
        curs = mysql.connection.cursor()
        curs.execute("INSERT INTO participantes (cedula, nombre, actividad,imagen,estrato) VALUES (%s,%s,%s,%s,%s)",
         (cedula, nombre, actividad,imagen,estrato))
        mysql.connection.commit()
        flash('Participante Agregado Con Exito')
        return redirect(url_for('Index'))
      
    return 'add_partici'
@app.route('/edit_partici/<id>')
def get_partici(id):
    curs= mysql.connection.cursor()
    curs.execute('SELECT * FROM participantes WHERE id=%s',((id)))
    dato= curs.fetchall()
    print(dato[0])
    return render_template('editar_participantes.htm', participantes = dato[0])

@app.route('/actualizar/<id>', methods = ['POST'])   
def actualizar_partici(id):
  if request.method == 'POST':
        cedula =request.form['cedula']
        nombre = request.form['nombre']
        actividad = request.form['actividad']
        imagen = request.form['imagen']
        estrato= request.form['estrato']
        curs = mysql.connection.cursor()
        curs.execute("""
            UPDATE participantes
            SET cedula = %s,
                actividad = %s,
                nombre = %s,
                imagen = %s,
                estrato = %s
            WHERE id = %s
        """, (cedula, actividad, nombre,imagen,estrato, id))
        flash('Participante Actualizo Con Exito')
        mysql.connection.commit()
        return redirect(url_for('Index'))

@app.route('/delete_partici/<string:id>')
def delete_partici(id):
   curs = mysql.connection.cursor()
   curs.execute('DELETE FROM  participantes WHERE  id={0}'.format(id))
   mysql.connection.commit()
   flash('Participante Eliminado Exitosamente')
   return redirect(url_for('Index')) 

if __name__ == '__main__':
    app.run(port=3000, debug= True)