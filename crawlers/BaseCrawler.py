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
        url_query['page'] = ['1']
        new_query_string = urlencode(url_query, doseq=True)
        
        target_url = parsed_url.scheme + '://' + parsed_url.netloc + parsed_url.path + '/api/jobs?' + new_query_string
        
        response = BaseCrawler.fetchWebpage(target_url)
        return SearchItemProcessor(url_query, response).filterCompany(conditions, status_callback)
        
      