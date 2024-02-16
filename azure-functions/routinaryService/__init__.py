import azure.functions as func
from datetime import datetime
import pytz

from flask import logging
from Vampiro.services.game import revision_period_done, dispute_revision, round_end
from Vampiro.services.settings import get_timer_switch_value

def main(mytimer: func.TimerRequest) -> None:

    timer_switch_value = get_timer_switch_value()  

    if timer_switch_value == False:
        logging.info('The timer is off')
        return
    else:
        logging.info('The timer is on')

        spain_tz = pytz.timezone('Europe/Madrid')
        spain_timestamp = datetime.datetime.now(spain_tz)

        if mytimer.past_due:
            logging.info('The timer is past due!')

        current_day = spain_timestamp.strftime('%A')
        current_hour = spain_timestamp.hour

        if current_day == 'Monday':
            if current_hour == 0:
                logging.info('Performing Monday 00:00 task')
                dispute_revision('DAY')
                round_end()
            elif current_hour == 12:
                logging.info('Performing Monday 12:00 task')
                dispute_revision('NIGHT')
                revision_period_done()
        else:
            logging.info('Performing regular task')
            if current_hour == 0:
                logging.info('Performing night task, checking day disputes')
                dispute_revision('DAY')
            elif current_hour == 12:
                logging.info('Performing morning task, cheking night disputes')
                dispute_revision('NIGHT')
    
    
    
    

