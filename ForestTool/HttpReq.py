#coding=utf-8
__author__ = 'zxlee'
__github__ = 'https://github.com/SmileZXLee/forestTool'
import json
import requests
from requests.cookies import RequestsCookieJar
import urlparse

def json_dic(json_str):
	try:
		json_object = json.loads(json_str)
	except ValueError, e:
		json_object = {}
	return json_object

def get_req(url):
	up = urlparse.urlparse(url)
	conn = httplib.HTTPConnection(up.netloc)
	conn.request(method="GET",url=url) 
	response = conn.getresponse()
	res= response.read()
	return res;


def send_req(url,headers,data,remember_token,post_type):
	str_json = json.dumps(data)
	up = urlparse.urlparse(url)
	org_headers = {
		"Accept": "*/*",
		"Accept-Encoding": "br, gzip, deflate",
		"Accept-Language": "zh-Hans-CN;q=1",
		"Connection": "keep-alive",
		"Content-Length": str(len(str_json)),
		"Content-Type": 
		"application/json; charset=utf-8",
		"Host": up.netloc,
		"User-Agent": "Forest/342 (iPhone; iOS 12.1.2; Scale/3.00)"
	}
	final_headers = org_headers.copy()
	if headers :
		final_headers.update(headers)

	cookie_jar = RequestsCookieJar()
	if len(remember_token):
		cookie_jar.set("remember_token",remember_token, domain=up.netloc)
	if post_type.upper() == 'POST':
		res = requests.post(url,data=str_json,headers=final_headers,cookies=cookie_jar)
	elif post_type.upper() == 'PUT':
		res = requests.put(url,data=str_json,headers=final_headers,cookies=cookie_jar)
	elif post_type.upper() == 'GET':
		res = requests.get(url,data=str_json,headers=final_headers,cookies=cookie_jar)
	else:
		print('TypeErr')
	dict_json = json_dic(res.text)
	#if res.status_code != requests.codes.ok:	
	return dict_json


