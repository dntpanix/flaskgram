# scripts/setup_roles.py
from pathlib import Path
import sys
sys.path.append(str(Path(__file__).resolve().parent.parent))
from app import create_app, db
from app.models import Role

app = create_app(config_name='default')   # pass config name if needed

with app.app_context():
    Role.insert_roles()
    roles = Role.query.all()
    print("Inserted/confirmed roles:", [r.name for r in roles])
