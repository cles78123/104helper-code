import requests
from modules.FileUtil import FileUtil
from urllib.parse import urlparse, parse_qs, urlencode

class BaseCrawler:  
    def getHeaders(url):
        headers_with_referer = FileUtil.loadSettings('headers')
        headers_with_referer["referer"] = url
        return headers_with_referer
    
    def fetchWebpage(url):
        response = requests.get(url, headers=BaseCrawler.getHeaders(url))
  
        if response.status_code == 200:
            return response.json()
        else:
            raise Exception(f"爬蟲失敗，狀態碼:{response.status_code}，網址:{url}")

    def getSearchItemTable(url, conditions, status_callback=None):
        from .processor.SearchItemProcessor import SearchItemProcessor 
        
        parsed_url = urlparse(url)
        url_query = parse_qs(parsed_url.query)
        
        # 先爬第一頁獲取總頁數
        url_query['page'] = ['1']
        new_query_string = urlencode(url_query, doseq=True)
        target_url = parsed_url.scheme + '://' + parsed_url.netloc + parsed_url.path + '/api/jobs?' + new_query_string
        
        first_response = BaseCrawler.fetchWebpage(target_url)
        processor = SearchItemProcessor(url_query, first_response)
        
        # 如果有多頁，繼續爬取剩餘頁面
        all_data = first_response['data']
        total_pages = first_response['metadata']['pagination']['lastPage']
        
        if total_pages > 1:
            for page in range(2, total_pages + 1):
                if status_callback:
                    status_callback(f"正在爬取第 {page}/{total_pages} 頁", (page / total_pages) * 100)
                    
                url_query['page'] = [str(page)]
                new_query_string = urlencode(url_query, doseq=True)
                target_url = parsed_url.scheme + '://' + parsed_url.netloc + parsed_url.path + '/api/jobs?' + new_query_string
                
                page_response = BaseCrawler.fetchWebpage(target_url)
                all_data.extend(page_response['data'])
        
        # 更新 processor 中的資料為所有頁面的資料
        processor.data = all_data
        return processor.filterCompany(conditions, status_callback)
        
      