from __future__ import print_function
import pickle
import os.path
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request

# Download the helper library from https://www.twilio.com/docs/python/install
from twilio.rest import Client

SCOPES = ['https://www.googleapis.com/auth/spreadsheets.readonly']

# The ID and range of a sample spreadsheet.
#For id, copy the sequence between /d/ and /edit in the url
SAMPLE_SPREADSHEET_ID = 'put-spreadsheet-id-here' #ID of spreadsheet to scrape, generic form
SAMPLE_RANGE_NAME = '!A2:G' #All data columns to collect, format 'FirstCellToStart:LastColumnToEnd'

 #Dictionary to hold all name:number key-value pairs from the spreadsheet
users = {
}

#Main method - sends messages to everyone
def main():
    """Shows basic usage of the Sheets API.
    Prints values from a sample spreadsheet.
    """
    creds = None
    # The file token.pickle stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    if os.path.exists('token.pickle'):
        with open('token.pickle', 'rb') as token:
            creds = pickle.load(token, encoding="latin1")

    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open('token.pickle', 'wb') as token:
            pickle.dump(creds, token)

    service = build('sheets', 'v4', credentials=creds)

    # Call the Sheets API
    sheet = service.spreadsheets()
    result = sheet.values().get(spreadsheetId=SAMPLE_SPREADSHEET_ID,
                                range=SAMPLE_RANGE_NAME).execute()
    values = result.get('values', [])

    if not values:
        print('No data found.')
    else:
        print('Name, Number:')
        for row in values:
            try:
                # Print columns B (names) and C (numbers), which correspond to indices 1 and 2.
                print('%s, %s' % (row[1], row[5]))
                users[row[1]] = row[5]  #Sets each name as a key, and each number as a value
            except:
                print(row[1] + " - No number for this user.")

        #Messaging portion of program
        account_sid = 'twilio-sid-here' #sid from twilio
        auth_token = 'twilio-auth-token-here' #auth token from twilio
        client = Client(account_sid, auth_token)
        for name in users: #loop through each name in the dictionary
            message = client.messages \
                    .create(
                         body= "Automated reminder: " + "\n" + "Hey " + name + ", we hope you're doing well! "  + "\n" + "\n" + "The CS Club's crossover event with SJSU's ICPC team will be happening today (4/9) @ 2:00pm. Come join us to get introduced to competitive programming!" + "\n" + "\n" + "Participants have a chance to win two $10 starbucks giftcards. Zoom link: google.com",
                         from_='twilio-number-here', #From number - given by Twilio
                         to= "+1" + users[name] #Concatenate the user's number with the country code prefix
                     ) #Message is sent to each user

#Main method 2 - used to test messages only to self
def main2():
    """Shows basic usage of the Sheets API.
    Prints values from a sample spreadsheet.
    """
    creds = None
    # The file token.pickle stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    if os.path.exists('token.pickle'):
        with open('token.pickle', 'rb') as token:
            creds = pickle.load(token, encoding="latin1")

    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open('token.pickle', 'wb') as token:
            pickle.dump(creds, token)

    service = build('sheets', 'v4', credentials=creds)

    # Call the Sheets API
    sheet = service.spreadsheets()
    result = sheet.values().get(spreadsheetId=SAMPLE_SPREADSHEET_ID,
                                range=SAMPLE_RANGE_NAME).execute()
    values = result.get('values', [])

    if not values:
        print('No data found.')
    else:
        print('Name, Number:')
        for row in values:
            try:
                # Print columns B (names) and C (numbers), which correspond to indices 1 and 2.
                print('%s, %s' % (row[1], row[5]))
                users[row[1]] = row[5]  #Sets each name as a key, and each number as a value
            except:
                print(row[1] + " - No number for this user.")


        #Messaging portion of program
        account_sid = 'twilio-sid-here' #sid from twilio
        auth_token = 'twilio-auth-token-here' #auth token from twilio
        client = Client(account_sid, auth_token)
        message = client.messages \
                .create(
                        body= "Automated Reminder: " + "\n" + "Hey your-name-here, we hope you're doing well" + "! " + "\n" + "\n" + "The CS Club's crossover event with SJSU's ICPC team will be happening today (4/9) @ 2:00pm. Come join us to get introduced to competitive programming!" + "\n" + "\n" + "Participants have a chance to win two $10 starbucks giftcards and a face mask. Zoom link: https://sjsu.zoom.us/j/87156265655?pwd=b0dEZUJ1UFI4cGRuSkUyZ1dWaTIvUT09",
                        from_='twilio-number-here', #From number - given by Twilio
                        to= "+1" + users['your-name-here'] #Concatenates the user's number with the country code prefix
                       ) #Message is sent to you
        print("New Line" + "\n");

        #print all the other users / numbers to verify what data is parsed
        for user in users:
            print(user, users[user])

#change function call to main2() to test individual message, main() to send to all
if __name__ == "__main__":
    main2();
