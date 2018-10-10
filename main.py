from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from ym51.ym51_api import Ym_api
from random import choice
import requests
import json
from geetest.bilibili_geetest_crack import CrackGeetest
from time import sleep

class Register(object):
	mobile_emulation = {"deviceName": "Galaxy S5"}
	options = Options()
	register_url = "https://passport.bilibili.com/register/phone.html#/phone"

	def __init__(self):
		self.message = Ym_api(itemid='1191')
		self.browser = webdriver.Chrome()
		self.browser.get(self.register_url)
		self.browser.implicitly_wait(10)

	@staticmethod
	def create_user():
		seed = "qwertyuiopasdfghjklzxcvbnmQWERTYUIOPASDFGHJKLZXCVBNM1234567890"
		sa = []
		for i in range(8):
			sa.append(choice(seed))
		salt = "".join(sa)
		return salt

	def fillin(self):
		while True:
			nickname = Register.create_user()
			if json.loads(requests.get("https://passport.bilibili.com/web/generic/check/nickname?nickName={}".format(nickname)).text)['code'] == 0:
				break
		# 输入用户名
		self.browser.find_element_by_xpath('//*[@id="registerForm"]/div[1]/div/input').send_keys(nickname)
		# 输入密码
		self.browser.find_element_by_xpath('//*[@id="registerForm"]/div[3]/div/input').send_keys('a510b630')


		# 输入手机
		phone = self.message.get_mobile()
		self.browser.find_element_by_xpath('//*[@id="registerForm"]/div[5]/div/input').send_keys(phone)

		# 点击获取验证码按钮
		self.browser.find_element_by_xpath('//*[@id="registerForm"]/div[7]/button/span').click()

		sleep(3)

		input(":")

		# 输入验证码
		cap = self.message.get_text(phone)
		print(cap)
		if cap:
			self.browser.find_element_by_xpath('//*[@id="registerForm"]/div[7]/div[1]/input').send_keys(cap)
		else:
			self.message.remove_mobile(phone)
			self.browser.quit()
			return False
		# 点击同意协议
		self.browser.find_element_by_xpath('//*[@id="registerForm"]/div[8]/label/label').click()

		# 点击注册按钮
		self.browser.find_element_by_xpath('//*[@id="registerForm"]/div[9]/button/span').click()

		print("username:", phone)
		input(":")


if __name__ == '__main__':
    Register().fillin()
