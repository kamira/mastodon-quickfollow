from __future__ import print_function
from googleapiclient.discovery import build
from httplib2 import Http
from oauth2client import file, client, tools
from quickfollow import mastodon_follow
import datetime
import re
# If modifying these scopes, delete the file token.json.
SCOPES = 'https://www.googleapis.com/auth/spreadsheets'

# The ID and range of a sample spreadsheet.
SPREADSHEET_ID = '1_S9aEfbdd0UcuFNeOdHUrKitWx8zhDeNVrrvqXJM4VM'
RANGE_NAME = 'Class Data!B2:C'

# REGEXP
EMAIL_REGEX = re.compile(r"[^@]+@[^@]+\.[^@]+")
DOMAIN_REGEX = re.compile(r"http[s]?:\/\/(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\), ]|(?:%[0-9a-fA-F][0-9a-fA-F]))+")
YESNO_REGEX = re.compile(r"[yYnN]")
YES_REGEX = re.compile(r'[yY]')

class app(mastodon_follow):
	def __init__( self  ):
		self.information_input()
		super().__init__()
		store = file.Storage('token.json')
		creds = store.get()
		if not creds or creds.invalid:
			flow = client.flow_from_clientsecrets('credentials.json', SCOPES)
			creds = tools.run_flow(flow, store)
		self.service = build('sheets', 'v4', http=creds.authorize(Http()), credentials=None)

	def main( self ):
		SPREADSHEET_ID = '1_S9aEfbdd0UcuFNeOdHUrKitWx8zhDeNVrrvqXJM4VM'
		RANGE_NAME = 'B2:C'

		if self.addfollowlist :
			RANGE_ = "A:C"
			value_input_option = 'RAW'  # TODO: Update placeholder value.
			# How the input data should be inserted.
			insert_data_option = 'INSERT_ROWS'  # TODO: Update placeholder value.

			value_range_body = {
				# TODO: Add desired entries to the request body.
				"values": [
					[datetime.datetime.now().strftime("%Y/%m/%d %H:%M:%S"), re.sub( r"http[s]?://", "", self.domain ), self.username]
				],
				"range": "A:C",
				"majorDimension": "ROWS"
			}
			print(value_range_body)
			request = self.service.spreadsheets().values().append( spreadsheetId = SPREADSHEET_ID , range = RANGE_,
																   valueInputOption = value_input_option,
																   insertDataOption = insert_data_option,
																   body = value_range_body )
			print(request.execute())


		result = self.service.spreadsheets().values().get( spreadsheetId = SPREADSHEET_ID, range = RANGE_NAME ).execute()
		values = result.get( 'values', [ ] )

		if not values :
			print( 'No data found.' )
		else :
			print( 'Name, Major:' )
		for row in values :
		# Print columns A and E, which correspond to indices 0 and 4.
			print( row[ 0 ], row[ 1 ] )
			super().follow_someone(row)

	def information_input( self ):
		while True:
			self.account = ""
			self.password = ""
			self.domain = ""
			self.tootit = ""
			self.addfollowlist = ""
			check = ""
			while not EMAIL_REGEX.match(self.account):
				self.account = input("請輸入您申請 Mastodon 的電子信箱 : ")
			while len(self.password) < 8:
				self.password = input("請輸入您的 Mastodon 密碼: ")
			while not DOMAIN_REGEX.match(self.domain):
				self.domain = input("請輸入您的 Mastodon 網站節點域名(ex. https://pawoo.net): ")
			while not (YESNO_REGEX.match(self.tootit) and len(self.tootit) == 1):
				self.tootit = input( "是否在 FOLLOW 之後貼文? (y/n) " )
			if YES_REGEX.match(self.tootit):
				self.tootit = True
			else:
				self.tootit = False
			while not (YESNO_REGEX.match(self.addfollowlist) and len(self.addfollowlist) == 1):
				self.addfollowlist = input( "是否加入 FOLLOW 清單? (y/n) " )
			if YES_REGEX.match(self.addfollowlist):
				self.addfollowlist = True
			else:
				self.addfollowlist = False
			if self.addfollowlist :
				self.username = input("請輸入您的 Mastodon 帳號 ID: ")

			print("請確認以下資料是否正確")
			print("{:<5} {}".format("電子信箱", self.account))
			print("{:<5} {}".format("密碼", self.password))
			print("{:<5} {}".format("網域", self.domain))
			if self.tootit:
				print("FOLLOW 後貼文")
			if self.addfollowlist:
				print("自動加入 FOLLOW 清單")

			while not (YESNO_REGEX.match(check) and len(check) == 1):
				check = input( "是否正確? (y/n) " )
			if YES_REGEX.match(check):
				break

if __name__ == '__main__':
	task = app()
	task.main()