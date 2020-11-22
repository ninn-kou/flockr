# Group Project Tasks Distribution

## Iteration 3

MORE CODES!

- [ ] message/sendlater
- [ ] message/react
- [ ] message/unreact
- [ ] message/pin
- [ ] message/unpin
- [ ] /user/profile/uploadphoto
- [ ] standup/start
- [ ] standup/active
- [ ] standup/send
- [ ] auth/passwordreset/request
- [ ] auth/passwordreset/reset

- planning.pdf
  - planning of new features in a pdf in root directory SLDC
  - For iteration 3 you are going to produce a short report in planning.pdf and place it in the repository. The contents of this report will be a simplified approach to understanding user problems, developing requirements, and doing some early designs.
  - find 2-3 people to interview as target users - collect name and email
    - give these questions and record answers
  - analysis and spec -> document user stories
        - For each user story, add User Acceptance Criteria as notes so that you have a clear definition of when a story has been completed.
        - Once documented, generate at least one use case that attempts to tell a story of a solution that satifies the requirements elicited. You can generate a visual diagram or a more written-recipe style, as per lectures.
  - With your completed use case work, reach out to the 2-3 people you interviewed originally and inquire as to the extent to which these use cases would adequately describe the problem they're trying to solve.
  - design interface -> specify as HTTP endpoints
  - add at least one state diagram to your PDF to show how the state of the application would change based on user actions. The aim of this diagram is how to a developer understand the different states the user or application.

## Iteration 2

Joseph writing up what functions we need to implement:

```
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
```

### General Breakdown

- those new functions
- servers and requests on top of auth.py, channel.py, and channels.py

This is the delegation for iteration 2:

- Steve - message.py
- Yuhan - user.py
- Liuyuzi - other.py
- Joseph - _http.py files for auth, channel, and channels, and server.py
- Hao Ren - _http.py files for message, user and other

Things to improve in Iteration 2:

- task boards
- exception messages
- project management
