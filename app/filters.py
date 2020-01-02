from datetime import datetime
from app import app


@app.template_filter('datetimeformat')
def datetimeformat(date, style='long'):
    if style == 'long':
        return date.strftime('%d %b \'%y')
    elif style == 'short':
        return date.strftime('%d-%m-%Y')
    elif style == 'delta':
        delta = datetime.now() - date
        if delta.days < 7:
            return '{}d'.format(delta.days)
        elif delta.days < 365:
            return '{}w'.format(int(delta.days/7))
        else:
            return '{}y'.format(int(delta.days/365)) 
