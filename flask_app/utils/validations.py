import re

PHONE_REGEX = re.compile(r"^\+\d{3}\.\d{8,9}$")  # +NNN.NNNNNNNN o +NNN.NNNNNNNNN

def validate_aviso_form(form, files):
    errors = []

    required = {
        "region": "Debes seleccionar una región.",
        "commune": "Debes seleccionar una comuna.",
        "sector": "Debes indicar el sector.",
        "name-user": "Debes ingresar tu nombre.",
        "email-user": "Debes ingresar tu email.",
        "pet-type": "Debes seleccionar el tipo de mascota.",
        "amount": "Debes indicar la cantidad.",
        "age": "Debes indicar la edad.",
        "age-type": "Debes indicar si la edad está en Años o Meses.",
        "delibery-date": "Debes ingresar una fecha de entrega.",
    }
    for k, msg in required.items():
        if not form.get(k):
            errors.append(msg)

    email = form.get("email-user", "").strip()
    if email and "@" not in email:
        errors.append("Email no tiene formato válido.")

    tel = form.get("tel-user", "").strip()
    if tel and not PHONE_REGEX.fullmatch(tel):
        errors.append("Celular debe tener formato +NNN.NNNNNNNN.")

    desc = form.get("description", "")
    if desc and len(desc) > 500:
        errors.append("Descripción no debe exceder 500 caracteres.")

    allowed = {".jpg", ".jpeg", ".png"}
    for f in files or []:
        if not f or f.filename == "":
            continue
        ext = f.filename.rsplit(".", 1)[-1].lower()
        if f and ("." + ext) not in allowed:
            errors.append(f"Extensión no permitida en archivo: {f.filename}")

    return errors
