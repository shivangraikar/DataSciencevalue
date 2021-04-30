def calc_proba(score):
    score = score / 1000
    if score < 0.05:
        return '0.3%'
    elif score < 0.1:
        return '0.7%'
    elif score < 0.2:
        return '2.6%'
    elif score < 0.4:
        return '6%'
    elif score < 0.5:
        return '11%'
    elif score < 0.6:
        return '14%'
    elif score < 0.7:
        return '21%'
    elif score < 0.8:
        return '40%'
    elif score < 0.9:
        return '67%'
    elif score < 0.95:
        return '79%'
    elif score <= 1:
        return '95%'