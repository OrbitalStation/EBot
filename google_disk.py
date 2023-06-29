import oauth2client.client



#from pydrive.auth import GoogleAuth
# from pydrive.drive import GoogleDrive
#
#
# gauth = GoogleAuth()
# gauth.LocalWebserverAuth()
#
#
# def upload(path, filename):
#     try:
#         drive = GoogleDrive(gauth)
#
#         file = drive.CreateFile({'title': f'{filename}'})
#         file.SetContentFile(path)
#         file.Upload()
#         file.InsertPermission({
#             'type': 'anyone',
#             'value': 'anyone',
#             'role': 'reader'})
#         link = file['alternateLink']
#         file = None
#
#         return link
#
#     except Exception:
#         return False
