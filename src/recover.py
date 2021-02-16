#!/usr/bin/env python3
from datetime import datetime
import plyvel

print('Recovery Start : '+datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
plyvel.DB('./.storage/db_icon_dex', create_if_missing=True, max_open_files=1024)
print('Recovery End : '+datetime.now().strftime('%Y-%m-%d %H:%M:%S'))