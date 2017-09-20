# !/usr/bin/env python
# _*_ coding:UTF-8 _*_
# @Author :  ZZM
# @Mail   :  zhangzhemingzzmh@gmail.com
# @Time   :  2017/9/20 11:54
# @File   :  enca_mem.py
import psutil


class Mem:
	@property
	def info(self):
		mem_info = psutil.virtual_memory()
		swap_info = psutil.swap_memory()
		res = dict(
			mem = dict(
				total=round(mem_info.total / (1024 ** 3), 2),  # 内存总数
				available=round(mem_info.available / (1024 ** 3), 2),  # 可用内存数
				percent=mem_info.percent,  # 内存使用率
				used=round(mem_info.used / (1024 ** 3), 2),  # 已使用的内存数
				free=round(mem_info.free / (1024 ** 3), 2),  # 空闲内存数
				active=round(mem_info.active / (1024 ** 3), 2),  # 活跃内存数
				inactive=round(mem_info.inactive / (1024 ** 3), 2),  # 不活跃内存数
				buffers=round(mem_info.buffers / (1024 ** 3), 2),  # 缓冲使用数
				cached=round(mem_info.cached / (1024 ** 3), 2),  # 缓存使用数
				shared = round(mem_info.shared / (1024 ** 3), 2)     # 共享内存数
			),
			swap=dict(
				total=round(swap_info.total / (1024 ** 3), 2),  # 交换分区总数
				used=round(swap_info.used / (1024 ** 3), 2),  # 已使用的交换分区数
				free=round(swap_info.free / (1024 ** 3), 2),  # 空闲交换分区数
				percent=swap_info.percent,  # swap空间使用率
				sin=round(swap_info.sin / (1024 ** 3), 2),  # 输入数
				sout=round(swap_info.sout / (1024 ** 3), 2)  # 输出数
			)
		)
		return res