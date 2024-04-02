def toCounter2(decimal):
    time = abs(int(decimal))
    minute = int((abs(decimal) - time) * 60)
    second = round((((abs(decimal) - time) * 60) - minute) * 60, 2)
            
    if decimal < 0:
        time = f"-{time:02d}"
    else:
        time = f"{time:02d}"

    return f"{time} j {minute:02d} m {second:02.2f} d"
		
def toDegree2(decimal):
    degree = abs(int(decimal))
    minute = int((abs(decimal) - degree) * 60)
    second = round((((abs(decimal) - degree) * 60) - minute) * 60, 2)
    
    if decimal < 0:
        degree = f"-{degree:02d}"
    else:
        degree = f"{degree:02d}"
        
    dms = f"{degree}\u00b0 {minute:02d}\u2032 {second:02.2f}\u2033"
    
    return dms

def toTime2(decimal):
    degree = abs(int(decimal))
    minute = int((abs(decimal) - degree) * 60)
    second = round((((abs(decimal) - degree) * 60) - minute) * 60, 2)
    
    if decimal < 0:
        degree = f"-{degree:02d}"
    else:
        degree = f"{degree:02d}"
        
    dms = f"{degree}:{minute:02d}:{second:02.2f}"
    
    return dms
	
def toDecimal(degree, minute, second, check):
    decimal = degree + (minute / 60) + (second / 3600)
    
    if check is False:
        decimal = 0 - decimal
    
    return decimal
    