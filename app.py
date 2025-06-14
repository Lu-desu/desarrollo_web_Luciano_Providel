from flask import Flask, render_template, request, redirect, url_for, flash, jsonify, abort
from flask_sqlalchemy import SQLAlchemy
from werkzeug.utils import secure_filename
from models import db, Region, Comuna, Actividad, Foto, ContactarPor, ActividadTema, Comentario
from utils import allowed_file, save_file, format_datetime
from config import Config
import os
from sqlalchemy import desc, func, extract
import json
from datetime import datetime

app = Flask(__name__)
app.config.from_object(Config)

# Inicializar la base de datos
db.init_app(app)

# Asegurar que exista el directorio de subida
os.makedirs(os.path.join(app.root_path, app.config['UPLOAD_FOLDER']), exist_ok=True)

# Rutas existentes
@app.route('/')
def index():
    """Página principal - muestra las últimas 5 actividades"""
    actividades = Actividad.query.order_by(desc(Actividad.id)).limit(5).all()
    return render_template('portada.html', actividades=actividades)

@app.route('/agregar', methods=['GET', 'POST'])
def agregar_actividad():
    """Formulario para agregar actividades"""
    if request.method == 'GET':
        # Mostrar el formulario
        regiones = Region.query.all()
        return render_template('agregar.html', regiones=regiones)
    else:
        # Procesar el formulario enviado
        errores = []
        
        # Validar datos del formulario
        region_id = request.form.get('region')
        comuna_id = request.form.get('comuna')
        sector = request.form.get('sector', '')
        nombre = request.form.get('nombre')
        email = request.form.get('email')
        celular = request.form.get('telefono', '')
        inicio_str = request.form.get('inicio')
        termino_str = request.form.get('termino', '')
        descripcion = request.form.get('descripcion', '')
        tema = request.form.get('tema')
        otro_tema = request.form.get('otroTema', '')
        
        # Validación básica
        if not region_id or not comuna_id or not nombre or not email or not inicio_str or not tema:
            errores.append('Todos los campos obligatorios deben ser completados')
        
        if nombre and len(nombre) > 200:
            errores.append('El nombre no puede exceder los 200 caracteres')
        
        if email and len(email) > 100:
            errores.append('El email no puede exceder los 100 caracteres')
        
        if celular and not celular.startswith('+'):
            errores.append('El formato del teléfono debe ser +XXX.XXXXXXXX')
        
        # Convertir fechas
        inicio_dt = format_datetime(inicio_str) if inicio_str else None
        termino_dt = format_datetime(termino_str) if termino_str else None
        
        if not inicio_dt:
            errores.append('Fecha de inicio inválida')
        
        if termino_dt and inicio_dt and termino_dt <= inicio_dt:
            errores.append('La fecha de término debe ser posterior a la de inicio')
        
        # Validar fotos
        fotos = request.files.getlist('foto')
        if not fotos or not fotos[0].filename:
            errores.append('Se requiere al menos una foto')
        
        if len(fotos) > 5:
            errores.append('No se pueden subir más de 5 fotos')
        
        for foto in fotos:
            if foto.filename and not allowed_file(foto.filename):
                errores.append('Tipo de archivo no permitido. Use PNG, JPG, JPEG o GIF')
        
        # Si hay errores, volver al formulario
        if errores:
            regiones = Region.query.all()
            return render_template('agregar.html', regiones=regiones, errores=errores)
        
        # Crear la actividad
        nueva_actividad = Actividad(
            comuna_id=comuna_id,
            sector=sector,
            nombre=nombre,
            email=email,
            celular=celular,
            dia_hora_inicio=inicio_dt,
            dia_hora_termino=termino_dt,
            descripcion=descripcion
        )
        
        db.session.add(nueva_actividad)
        db.session.flush()  # Obtener ID sin commit
        
        # Agregar tema
        nuevo_tema = ActividadTema(
            tema=tema,
            glosa_otro=otro_tema if tema == 'otro' else None,
            actividad_id=nueva_actividad.id
        )
        db.session.add(nuevo_tema)
        
        # Agregar método de contacto
        contacto_tipo = request.form.get('contacto')
        contacto_id = request.form.get('contacto_id')
        if contacto_tipo and contacto_id:
            nuevo_contacto = ContactarPor(
                nombre=contacto_tipo,
                identificador=contacto_id,
                actividad_id=nueva_actividad.id
            )
            db.session.add(nuevo_contacto)
        
        # Guardar fotos
        for foto in fotos:
            if foto.filename:
                unique_filename = save_file(foto, os.path.join(app.root_path, app.config['UPLOAD_FOLDER']))
                if unique_filename:
                    nueva_foto = Foto(
                        ruta_archivo=os.path.join(app.config['UPLOAD_FOLDER'], unique_filename),
                        nombre_archivo=foto.filename,
                        actividad_id=nueva_actividad.id
                    )
                    db.session.add(nueva_foto)
        
        try:
            db.session.commit()
            flash('¡Actividad agregada correctamente!')
            return redirect(url_for('index'))
        except Exception as e:
            db.session.rollback()
            errores.append(f'Error al guardar la actividad: {str(e)}')
            regiones = Region.query.all()
            return render_template('agregar.html', regiones=regiones, errores=errores)

