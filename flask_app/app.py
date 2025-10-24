from flask import Flask, request, render_template, redirect, url_for, jsonify, flash, send_from_directory
from datetime import datetime
from database.db import (get_regiones, get_comunas_by_region, insert_aviso, insert_contacto, insert_foto, get_last_avisos, 
    get_total_avisos, get_avisos_paginated, get_aviso_by_id, get_fotos_by_aviso, get_contactos_by_aviso, 
    get_stats_por_tipo, get_stats_por_dia, get_stats_por_mes, get_comentario_by_aviso, insert_comentario, get_stats_por_mes_tipo)
from werkzeug.utils import secure_filename
from utils.validations import validate_aviso_form
import os

UPLOAD_FOLDER = 'static/uploads'
app = Flask(__name__)
app.secret_key = 'comoasi'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = 16 * 1000 * 1000  # 16MB total
ALLOWED_EXTENSIONS = {'jpg', 'png', 'jpeg'}
MAX_FILES = 5

if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route("/")
def portada():
    ultimos = get_last_avisos(limit=5)
    regiones = get_regiones()
    return render_template("portada.html", ultimos=ultimos, regiones=regiones)

@app.route("/anuncio", methods=["GET", "POST"])
def anuncio():
    regiones = get_regiones()

    if request.method == "GET":
        return render_template("anuncio.html", regiones=regiones)

    # POST
    form = request.form
    files = request.files.getlist("photos[]")  # <-- coincide con name="photos[]"
    errors = validate_aviso_form(form, files)

    if errors:
        for e in errors:
            flash(e, "error")
        return render_template("anuncio.html", regiones=regiones), 400

    tipo = form["pet-type"].strip().lower()
    unidad_medida = "a" if form["age-type"] == "Años" else "m"
    try:
        fecha_entrega = datetime.strptime(form["delibery-date"], "%Y-%m-%d")
    except Exception:
        flash("Fecha de entrega inválida (YYYY-MM-DD).", "error")
        return render_template("anuncio.html", regiones=regiones), 400

    try:
        aviso_id = insert_aviso(
            comuna_id=int(form["commune"]),
            sector=form["sector"].strip(),
            nombre=form["name-user"].strip(),
            email=form["email-user"].strip(),
            celular=form.get("tel-user", "").strip(),
            tipo=tipo,
            cantidad=int(form["amount"]),
            edad=int(form["age"]),
            unidad_medida=unidad_medida,
            fecha_entrega=fecha_entrega,
            descripcion=form.get("description", "").strip()
        )
    except Exception as ex:
        flash(f"Error al guardar aviso: {ex}", "error")
        return render_template("anuncio.html", regiones=regiones), 500

    # Contactos (preservar 'X')
    contact_nombres = request.form.getlist("contact_nombre[]")
    contact_identificadores = request.form.getlist("contact_identificador[]")
    for n, i in zip(contact_nombres, contact_identificadores):
        n = (n or "").strip()
        i = (i or "").strip()
        if n and i:
            nombre_contacto = n if n == "X" else n.lower()
            try:
                insert_contacto(aviso_id, nombre_contacto, i)
            except Exception as ex:
                flash(f"No se pudo guardar un contacto ({n}): {ex}", "warning")

    # Fotos 
    for f in files:
        if not f or f.filename == "":
            continue
        if not allowed_file(f.filename):
            flash(f"Archivo no permitido: {f.filename}", "warning")
            continue
        filename = secure_filename(f.filename)
        name, ext = os.path.splitext(filename)
        safe_name = f"{datetime.now().strftime('%Y%m%d%H%M%S%f')}_{name}{ext}"
        path = os.path.join(app.config["UPLOAD_FOLDER"], safe_name)
        try:
            f.save(path)
            # db.py espera (aviso_id, ruta_archivo, nombre_archivo)
            insert_foto(aviso_id, app.config["UPLOAD_FOLDER"], safe_name)
        except Exception as ex:
            flash(f"No se pudo guardar una foto: {ex}", "warning")

    flash("¡Aviso publicado con éxito!", "success")
    return redirect(url_for("avisos"))

@app.route("/uploads/<path:filename>")
def uploaded_file(filename):
    return send_from_directory(app.config["UPLOAD_FOLDER"], filename)

@app.route("/comunas")
def comunas_por_region():
    region_id = request.args.get("region_id", type=int)
    if not region_id:
        return jsonify([])

    comunas = get_comunas_by_region(region_id)

