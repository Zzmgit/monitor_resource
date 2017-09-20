# !/usr/bin/env python
# _*_ coding:UTF-8 _*_
# @Author :  ZZM
# @Mail   :  zhangzhemingzzmh@gmail.com
# @Time   :  2017/9/20 11:38
# @File   :  enca_cpu.py
import psutil


class Cpu:
	@property
	def info(self):
		cpu_info = psutil.cpu_times()
		res = dict(
			user = cpu_info.user,   # 执行用户进程的时间百分比
			system = cpu_info.system,   # 执行内核进程和中断的时间百分比
			iowait = cpu_info.iowait,   # 由于IO等待而使CPU处于idle(空闲)状态的时间百分比
			idle = cpu_info.idle,   # CPU处于idle状态的时间百分比
			cpuCount_1 = psutil.cpu_count(),    # 获取CPU的逻辑个数
			cpuCount_2 = psutil.cpu_count(logical=False)    # 获取CPU的物理个数
		)
		return res