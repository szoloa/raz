# 请求地址
url = 'https://youtube.googleapis.com/youtube/v3/search' 

# 请求头
self.headers = {
	"Accept": "*/*",
	"User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
}

# 请求参数
params = {
	'part': 'snippet',
	'maxResults': '25',
	'q': search_keyword,
	'key': self.API_KEY,
	'pageToken': pageToken,
	'order': self.sort_by,
	'publishedBefore': str(self.end_date) + 'T00:00:00Z',
	'publishedAfter': str(self.start_date) + 'T00:00:00Z',
}

