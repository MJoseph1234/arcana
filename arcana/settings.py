
from pathlib import Path
import os

SITE_NAME = 'arcana-check'

# Important Directories
BASE = Path(__file__).resolve().parent.parent
MARKDOWN = os.path.join(BASE, 'markdown')
STATIC = os.path.join(BASE, 'static')
TEMPLATES = os.path.join(BASE, 'templates')
OUTPUT = os.path.join(BASE, SITE_NAME)