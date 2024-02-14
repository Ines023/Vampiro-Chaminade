import azure.functions as func
from Vampiro.services.game import revision_period_done

def main(mytimer: func.TimerRequest) -> None:
    revision_period_done()
