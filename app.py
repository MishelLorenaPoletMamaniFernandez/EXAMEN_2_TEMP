from flask import Flask, session, redirect, url_for, request, render_template, flash
from datetime import datetime
import uuid

app = Flask(__name__)
app.secret_key = 'secret_key'  # Necesario para utilizar sesiones


# Función para inicializar la lista de productos en la sesión si no existe
def init_session():
    if 'productos' not in session:
        session['productos'] = []


# Ruta para la página principal, lista de productos
@app.route('/')
def index():
    init_session()
    return render_template('index.html', productos=session['productos'])


# Ruta para agregar un producto
@app.route('/agregar', methods=['POST'])
def agregar_producto():
    init_session()
    
    nombre = request.form.get('nombre')
    cantidad = int(request.form.get('cantidad'))
    precio = float(request.form.get('precio'))
    fecha_vencimiento = request.form.get('fecha_vencimiento')
    categoria = request.form.get('categoria')
    
    # Generar un ID único para cada producto
    id_producto = str(uuid.uuid4())
    
    producto = {
        'id': id_producto,
        'nombre': nombre,
        'cantidad': cantidad,
        'precio': precio,
        'fecha_vencimiento': fecha_vencimiento,
        'categoria': categoria
    }
    
    session['productos'].append(producto)
    flash(f'Producto {nombre} agregado exitosamente')
    
    return redirect(url_for('index'))


# Ruta para eliminar un producto por ID
@app.route('/eliminar/<id>', methods=['POST'])
def eliminar_producto(id):
    init_session()
    session['productos'] = [p for p in session['productos'] if p['id'] != id]
    flash('Producto eliminado correctamente')
    return redirect(url_for('index'))


# Ruta para editar un producto
@app.route('/editar/<id>', methods=['GET', 'POST'])
def editar_producto(id):
    init_session()
    productos = session['productos']
    
    # Buscar el producto por ID
    producto = next((p for p in productos if p['id'] == id), None)
    
    if request.method == 'POST':
        if producto:
            producto['nombre'] = request.form.get('nombre')
            producto['cantidad'] = int(request.form.get('cantidad'))
            producto['precio'] = float(request.form.get('precio'))
            producto['fecha_vencimiento'] = request.form.get('fecha_vencimiento')
            producto['categoria'] = request.form.get('categoria')
            flash('Producto actualizado correctamente')
        return redirect(url_for('index'))
    
    return render_template('editar.html', producto=producto)


# Plantillas HTML
# La página principal mostrará la lista de productos y el formulario de agregar.

@app.route('/formulario_agregar')
def formulario_agregar():
    return render_template('formulario_agregar.html')


if __name__ == '__main__':
    app.run(debug=True)
