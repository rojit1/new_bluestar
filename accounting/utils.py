from pyBSDate import convert_AD_to_BS
from datetime import datetime
def calculate_depreciation(amount, percentage, bill_date):
    date_format = '%Y-%m-%d'
    ad_date = datetime.strptime(bill_date, date_format)
    year, month, day = ad_date.year, ad_date.month, ad_date.day
    bs_date = convert_AD_to_BS(year, month, day)
    nepali_month_int = bs_date[1]
    depreciation_amount = 0
    if nepali_month_int <= 3:
        depreciation_amount = (amount*(percentage/100))/3
    elif nepali_month_int <= 9:
        depreciation_amount = amount*(percentage/100)
    else:
        depreciation_amount = (amount*(percentage/100))*2/3
    return depreciation_amount, bs_date
