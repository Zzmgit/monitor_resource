# !/usr/bin/env python
# _*_ coding:UTF-8 _*_
# @Author :  ZZM
# @Mail   :  zhangzhemingzzmh@gmail.com
# @Time   :  2017/9/25 09:42
# @File   :  mon_info.py
from django.db import models

class Host(module.Model):
	name = module.CharFiels(max_length=64, unique=True)
	ip_addr = models.GenericIPAddressField(unique=True)
	host_group = models.ManyToManyField('HostGroup', blank=True)
	templates = models.ManyToManyField('Template', blank=True)
	monitored_by_choices = (
		('agent', 'Agent'),
		('snmp', 'SNMP'),
		('wget', 'WGET')
	)
	monitored_by = models.CharField(u'监控方式', max_length=64, choices=monitored_by_choices)
	status_choices = (
		(1, 'Online'),
		(2, 'Down'),
		(3, 'Unreachable'),
		(4, 'Offline')
	)
	status = models.IntegerField(u'状态', choices=status_choices, default=1)
	memo = models.TextField(u'备注', blank=True, null=True)

	def __unicode__(self):
		return self.name


class HostGroup(models.Model):
	name = models.CharField(max_length=64, unique=True)
	templates = models.ManyToManyField('Template', blank=True)
	memo = models.TextField(u'备注', blank=True, null=True)

	def __unicode__(self):
		return self.name


class ServiceIndex(models.Model):
	name = models.CharField(max_length=64)
	key = models.CharField(max_length=64)
	data_type_choices = (
		('int', "int"),
		('float', "float"),
		('str', "string")
	)
	data_type = models.CharField(u'指标数据类型', max_length=32, choices=data_type_choices, default='int')
	memo = models.CharField(u'备注', max_length=128, blank=True, null=True)

	def __unicode__(self):
		return "%s.%s" % (self.name, self.key)


class Service(models.Model):
	name = models.CharField(u'服务名称', max_length=64, unique=True)
	interval = models.IntegerField(u'监控间隔', default=60)
	plugin_name = models.CharField(u'监控插件', max_length=64, default='n/a')
	items = models.ManyToManyField('ServiceIndex', verbose_name=u'指标列表', blank=True)
	memo = models.CharField(u'备注', max_length=128, blank=True, null=True)

	def __unicode__(self):
		return self.name
	"""
	def get_service_items(obj):
		return ",".join([i.name for i in obj.items.all()])
	"""


class Template(models.Model):
	pass
