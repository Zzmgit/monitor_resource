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
	name = models.CharField(u'模板名称', max_length=64, unique=True)
	services = models.ManyToManyField('Service', verbose_name=u'服务列表')
	triggers = models.ManyToManyField('Trigger', verbose_name=u'触发器列表', blank=True)

	def __unicode__(self):
		return self.name


class TriggerExpression(models.Model):
	trigger = models.ForeignKey('Trigger', verbose_name=u'所顺触发器')
	service = models.ForeignKey(Service, verbose_name=u'关联服务')
	service_index = models.ForeignKey(ServiceIndex, verbose_name=u'关联服务指标')
	specified_index_key = models.CharField(verbose_name=u'只监控专门指定的指标key', max_length=64, blank=True, null=True)
	operator_type_choices = (('eq', '='), ('lt', '<'), ('gt', '>'))
	operator_type = models.CharField(u'运算符', choices=operator_type_choices, max_length=32)
	data_calc_type_choices = (
		('avg', 'Average'),
		('max', 'Max'),
		('hit', 'Hit'),
		('last', 'Last')
	)
	data_calc_func = models.CharField(u'数据处理方式', choices=data_calc_type_choices, max_length=64)
	data_calc_args = models.CharField(u'函数传入参数', help_text=u'若有多个参数，分号隔开，第一值是时间', max_length=64)
	threshold = models.IntegerField(u'阈值')

	logic_type_choices = (('or', 'OR'), ('and', 'AND'))
	logic_type = models.CharField(u'与一个条件的逻辑关系', choices=logic_type_choices, max_length=32, blank=True, null=True)

	def __unicode__(self):
		return "%s %s(%s(%s))" % (self.service_index, self.operator_type, self.data_calc_func, self.data_calc_args)

	class Meta:
		pass


class Trigger(models.Model):
	name = models.CharField(u'触发器名称', max_length=64)
	severity_choices = (
		(1, 'Information'),
		(2, 'Warning'),
		(3, 'Average'),
		(4, 'High'),
		(5, 'Diaster')
	)
	severity = models.IntegerField(u'告警级别', choices=severity_choices)
	enabled = models.BooleanField(default=True)
	memo = models.TextField(u'备注', blank=True, null=True)

	def __unicode__(self):
		return "<serice:%s, severity:%s>" % (self.name, self.get_severity_display())


class Action(models.Model):
	name = models.CharField(max_length=64, unique=True)
	host_groups = models.ManyToManyField('HostGroup', blank=True)
	hosts = models.ManyToManyField('Hosts', blank=True)

	conditions = models.TextField(u'告警条件')
	interval = models.IntegerField(u'告警间隔(s)', default=300)
	operations = models.ManyToManyField('ActionOperation')

	recover_notice = models.BooleanField(u'故障恢复后发送通知消息', default=True)
	recover_subject = models.CharField(max_length=128, blank=True, null=True)
	recover_message = models.TextField(blank=True, null=True)

	enabled = models.BooleanField(default=True)

	def __unicode__(self):
		return self.name


class ActionOperation(models.Model):
	name = models.CharField(max_length=64)
	step = models.SmallIntegerField(u'第n次告警', default=1)
	action_type_choices = (
		('email', 'Email'),
		('sms', 'SMS'),
		('script', 'RunScript')
	)
	action_type = models.CharField(u'动作类型', choices=action_type_choices, max_length=64, default='email')

	def __unicode__(self):
		return self.name


class Maintenance(models.Model):
	name = models.CharField(max_length=64, unique=True)
	hosts = models.ManyToManyField('Host', blank=True)
	hosts_groups = models.ManyToManyField('HostGroup', blank=True)
	content = models.TextField(u'维护内容')
	start_time = models.DateTimeField()
	end_time = models.DateTimeField()

	def __unicode__(self):
		return self.name