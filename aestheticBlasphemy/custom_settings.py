'''		
Created on 28-May-2016		
		
@author: Anshul		
'''		

import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
		
SITE_TITLE="Aesthetic Blasphemy"		
SITE_TAGLINE="a million little things"		
		
SITE_URLS=["aestheticblasphemy.com",		
           "www.aestheticblasphemy.com",
           "127.0.0.1:8000"]
DB_NAME="root"		
DB_PASSWORD="root"		

DB_BASENAME=os.path.join(BASE_DIR, 'db.sqlite3')
		
TIME_ZONE_VALUE='Asia/Kolkata'

STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR,'static')

MEDIA_ROOT = os.path.join(BASE_DIR,'media')
MEDIA_URL = '/media/'
