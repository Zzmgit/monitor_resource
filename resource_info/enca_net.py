# !/usr/bin/env python
# _*_ coding:UTF-8 _*_
# @Author :  ZZM
# @Mail   :  zhangzhemingzzmh@gmail.com
# @Time   :  2017/9/20 14:17
# @File   :  enca_net.py
import psutil


class Net:
	@property
	def info(self):
		allnetio = psutil.net_io_counters()  # 获取网络总的IO信息
		onenetio = psutil.net_io_counters(pernic=True)  # 输出每个网络接口的IO信息
		res = dict(
			allnetio=dict(
				bytes_sent=allnetio.bytes_sent,  # 发送字节数
				bytes_recv=allnetio.bytes_recv,  # 接受字节数
				packets_sent=allnetio.packets_sent,  # 发送数据包数
				packets_recv=allnetio.packets_recv,  # 接受数据包数
				errin=allnetio.errin,
				errout=allnetio.errout,
				dropin=allnetio.dropin,
				dropout=allnetio.dropout
			),
			onenetio=[
				dict(
					name=v[0],
					bytes_sent=v[1].bytes_sent,  # 发送字节数
					bytes_recv=v[1].bytes_recv,  # 接受字节数
					packets_sent=v[1].packets_sent,  # 发送数据包数
					packets_recv=v[1].packets_recv,  # 接受数据包数
					errin=v[1].errin,
					errout=v[1].errout,
					dropin=v[1].dropin,
					dropout=v[1].dropout
				)
				for v in onenetio.items()
			]
		)
		return res