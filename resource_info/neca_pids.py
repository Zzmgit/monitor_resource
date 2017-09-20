# !/usr/bin/env python
# _*_ coding:UTF-8 _*_
# @Author :  ZZM
# @Mail   :  zhangzhemingzzmh@gmail.com
# @Time   :  2017/9/20 14:20
# @File   :  neca_pids.py
import datetime

import psutil


class Pids:
	@property
	def info(self):
		pids_info = psutil.pids()  # 列出所有进程pid
		p_info = map(lambda v: psutil.Process(v), pids_info)  # 实例化进程状态
		res = dict(
			p_info=[
				dict(
					pid=v[0],  # 进程pid
					name=v[1].name(),  # 进程名称
					exe=v[1].exe(),  # 进程bin路劲
					cwd=v[1].cwd(),  # 进程工作目录绝对路劲
					status=v[1].status(),  # 进程状态
					create_time=datetime.datetime.fromtimestamp(v[1].create_time()).strftime("%Y-%m-%d %H:%M:%S"),
					# 进程创建时间
					uids=dict(  # 进程uid信息
						real=v[1].uids().real,
						effective=v[1].uids().effective,
						saved=v[1].uids().saved,
					),
					gids=dict(  # 进程gid信息
						real=v[1].gids().real,
						effective=v[1].gids().effective,
						saved=v[1].gids().saved,
					),
					cpu_times=dict(  # 进程cpu时间
						user=v[1].cpu_times().user,  # 用户cpu时间
						system=v[1].cpu_times().system,  # 系统cpu时间
					),
					cpu_affinity=v[1].cpu_affinity(),  # 进程cpu亲和度
					memory_percent=round(v[1].memory_percent(), 2),  # 进程内存利用率
					memory_info=dict(  # 进程内存信息
						rss=v[1].memory_info().rss,  # 进程内存rss信息
						vms=v[1].memory_info().vms,  # 进程内存vms信息
					),
					io_counters=dict(  # 进程IO信息
						read_count=v[1].io_counters().read_count,  # 读IO数
						read_bytes=v[1].io_counters().read_bytes,  # IO读字节数
						write_count=v[1].io_counters().write_count,  # 写IO数
						write_bytes=v[1].io_counters().write_bytes,  # IO写字节数
					),
					# connections=v[1].connections(),     # 打开进程socket的namedutples列表
					num_threads=v[1].num_threads(),  # 进程开启的进程数
				)
				for v in zip(pids_info, p_info)
			]
		)
		res["p_info"] = sorted(res["p_info"], key=lambda v: v[""], reverse=True)
		return res