# !/usr/bin/env python
# _*_ coding:UTF-8 _*_
# @Author :  ZZM
# @Mail   :  zhangzhemingzzmh@gmail.com
# @Time   :  2017/9/20 14:22
# @File   :  enca_user.py
import datetime

import psutil


class User:
	@property
	def info(self):
		user_info = psutil.users()  # 当前登录系统的用户信息
		res = dict(
			user = [
				dict(
					name = n.name,  # 当前登录用户名
					terminal = n.terminal,  # 打开终端
					host = n.host,  # 登陆IP地址
					started = datetime.datetime.fromtimestamp(n.started).strftime("%Y-%m-%d %H:%M:%S")  # 登录时间
				)
				for n in user_info  # 循环所有用户
			],
			boottime = datetime.datetime.fromtimestamp(psutil.boot_time()).strftime("%Y-%m-%d %H:%M:%S")    # 开机时间
		)
		return res