'''
Author: FSt. J
Comments: We'll use this .py file to maintain all of our user-defined functions for the project
          Note that functions within this code can be called using the following syntax
          from nfl_site.nfl_site.libraries import <my_function1>, <my_function2>, ... : for specific functions OR
          from nfl_site.nfl_site.libraries import * : for all functions
'''

'''
Author: FSt.J
Comments: Function to retrive Kaggle .csv files from Google Drive
'''
import pickle
import os.path
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request

SCOPES = ['https://www.googleapis.com/auth/drive']

# Get relative path of credentials.json file based on directory this script is in
basepath = os.path.dirname(__file__)
credspath = os.path.abspath(os.path.join(basepath, "credentials.json"))

# Function getFileList to list n files
def getFileList(n):
    # Variable creds will store user access token.  Create token if none found
    creds = None

    if os.path.exists('token.pickle'):
        with open('token.pickle', 'rb') as token:
            creds = pickle.load(token)

    # If valid creds are unavailable, request user to log in
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token: 
            creds.refresh(Request()) 
        else:
            # Specify the file path to the credential.json file.  It should be in the nfl_data path
            flow = InstalledAppFlow.from_client_secrets_file(credspath, SCOPES) 
            creds = flow.run_local_server(port=0) 
            # Save the access token in token.pickle for future use
            with open('token.pickle', 'wb') as token:
                pickle.dump(creds, token)

    # Connect to the API service
    service = build('drive', 'v3', credentials=creds)

    # Request list of first n files
    resource = service.files()
    result = resource.list(pageSize=n, fields="files(id, name)").execute()

    # return the dictionary containing the information about the files
    return result

'''
result_dict = getFileList(10)
file_list = result_dict.get('files')
for file in file_list:
    print(file['name'])
'''