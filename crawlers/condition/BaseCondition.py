from crawlers.condition.FilterCompanyRules import FilterCompanyRules
from crawlers.condition.FilterJobRules import FilterJobRules
from pydash.strings import camel_case

class BaseCondition:
    def generateConditionFromSettings(settings):
        conditions = {
            'company': [],
            'job': []
        }
        
        for key, item in settings.items():
            if(item.get('status') == True):
                # 解析規則類型（公司或職缺）和規則名稱
                rule_type, rule_name = key.split('.')
                method_name = camel_case(rule_name.removeprefix("exclude_"))
                
                # 根據規則類型添加到對應的列表
                if rule_type == 'company':
                    method = getattr(FilterCompanyRules, method_name)
                    conditions['company'].append(lambda x, m=method: m(x))
                elif rule_type == 'job':
                    method = getattr(FilterJobRules, method_name)
                    conditions['job'].append(lambda x, m=method: m(x))
        
        return conditions