from mastodon import *
import re
import os.path

class mastodon_follow():
	def __init__( self ):

		userdata = ""
		with open('acpwd.txt', 'r') as f:
			userdata = f.read().replace('\n', '')
			userdata = userdata.split(',')

		self.account = userdata[0]
		self.password = userdata[1]
		self.domain = userdata[2]
		self.tootit = userdata[3].upper()
		try:
			print(os.path.isfile("app.secret"))
			if not os.path.isfile("app.secret"):
				Mastodon.create_app(
					'[Python] QuickFollower',
					api_base_url = self.domain,
					to_file = 'app.secret',
					scopes = [ 'read', 'write', 'follow', 'push' ]
				)

				self.mastodon = Mastodon(
					client_id = 'app.secret',
					api_base_url = self.domain
				)
				self.mastodon.log_in(
					self.account,
					self.password,
					to_file = 'user.secret'
				)
			else:
				self.mastodon = Mastodon(
					access_token = 'user.secret',
					api_base_url = self.domain
				)
		except Exception as e:
			print(e)



	def follow_someone( self, target ):
		domain_less = re.sub(r"http[s]?://", "", self.domain)
		try:
			if self.tootit == "TRUE":
				self.mastodon.toot('I follow @{}@{} by QuickFollower, which made by @h4ru75uk1@pawoo.net'.format(target[1], target[0]))
			if target[0] == domain_less:
				self.mastodon.follows(target[1])
			else:
				self.mastodon.follows('{}@{}'.format(target[1], target[0]))
		except Exception as e:
			if self.tootit == "TRUE":
				self.mastodon.toot('[Warning] Exception Event: {} | Follow Failed: {}@{}'.format(e, target[1], target[0]))