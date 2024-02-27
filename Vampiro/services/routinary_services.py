from datetime import datetime
import pytz
import logging

from Vampiro.services.game import revision_period_done, dispute_revision, round_end
from Vampiro.services.settings import get_timer_switch_value
from Vampiro.utils.security import handle_exceptions

logger = logging.getLogger('simple_logger')

@handle_exceptions
def DatabaseUpdate():
    timer_switch_value = get_timer_switch_value()  

    if timer_switch_value == False:
        logger.info('The timer is off')
        return
    else:
        logger.info('The timer is on')

        spain_tz = pytz.timezone('Europe/Madrid')
        logger.info('The timezone was chosen')
        spain_timestamp = datetime.now(spain_tz)
        logger.info('The timestamp was created')


        current_day = spain_timestamp.strftime('%A')
        current_hour = spain_timestamp.hour

        logger.info('Hoy es %s y son las %s horas', current_day, current_hour)

        if current_day == 'Monday':
            if current_hour < 12:
                logger.info('Performing Monday 00:00 task')
                dispute_revision('DAY')
                round_end()
            elif current_hour >= 12:
                logger.info('Performing Monday 12:00 task')
                dispute_revision('NIGHT')
                revision_period_done()
        else:
            logger.info('Performing regular task')
            if current_hour < 12:
                logger.info('Performing night task, checking day disputes')
                dispute_revision('DAY')
            elif current_hour >= 12:
                logger.info('Performing morning task, cheking night disputes')
                dispute_revision('NIGHT')