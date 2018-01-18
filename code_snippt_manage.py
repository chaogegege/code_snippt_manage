#-*- coding: UTF-8 -*-
import sublime, sublime_plugin
import os
import os.path
import json
import time
import sys
import webbrowser
import re
from urllib import request, parse
import uuid
from imp import reload
reload(sys)

class EidtSnppitConfigCommand(sublime_plugin.TextCommand):
	def run(self,edit):
		view = self.view
		sels = view.sel()
		
		#判断设置文件是否存在
		filepath = os.path.split(os.path.realpath(__file__))[0]+"\\code.sublime-settings"
		if not os.path.exists(filepath):
			
			settingContent = '{\n	//登录代码管理平台的token\n	"token": "'+str(uuid.uuid1())+'",\n}'
			open(filepath,'w',encoding='utf8').write(settingContent)
			
		view.window().open_file(filepath)


class NewSnppitCommand(sublime_plugin.TextCommand):
	def run(self,edit):
		view = self.view
		sels = view.sel()
		content = view.substr(view.sel()[0])
		#判断设置文件是否存在
		filepath = os.path.split(os.path.realpath(__file__))[0]+"\\code.sublime-settings"
		if not os.path.exists(filepath):
			
			settingContent = '{\n	//登录代码管理平台的token\n	"token": "'+str(uuid.uuid1())+'",\n}'
			open(filepath,'w',encoding='utf8').write(settingContent)
			
		settings = sublime.load_settings('code.sublime-settings')
		token = settings.get('token',False)
		targetUrl = 'http://123.207.174.22/home/index/add_callback'
		postData = {
    	    'token': token,
    	    'content':content,
	    }
		

		postDataEncode = parse.urlencode(postData)
		f = request.urlopen(targetUrl, data=postDataEncode.encode())
		data = f.read()
		
		jsonResultString = data.decode('utf-8')
		jsonResult = json.loads(jsonResultString)		
		if not jsonResult['error_code']:
			webbrowser.open_new("http://123.207.174.22/home/index/add.html?id="+jsonResult['msg']+"&token="+token)
			print(jsonResult['msg'])


class SynoSnppitCommand(sublime_plugin.TextCommand):
	
	def run(self, edit):
		#判断设置文件是否存在
		filepath = os.path.split(os.path.realpath(__file__))[0]+"\\code.sublime-settings"
		if not os.path.exists(filepath):
			
			settingContent = '{\n	//登录代码管理平台的token\n	"token": "'+str(uuid.uuid1())+'",\n}'
			open(filepath,'w',encoding='utf8').write(settingContent)		

		#看是否有要打开的文件
		settings = sublime.load_settings('code.sublime-settings')
		token = settings.get('token',False)

		targetUrl = 'http://123.207.174.22/home/index/syno'
		postData = {
    	    'token': token
	    }
	
		postDataEncode = parse.urlencode(postData)
		f = request.urlopen(targetUrl, data=postDataEncode.encode())
		data = f.read()
		
		jsonResultString = data.decode('utf-8')
		jsonResult = json.loads(jsonResultString)


		#删除用户文件夹
		path1 = os.path.split(os.path.realpath(__file__))[0]+"\\snippt\\"+token
		print(path1)
		if os.path.exists(path1):
			filelist=os.listdir(path1)
			print(filelist)    
			for f in filelist:
				filepath = os.path.join( path1, f )
				print(filepath)
				if os.path.isfile(filepath):
					os.remove(filepath)
		else:
			os.makedirs(path1)
		for x in jsonResult:
			x['content'] = x['content'].replace("$","\$");
			scope = 'text.html,source.js,source.php,source.css meta.property-list.css - meta.property-value.css, source.less - meta.property-value.css, source.sass - meta.property-list - support.function.name.sass.library - variable.other.root, source.scss - meta.property-list - support.function.name.sass.library - variable.other.root'
			txt = "<snippet>\n<content><![CDATA["+x['content']+"]]></content>\n<tabTrigger>"+x['trigger']+"</tabTrigger>\n<scope>"+scope+"</scope>\n<description>"+x['des']+"</description>\n</snippet>"
			open(path1+"\\"+x['id']+".sublime-snippet",'w',encoding='utf8').write(txt)
	
		
			