@app.route('/listado')
def listar_actividades():
    """Listado de actividades con paginación"""
    page = request.args.get('page', 1, type=int)
    per_page = 5
    
    # Paginación de actividades
    pagination = Actividad.query.order_by(desc(Actividad.id)).paginate(
        page=page, per_page=per_page, error_out=False
    )
    
    actividades = pagination.items
    
    return render_template('listado.html', actividades=actividades, pagination=pagination)

@app.route('/actividad/<int:id>')
def detalle_actividad(id):
    """Detalle de una actividad específica"""
    actividad = Actividad.query.get_or_404(id)
    
    # Preparar la data para JSON
    data = {
        'id': actividad.id,
        'nombre': actividad.nombre,
        'inicio': actividad.dia_hora_inicio.strftime('%Y-%m-%d %H:%M'),
        'termino': actividad.dia_hora_termino.strftime('%Y-%m-%d %H:%M') if actividad.dia_hora_termino else None,
        'comuna': Comuna.query.get(actividad.comuna_id).nombre,
        'sector': actividad.sector,
        'email': actividad.email,
        'celular': actividad.celular,
        'descripcion': actividad.descripcion,
        'tema': actividad.temas[0].tema if actividad.temas else None,
        'fotos': [
            {
                'id': foto.id,
                'ruta': f"/{foto.ruta_archivo}",
                'nombre': foto.nombre_archivo
            } for foto in actividad.fotos
        ],
        'contactos': [
            {
                'tipo': contacto.nombre,
                'id': contacto.identificador
            } for contacto in actividad.contactos
        ]
    }
    
    return jsonify(data)

# Nuevas rutas para estadísticas
@app.route('/estadisticas')
def estadisticas():
    """Página de estadísticas con gráficos"""
    return render_template('estadisticas.html')

@app.route('/api/estadisticas/actividades-por-dia')
def actividades_por_dia():
    """API para obtener datos del gráfico de líneas: actividades por día"""
    # Obtener todas las actividades y agrupar por fecha de inicio
    result = db.session.query(
        func.date(Actividad.dia_hora_inicio).label('fecha'),
        func.count(Actividad.id).label('cantidad')
    ).group_by(func.date(Actividad.dia_hora_inicio)).order_by('fecha').all()
    
    data = {
        'labels': [str(item.fecha) for item in result],
        'values': [item.cantidad for item in result]
    }
    
    return jsonify(data)

@app.route('/api/estadisticas/actividades-por-tipo')
def actividades_por_tipo():
    """API para obtener datos del gráfico de torta: actividades por tipo"""
    result = db.session.query(
        ActividadTema.tema.label('tema'),
        func.count(ActividadTema.id).label('cantidad')
    ).group_by(ActividadTema.tema).all()
    
    data = {
        'labels': [item.tema for item in result],
        'values': [item.cantidad for item in result]
    }
    
    return jsonify(data)

