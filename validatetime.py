from datetime import datetime

def validate_time(h):
    try:
        if len(h) == 4: 
            datetime.strptime(h, '%H%M')
            return False
        else: return True

    except ValueError:
        return True
