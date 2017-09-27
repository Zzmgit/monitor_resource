# !/usr/bin/env python
# _*_ coding:UTF-8 _*_
# @Author :  ZZM
# @Mail   :  zhangzhemingzzmh@gmail.com
# @Time   :  2017/9/27 10:02
# @File   :  telnetMonitor.py
import logging
import socket
import telnetlib

import time
import traceback


class telnetAction:
	def __init__(self, host, prompt, account, accoutPasswd, RootPasswd=""):
		self.log = logging.getLogger()
		self.host = host        # IP Address
		self.prompt = prompt        # 登录提示
		self.accout = account       # 账户
		self.accoutPasswd = accoutPasswd        # 账户密码
		self.RootPasswd = RootPasswd        # 超管账户
		self.possible_prompt = ["#", "$"]       # 可能出现的用户标识提示
		self.default_timeout = 20      # ；；默认超时时间
		self.child = None
		self.login()

	def expand_expect(self, expect_list):
		try:
			result = self.child.expect(expect_list, self.default_timeout)
		except EOFError:
			self.log.error("No text was read, please check reason.")

		if result[0] == -1:
			self.log.error("Expect result" + str(expect_list) + "don't exit.")
		else:
			pass
		return result

	def login(self):
		"""Connect to a remote host and login."""
		try:
			self.child = telnetlib.Telnet(self.host)
			self.expand_expect(['login: '])
			self.child.write(self.accout + '\n')
			self.expand_expect(['assword:'])
			self.child.write(self.accoutPasswd + '\n')
			self.expand_expect(self.possible_prompt)
			self.child.write("swith to root accout on host " + self.host)
			if self.RootPasswd != "":
				self.child.write("su -" + "\n")
				self.expand_expect(['assword: '])
				self.child.write(self.RootPasswd + '\n')
				self.expand_expect(self.possible_prompt)
			self.child.read_until(self.prompt)
			self.log.info("login host " + self.host + "sucessfully!")
			return True
		except:
			print("Login failed, please check ip address and accout/passwd")
			self.log.error("login host " + self.host + "failed , please check reason.")
			return False

	def send_command(self, command, sleeptime=0.5):
		"""
		Run a command on the remote host.
		:param command:
		:param sleeptime:
		:return:
		"""
		self.log.debug("Starting to execute command: " + command)
		try:
			self.child.write(command + "\n")
			if self.expand_expect(self.possible_prompt)[0] == -1:
				self.log.error("Executed command " + command + " is failed, please check it")
				return False
			else:
				time.sleep(sleeptime)
				self.log.debug("Executed command " + command + " is successful")
				return True
		except socket.error:
			self.log.error("when executed command " + command + " the connection maybe break, reconnect")
			traceback.print_exc()
			for i in range(0, 3):
				self.log.error("Telnet session is broken from " + self.host + ", reconnecting....")
				if self.login():
					break
			return False

	def get_output(self,timeout=2):
		response = self.child.read_until(self.prompt, timeout)
		self.log.debug("response: " + response)
		return self.__strip_output(response)

	def send_atomic_command(self, command):
		self.send_command(command)
		command_output = self.get_output()
		self.logout()
		return command_output

	def process_is_running(self, process_name, output_string):
		self.send_command("ps -ef | grep " + process_name + " | grep -v grep")
		output_list = [output_string]
		if self.expand_expect(output_list)[0] == -1:
			return False
		else:
			return True

	def __strip_output(self, response):
		lines = response.splitliness()
		self.log.debug("lines: " + str(lines))
		if len(lines) > 1:
			if self.prompt in lines[0]:
				lines.pop(0)
			lines.pop()
			lines = [item + '\n' for item in lines]
			return ''.join(lines)
		else:
			self.log.info("The response is blank: " + response)
			return "Null response"

	def logout(self):
		self.child.close()