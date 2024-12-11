import re

class FilterCompanyRules:
    def missingEmployeeAndCapital(company_data):
        profile_data = company_data.get('data')
        return (profile_data['capital'] == '暫不提供' and 
                profile_data['empNo'] == '暫不提供')

    def defaultCompanyIntro(company_data):
        profile_text = company_data.get('data')['profile']
        return profile_text.startswith("我们重视每一位员工，除了有良好工作環境、也提供學習及成長的空間")

    def shortCompanyIntro(company_data):
        profile_text = company_data.get('data')['profile']
        # 如果是空值或非字符串，直接返回True
        if not profile_text or not isinstance(profile_text, str):
            return True
        clean_text = re.sub(r'<[^>]+>', '', profile_text)  # 使用正則表達式移除HTML標籤
        clean_text = re.sub(r'\s+', '', clean_text)        # 移除空白字符
        return len(clean_text) < 200
    
    def shortMainProductDescription(company_data):
        product_text = company_data.get('data')['product']
        # 如果是空值或非字符串，直接返回True
        if not product_text or not isinstance(product_text, str):
            return True
        clean_text = re.sub(r'<[^>]+>', '', product_text)  # 使用正則表達式移除HTML標籤
        clean_text = re.sub(r'\s+', '', clean_text)        # 移除空白字符
        return len(clean_text) < 200 