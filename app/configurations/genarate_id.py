# app/configurations/genarate_id.py
def generate_prefixed_id(db, model, field_name: str, prefix: str, digits: int) -> str:
    last_entry = db.query(model).order_by(getattr(model, field_name).desc()).first()
    if not last_entry:
        next_id = 1
    else:
        last_id = getattr(last_entry, field_name)
        next_id = int(last_id.replace(prefix, "")) + 1
    return f"{prefix}{str(next_id).zfill(digits)}"