@app.route('/api/estadisticas/actividades-por-mes-horario')
def actividades_por_mes_horario():
    """API para obtener datos del gráfico de barras: actividades por mes y horario"""
    # Obtener actividades agrupadas por mes y clasificadas por horario
    actividades = Actividad.query.all()
    
    # Procesar datos
    meses_data = {}
    
    for actividad in actividades:
        mes = actividad.dia_hora_inicio.strftime('%Y-%m')
        hora = actividad.dia_hora_inicio.hour
        
        if mes not in meses_data:
            meses_data[mes] = {'mañana': 0, 'mediodia': 0, 'tarde': 0}
        
        if 6 <= hora < 12:
            meses_data[mes]['mañana'] += 1
        elif 12 <= hora < 18:
            meses_data[mes]['mediodia'] += 1
        else:
            meses_data[mes]['tarde'] += 1
    
    # Ordenar por mes
    meses_ordenados = sorted(meses_data.keys())
    
    data = {
        'labels': meses_ordenados,
        'mañana': [meses_data[mes]['mañana'] for mes in meses_ordenados],
        'mediodia': [meses_data[mes]['mediodia'] for mes in meses_ordenados],
        'tarde': [meses_data[mes]['tarde'] for mes in meses_ordenados]
    }
    
    return jsonify(data)

# Rutas para comentarios
@app.route('/api/comentarios/<int:actividad_id>')
def obtener_comentarios(actividad_id):
    """API para obtener comentarios de una actividad"""
    comentarios = Comentario.query.filter_by(actividad_id=actividad_id).order_by(desc(Comentario.fecha)).all()
    
    data = [
        {
            'id': comentario.id,
            'nombre': comentario.nombre,
            'texto': comentario.texto,
            'fecha': comentario.fecha.strftime('%Y-%m-%d %H:%M:%S')
        } for comentario in comentarios
    ]
    
    return jsonify(data)

@app.route('/api/comentarios', methods=['POST'])
def agregar_comentario():
    """API para agregar un comentario"""
    try:
        data = request.get_json()
        
        # Validaciones
        nombre = data.get('nombre', '').strip()
        texto = data.get('texto', '').strip()
        actividad_id = data.get('actividad_id')
        
        errores = []
        
        if not nombre or len(nombre) < 3 or len(nombre) > 80:
            errores.append('El nombre debe tener entre 3 y 80 caracteres')
        
        if not texto or len(texto) < 5:
            errores.append('El comentario debe tener al menos 5 caracteres')
        
        if not actividad_id:
            errores.append('ID de actividad requerido')
        
        # Verificar que la actividad existe
        actividad = Actividad.query.get(actividad_id)
        if not actividad:
            errores.append('La actividad no existe')
        
        if errores:
            return jsonify({'success': False, 'errores': errores}), 400
        
        # Crear el comentario
        nuevo_comentario = Comentario(
            nombre=nombre,
            texto=texto,
            actividad_id=actividad_id,
            fecha=datetime.utcnow()
        )
        
        db.session.add(nuevo_comentario)
        db.session.commit()
        
        return jsonify({
            'success': True,
            'comentario': {
                'id': nuevo_comentario.id,
                'nombre': nuevo_comentario.nombre,
                'texto': nuevo_comentario.texto,
                'fecha': nuevo_comentario.fecha.strftime('%Y-%m-%d %H:%M:%S')
            }
        })
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'success': False, 'errores': [f'Error interno: {str(e)}']}), 500

# APIs existentes
@app.route('/api/regiones')
def get_regiones():
    """API para obtener todas las regiones"""
    regiones = Region.query.all()
    return jsonify({
        'regiones': [{'id': r.id, 'nombre': r.nombre} for r in regiones]
    })

@app.route('/api/comunas/<int:region_id>')
def get_comunas(region_id):
    """API para obtener comunas de una región específica"""
    comunas = Comuna.query.filter_by(region_id=region_id).all()
    return jsonify({
        'comunas': [{'id': c.id, 'nombre': c.nombre} for c in comunas]
    })

@app.errorhandler(404)
def page_not_found(e):
    """Manejador para errores 404"""
    return render_template('404.html'), 404

@app.errorhandler(500)
def server_error(e):
    """Manejador para errores 500"""
    return render_template('500.html'), 500

if __name__ == '__main__':
    app.run(debug=True)