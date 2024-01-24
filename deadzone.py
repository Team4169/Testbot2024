import constants

def addDeadzone(val):
    threshold = constants.deadzone
    if val > 0:
        if val <  threshold:
            return 0
        else:
            return (val - threshold) / (1 - threshold)
    else:
        if val >  -threshold:
            return 0
        else:
            return (val + threshold) / (1 - threshold)
        
        