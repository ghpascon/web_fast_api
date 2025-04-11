from fastapi.templating import Jinja2Templates
from datetime import datetime

def generate_footer():
    year = datetime.now().year
    return f"© {year} - Gabriel Henrique Pascon"

templates = Jinja2Templates(directory="app/templates")
templates.env.globals["generate_footer"] = generate_footer
