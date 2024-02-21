# Vampiro/services/admin_actions.py
from datetime import datetime
import threading
import time
from sqlalchemy import create_engine, MetaData, Table, select, func
from flask import send_file
import pandas as pd
from pyunpack import Archive
import os
import tempfile
import zipfile
import shutil
from werkzeug.utils import secure_filename
import logging

from Vampiro.database.mysql import db
from Vampiro.models.SettingsModel import Settings
from Vampiro.models.UserModel import User
from Vampiro.services.settings import set_holidays, set_timer_switch_value
from Vampiro.utils.emails import send_game_starting_soon_email

logger = logging.getLogger('simple_logger')

# CRONICAS _________________________________________________________________

def add_cronica(cronica):
    """
    Adds a new cronica to the database
    """
    db.session.add(cronica)
    db.session.commit()

# USERS _______________________________________________________________________
    
def avisar_a_usuarios():
    """
    Avisa a todos los usuarios de la nueva partida
    """
    users = User.query.all()
    for user in users:
        send_game_starting_soon_email(user)
    return True

# AUTOMATIONS _______________________________

def activate_automation():
    set_timer_switch_value(True) 

def deactivate_automation():
    set_timer_switch_value(False) 

# VACACIONES _______________________________________________________________    

def activate_holidays():
    set_holidays(True)

def deactivate_holidays():
    set_holidays(False)

# GAME RESETTER _____________________________________________________________


engine = create_engine(os.environ['SQLALCHEMY_DATABASE_URI'])
metadata = MetaData()
tables = ['user','player', 'hunt', 'dispute','settings', 'cronicas', 'role']

def download_data():
    # Create a temporary directory
    with tempfile.TemporaryDirectory() as tmpdirname:
        for table_name in tables:
            table = Table(table_name, metadata, autoload_with=engine)
            query = select(table)
            df = pd.read_sql(query, engine)

            # write the DataFrame to a CSV file in the temporary directory
            df.to_csv(os.path.join(tmpdirname, f'{table_name}.csv'), index=False)

        filename = datetime.now().strftime('%Y-%m-%d_%H-%M-%S')

        # Zip all CSV files in the temporary directory
        zip_file_path = os.path.join(os.getcwd(), 'Game_data_downloads', filename)
        shutil.make_archive(zip_file_path, 'zip', tmpdirname)

        delayed_delete_file(f'{zip_file_path}.zip', 30)

        # Send the zip file as an attachment
        return send_file(f'{zip_file_path}.zip', as_attachment=True)

def delayed_delete_file(path, delay):
    def delete_file():
        time.sleep(delay)
        os.remove(path)
        print(f'{path} removed')

    threading.Thread(target=delete_file).start()

def reset_tables():
    reset_tables = ['dispute','hunt','player','user', 'settings']
    for table_name in reset_tables:
        # reflect the table
        table = Table(table_name, metadata, autoload_with=engine)

        # delete all records from the table except the base user
        with engine.begin() as connection:
            if table_name == 'user':
                connection.execute(table.delete().where(table.c.name != 'Dracula'))
            else:
                connection.execute(table.delete())

    # Insert initial settings
    settings = Settings(mode='VAMPIRO', game_status='NOT_STARTED', round_status='PROCESSED', extension_status='NOT_EXTENDED', timer_switch=False, holidays=False)
    db.session.add(settings)
    db.session.commit()
    print('Tables reset successfully')
    logger.info('Tables reset successfully')

def upload_data(file):
    if file and zipfile.is_zipfile(file):
        filename = secure_filename(file.filename)
        os.makedirs('Game_data_uploads', exist_ok=True)
        filepath=os.path.join('Game_data_uploads', filename)
        file.save(filepath)
        time.sleep(5)

        # Create a temporary directory
        with tempfile.TemporaryDirectory() as tmpdirname:
            print('Temporary directory created'	)

            try:
                Archive(filepath).extractall(tmpdirname)
            except Exception as e:
                return str(e), 400

            print('Zip file extracted')
            print(tables)
            for table_name in tables:
                # reflect the table
                table = Table(table_name, metadata, autoload_with=engine)

                # check if table is empty
                query = select([func.count('*')]).select_from(table)
                count = engine.execute(query).scalar()
                if count == 0:
                    # read the data from the CSV file
                    df = pd.read_csv(os.path.join(tmpdirname, f'{table_name}.csv'))

                    # write the data to the table
                    df.to_sql(table_name, engine, if_exists='append', index=False)
                    print('Data imported successfully')
                else:
                    print('Table is not empty')
                    return f'Table {table_name} is not empty', 400

        return 'File uploaded and data imported successfully', 200
    else:
        return 'Invalid file', 400