#si no ponia esto daba error -.-
    def _attr(x, key):
        # ORM object
        if hasattr(x, key):
            return getattr(x, key)
        # dict
        if isinstance(x, dict):
            return x.get(key)
        # tuple/list (id, nombre)
        if isinstance(x, (tuple, list)):
            return x[0] if key == "id" else x[1]
        return None

    data = [{"id": _attr(c, "id"), "nombre": _attr(c, "nombre")} for c in comunas]
    return jsonify(data)

@app.route("/avisos")
def avisos():
    page = request.args.get("page", default=1, type=int)
    per_page = request.args.get("per_page", default=10, type=int)

    total = get_total_avisos()
    avisos_list = get_avisos_paginated(page=page, per_page=per_page)
    total_pages = max(1, (total + per_page - 1) // per_page)
    has_prev = page > 1
    has_next = page < total_pages

    # Si es AJAX, devuelve solo el parcial de tabla
    if request.headers.get("X-Requested-With") == "XMLHttpRequest":
        return render_template(
            "_avisos_table.html",
            avisos=avisos_list,
            page=page,
            total_pages=total_pages,
            has_prev=has_prev,
            has_next=has_next
        )

    return render_template(
        "avisos.html",
        avisos=avisos_list,
        page=page,
        total_pages=total_pages,
        has_prev=has_prev,
        has_next=has_next
    )

@app.route("/aviso/<int:aviso_id>")
def detalle_aviso(aviso_id: int):
    page = request.args.get("page", type=int)
    aviso = get_aviso_by_id(aviso_id)
    if not aviso:
        flash("Aviso no encontrado.", "error")
        return redirect(url_for("avisos"))

    fotos = get_fotos_by_aviso(aviso_id)
    contactos = get_contactos_by_aviso(aviso_id)

    return render_template(
        "detalle.html",
        aviso=aviso,
        fotos=fotos,
        contactos=contactos,
        page=page
    )

#same
@app.route("/estadisticas")
def estadisticas():
    return render_template("estadisticas.html")

@app.route("/api/stats/por_tipo")
def api_stats_por_tipo():
    rows = get_stats_por_tipo()
    return jsonify([{"tipo": r["tipo"], "total": int(r["total"])} for r in rows])

@app.route("/api/stats/por_dia")
def api_stats_por_dia():
    days = request.args.get("days", default=30, type=int)
    rows = get_stats_por_dia(days=days)
    return jsonify([{"dia": r["dia"].strftime("%Y-%m-%d"), "total": int(r["total"])} for r in rows])

@app.route("/api/stats/por_mes")
def api_stats_por_mes():
    year = request.args.get("year", default=datetime.now().year, type=int)
    rows = get_stats_por_mes(year=year)
    return jsonify([{"mes": int(r["mes"]), "total": int(r["total"])} for r in rows])

if __name__ == "__main__":
    app.run(debug=True)

#obtener los comentarios (GET)
@app.route("/api/avisos/<int:aviso_id>/comentarios", methods = ["GET"])
def api_listar_comentarios(aviso_id):
    comentarios = get_comentario_by_aviso(aviso_id)
    data = [ {
        "id": c.id, 
        "nombre": c.nombre, 
        "texto": c.texto, 
        "fecha": c.fecha.strftime("%Y-%m-%d %H:%M") 
    }
    for c in comentarios ]
    return jsonify(data)

#incluir comentarios (POST)
@app.route("/api/avisos/<int:aviso_id>/comentarios", methods=["POST"])
def api_agregar_comentario(aviso_id):
    # puede venir como JSON o form-encoded
    if request.is_json:
        payload = request.get_json(silent=True) or {}
        nombre = (payload.get("nombre") or "").strip()
        texto  = (payload.get("texto") or "").strip()
    else:
        nombre = (request.form.get("nombre") or "").strip()
        texto  = (request.form.get("texto") or "").strip()

    # Validación servidor: nombre 3..80, texto 5..300
    errors = []
    if len(nombre) < 3 or len(nombre) > 80:
        errors.append("El nombre debe tener entre 3 y 80 caracteres.")
    if len(texto) < 5 or len(texto) > 300:
        errors.append("El comentario debe tener entre 5 y 300 caracteres.")

    if errors:
        return jsonify({"ok": False, "errors": errors}), 400

    try:
        cid = insert_comentario(aviso_id, nombre, texto)
        return jsonify({"ok": True, "id": cid}), 201
    except Exception:
        return jsonify({"ok": False, "errors": [f"Error al guardar: {Exception}"]}), 500
    
@app.route("/api/stats/por_mes_tipo")
def api_stats_por_mes_tipo():
    year = request.args.get("year", default=datetime.now().year, type=int)
    rows = get_stats_por_mes_tipo(year=year)
    return jsonify(rows)