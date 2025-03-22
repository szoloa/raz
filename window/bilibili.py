import httpx
from bs4 import BeautifulSoup as soup
import time
from urllib.parse import urljoin

class VideoSpider:
    def __init__(self, key, handle=print, type_opt='json', year1=2009, year2=2025):
        self.base_url = 'https://search.bilibili.com/all'
        self.key = key
        self.year1 = year1
        self.year2 = year2
        self.type_opt = type_opt
        self.handle = handle
        self.host = 'https://www.bilibili.com'
        self.opt = f'./data/{key}_{year2}_{year1}.txt'
        
        # 时间戳转换
        a1 = f"{year1}-1-1 00:00:00"
        a2 = f"{year2}-12-31 00:00:00"
        timeArray1 = time.strptime(a1, "%Y-%m-%d %H:%M:%S")
        timeArray2 = time.strptime(a2, "%Y-%m-%d %H:%M:%S")
        sjc1 = max(int(time.mktime(timeArray1)), 1245945600)
        sjc2 = min(int(time.mktime(timeArray2)), int(time.time()))
        
        # 请求参数
        self.params = {
            'keyword': key,
            'pubtime_begin_s': sjc1,
            'pubtime_end_s': sjc2,
            'page': 1  # 分页参数可能需要调整为'pn'
        }
        
        # 请求头
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
            'Referer': 'https://www.bilibili.com/'
        }
        
        self.navigate_and_scrape()

    def navigate_and_scrape(self):
        page = 1
        while True:
            self.params['page'] = page  # 如果分页参数是'pn'，改为self.params['pn'] = page
            try:
                with httpx.Client(headers=self.headers, follow_redirects=True) as client:
                    response = client.get(self.base_url, params=self.params, timeout=10)
                    response.raise_for_status()
            except Exception as e:
                self.handle(f"请求失败: {e}")
                break
            
            has_data = self.scrape_page(response.text)
            if not has_data:
                break
            
            page += 1
            time.sleep(1)  # 避免请求过快

    def scrape_page(self, html):
        soup_page = soup(html, 'lxml')
        videos = soup_page.find_all(class_='bili-video-card')
        if not videos:
            return False
        for video in videos:
            try:
                title_elem = video.find(class_='bili-video-card__info--tit')
                title = title_elem.get_text(strip=True) if title_elem else ''
                
                stats = video.find_all(class_='bili-video-card__stats--item')
                item_times = stats[0].get_text(strip=True) if len(stats) > 0 else ''
                duration_elem = video.find(class_='bili-video-card__stats__duration')
                duration = duration_elem.get_text(strip=True) if duration_elem else ''
                
                # 处理播放量条件
                if '万' in item_times:
                    views = float(item_times.replace('万', ''))
                    if views > 5 and self.check_duration(duration):
                        link_elem = video.find('a', href=lambda href: href and '/video/' in href)
                        if link_elem:
                            video_path = link_elem['href']
                            video_link = urljoin(self.host, video_path)
                            if self.type_opt == 'json':
                                f.write(f'{{"text": "{title}", "url": "{video_link}"}}\n')
                            else:
                                f.write(f'{video_link}\n')
                            self.handle(f"Saved: {title}")
            except Exception as e:
                self.handle(f"解析视频出错: {e}")
        return True

    @staticmethod
    def check_duration(duration):
        """检查时长是否大于1分钟"""
        parts = duration.split(':')
        if len(parts) == 2:  # 格式为 MM:SS
            return int(parts[0]) >= 1
        elif '时' in duration:  # 处理小时格式
            return True
        return False  # 不足1分钟

if __name__ == '__main__':
    VideoSpider('amv', year1=2020, year2=2023)