from urllib.parse import urlparse
from crawlers.BaseCrawler import BaseCrawler
from crawlers.condition.FilterCompanyRules import FilterCompanyRules
from crawlers.condition.FilterJobRules import FilterJobRules

class SearchItemProcessor:
    def __init__(self, query, response):
        self.data = response['data']
        self.page_count = response['metadata']['pagination']['lastPage']
        self.query = query
        
    def filterCompany(self, conditions, status_callback=None):
        filter_company = set()
        done_company = set()
        pass_company = []
        
        # 檢查是否有任何規則
        if not conditions or (not conditions.get('company') and not conditions.get('job')):
            return [{
                'company': job['custName'],
                'company_url': job['link']['cust'],
                'job': job['jobName'],
                'job_url': job['link']['job'],
                'appear_at': job['appearDate'],
            } for job in self.data]
        
        total_jobs = len(self.data)
        processed_jobs = 0
        
        if status_callback:
            status_callback(f"開始過濾公司資料 (共 {total_jobs} 筆)", 0)
        
        for job in self.data:
            company = job['custName']
            processed_jobs += 1
            
            # 更新進度信息
            if status_callback:
                progress = (processed_jobs / total_jobs) * 100
                status_callback(f"正在處理: {company} ({processed_jobs}/{total_jobs})", progress)
            
            # 如果公司已被過濾，直接跳過
            if company in filter_company:
                continue
            
            # 處理公司規則（只有當公司未處理過時）
            if conditions.get('company') and company not in done_company:
                parsed_company_url = urlparse(job['link']['cust'])
                target_url = parsed_company_url.scheme + '://' + parsed_company_url.netloc + parsed_company_url.path.replace("/company/", "/company/ajax/content/")
                company_response = BaseCrawler.fetchWebpage(target_url)
                
                if any(condition(company_response) for condition in conditions['company']):
                    filter_company.add(company)
                    continue
                done_company.add(company)
            
            # 處理職缺規則
            if conditions.get('job'):
                if any(condition(job) for condition in conditions['job']):
                    continue
            
            pass_company.append({
                'company': company,
                'company_url': job['link']['cust'],
                'job': job['jobName'],
                'job_url': job['link']['job'],
                'appear_at': job['appearDate'],
            })
    
        return pass_company
                