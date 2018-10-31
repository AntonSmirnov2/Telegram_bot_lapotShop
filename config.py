from plugins.check_db import get_user_ids, check_db_exist
# CONFIG
TELE_BOT_TOKEN = '662294408:AAEONHwx_zxR0PzFhmjqV0vYbLFxH5j2nIo'
DB_NAME = 'lapotshop.sqlite'
DEEP_LOGGING = False # FOR DEBUGGING PURPOSES ONLY
PROXY_CONNECTION = True # ВКЛЮЧАЕТ СОЕДИНЕНИЕ С СЕРВЕРАМИ ТЕЛЕГИ ЧЕРЕЗ ПРОКСИ
ADMIN_IDS = (401814822, 0) # BOT's ADMINS
check_db_exist()
USER_IDS = get_user_ids()

# END OF CONFIG
