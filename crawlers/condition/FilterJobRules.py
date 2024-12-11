from datetime import datetime, timedelta

class FilterJobRules:   
    def outdatedEntries(data):
        # 獲取職缺的刊登日期，將YYYYMMDD格式轉換為datetime
        appear_date = datetime.strptime(data['appearDate'], '%Y%m%d')
        # 獲取當前日期，但只保留年月日
        current_date = datetime.now().replace(hour=0, minute=0, second=0, microsecond=0)
        # 計算日期差
        date_difference = current_date - appear_date
        # 如果超過兩個月（60天）則返回True
        return date_difference > timedelta(days=60)
      
