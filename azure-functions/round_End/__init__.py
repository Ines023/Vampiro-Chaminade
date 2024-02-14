import azure.functions as func
from Vampiro.services.game import round_end

def main(mytimer: func.TimerRequest) -> None:
    round_end()
