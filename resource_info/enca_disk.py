# !/usr/bin/env python
# _*_ coding:UTF-8 _*_
# @Author :  ZZM
# @Mail   :  zhangzhemingzzmh@gmail.com
# @Time   :  2017/9/20 11:44
# @File   :  enca_disk.py
import psutil


class Disk:
	@property
	def info(self):
		root_partition = psutil.disk_usage("/") # 获取根分区完整信息
		home_partition = psutil.disk_usage("/home") # 获取home分区完整信息
		boot_partition = psutil.disk_usage("/boot") # 获取boot分区完整信息
		res = dict(
			root = dict(
				total = root_partition.total,   # 分区总数
				free = root_partition.free, # 分区空闲数
				used = root_partition.used  # 分区使用数
			),
			home = dict(
				total = home_partition.total,
				free = home_partition.free,
				used = home_partition.used
			),
			boot = dict(
				total = boot_partition.total,
				free = boot_partition.free,
				used = boot_partition.used
			)
		)
		return res