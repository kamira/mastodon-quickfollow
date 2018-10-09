from __future__ import print_function
from googleapiclient.discovery import build
from httplib2 import Http
from oauth2client import file, client, tools
from quickfollow import mastodon_follow
# If modifying these scopes, delete the file token.json.
SCOPES = 'https://www.googleapis.com/auth/spreadsheets.readonly'

# The ID and range of a sample spreadsheet.
SPREADSHEET_ID = '1_S9aEfbdd0UcuFNeOdHUrKitWx8zhDeNVrrvqXJM4VM'
RANGE_NAME = 'Class Data!B2:C'

class app(mastodon_follow):
	def __init__( self  ):
		super().__init__()
		store = file.Storage('token.json')
		creds = store.get()
		if not creds or creds.invalid:
			flow = client.flow_from_clientsecrets('credentials.json', SCOPES)
			creds = tools.run_flow(flow, store)
		self.service = build('sheets', 'v4', http=creds.authorize(Http()))

	def main( self ):
		SPREADSHEET_ID = '1_S9aEfbdd0UcuFNeOdHUrKitWx8zhDeNVrrvqXJM4VM'
		RANGE_NAME = 'B2:C'
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

if __name__ == '__main__':
	task = app()
	task.main()