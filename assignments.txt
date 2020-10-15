Joseph writing up what functions we need to implement:

message/send
message/remove
message/edit

user/profile
user/profile/setname
user/profile/setemail
user/profile/sethandle

(in other.py)
users/all
admin/userpermission/change
search

General breakdown

- those new functions
- servers and requests on top of auth.py, channel.py, and channels.py

This is the delegation for iteration 2:
Steve - message.py
Yuhan - user.py
Liuyuzi - other.py
Joseph - _http.py files for auth, channel, and channels, and server.py
Hao Ren - _http.py files for message, user and other

Things to improve in Iteration 2:
- task boards
- exception messages
- project management