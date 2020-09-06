# COMP1531 Major Project

A video describing this project and the background here can be found here.

## Aims:

* To provide students with hands on experience testing, developing, and maintaining a backend server in python.
* To develop students' problem solving skills in relation to the software development lifecycle.
* Learn to work effectively as part of a team by managing your project, planning, and allocation of responsibilities among the members of your team.
* Gain experience in collaborating through the use of a source control and other associated modern team-based tools.
* Apply appropriate design practices and methodologies in the development of their solution
* Develop an appreciation for product design and an intuition of how a typical customer will use a product.

## Changelog

* Nothing yet.

## Overview

An overview of this project will be provided toward the end of week 1.

To manage the transition from trimesters to hexamesters in 2020, UNSW has established a new focus on building an in-house digital collaboration and communication tool for groups and teams to support the high intensity learning environment.

Rather than re-invent the wheel, UNSW has decided that it finds the functionality of **<a href="https://flock.com/">Flock</a>** to be nearly exactly what it needs. For this reason, UNSW has contracted out Pineapple Pty Ltd (a small software business run by Hayden) to build the new product. In UNSW's attempt to connect with the younger and more "hip" generation that fell in love with flickr, Tumblr, etc, they would like to call the new UNSW-based product **flockr**.

Pineapple Pty Ltd has sub-contracted two software firms:

* Catdog Pty Ltd (two software developers, Sally and Bob, who will build the initial web-based GUI)
* YourTeam Pty Ltd (a team of talented misfits completing COMP1531 in 20T1), who will build the backend python server and possibly assist in the GUI later in the project

In summary, UNSW contracts Pineapple Pty Ltd, who sub contracts:

* Catdog (Sally and Bob) for front end work
* YourTeam (you and others) for backend work

Pineapple Pty Ltd met with Sally and Bob (the front end development team) 2 weeks ago to brief them on this project. While you are still trying to get up to speed on the requirements of this project, Sally and Bob understand the requirements of the project very well.

Because of this they have already specified a **common interface** for the front end and backend to operate on. This allows both parties to go off and do their own development and testing under the assumption that both parties comply will comply with the common interface. This is the interface **you are required to use**

Beside the information available in the interface that Sally and Bob provided, you have been told (so far) that the features of flockr that UNSW would like to see implemented include:

1. Ability to login, register if not registered, and log out
2. Ability to reset password if forgotten it
3. Ability to see a list of channels
4. Ability to create a channel, join a channel, invite someone else to a channel, and leave a channel
5. Within a channel, ability to view all messages, view the members of the channel, and the details of the channel
6. Within a channel, ability to send a message now, or to send a message at a specified time in the future
7. Within a channel, ability to edit, remove, pin, unpin, react, or unreact to a message
8. Ability to view user anyone's user profile, and modify a user's own profile (name, email, handle, and profile photo)
9. Ability to search for messages based on a search string
10. Ability to modify a user's admin privileges: (MEMBER, OWNER)
11. Ability to begin a "standup", which is an X minute period where users can send messages that at the end of the period will automatically be collated and summarised to all users

The specific capabilities that need to be built for this project are described in the interface at the bottom.

## Progress check-in

During your lab class, in weeks without demonstrations (see below), you and your team will conduct a short stand-up in the presence of your tutor. Each member of the team will briefly state what they have done in the past week, what they intend to do over the next week, and what issues they faced or are currently facing. This is so your tutor, who is acting as a representative of the client, is kept informed of your progress. They will make note of your presence and may ask you to elaborate on the work you've done.

## Iteration 1: Test Driven Development

### Task

In this iteration, you are expected to:

1. Create extensive tests (using pytest) for all of the functions in the agreed upon interface.

    These should all be in files of the formn `*_test.py`. See below for more information.

    Your tests will be automarked to assist in determining your performance mark.

2. Write assumptions that you feel you are making in your interpretation of the specification and of the functions provided.

    Write these in markdown in `assumptions.md`.

You are **not** expected to begin developing or completing the actual functions themselves.

The first iteration does not include all capabilities. Further capabilities will be introduced in subsequent iterations.

You will be heavily marked for your use of thoughtful project management and use of git effectively. The degree to which your team works effectively will also be assessed.

The `assumptions.md` file described above should be in the root of your repository. If you've not written markdown before (which we assume most of you haven't), it's not necessary to research the format. Markdown is essentially plain text with a few extra features for basic formatting. You can just stick with plain text if you find that easier.

Do NOT attempt to try and write or start a web server. Don't overthink how these functions are meant to connect to a frontend yet. This is for the next iteration. In this iteration you are just focusing on the high level functions that will eventually be used for a web server.


### Tests

Our recommendation is to break all of the functions to test up into 1 or many files (this is a decision for you and your team), and then create test files in the same directory as the files the tests are testing. An example of this has been done with:

* `/src/echo.py`
* `/src/echo_test.py`

A number of stub files have been added to your /src/ folder in your repository. These files are:
 * `auth.py`
 * `channel.py`
 * `channels.py`
 * `user.py`
 * `message.py`
 * `other.py`

**Do not modify these files**, otherwise you will be unable to get your 40% performance marking. When automarking your tests, we will replace these stub functions with actual functions. If you're trying to implement/finish these stubs in order to complete your tests, you're approaching testing wrong.

Besides those files, you have complete control over how you structure your tests and any other helper functions. You can put all your tests in one file, or many files, or in sub-directories. That is up to you.

Stub functions are dummy implementations of functions that allow them to be trivially tested. E.G. A stub function for a user to login may always return a dummy auth token "123456". This will allow your tests to successfully compile. Of course, because these functions aren't implemented it means that your pytests will fail, but that's OK.

### Submission

This iteration is due to be submitted at 8pm Sunday 4th October (**week 3**). You will then be demonstrating this in your week 4 lab. All team members **must** attend this lab session, or they will not receive a mark.

At the due date provided, we will automatically collect and submit the code that is on the master branch of your group repositories. Ensure that your most recent code is on the master branch on gitlab. That is the code that you will be demonstrating and we will be marking.. 

### Marking Criteria

|Section|Weighting|Criteria|
|---|---|---|
|Pytests|40%| <ul><li>Demonstrated an understanding of good test **coverage**</li><li>Demonstrated an understanding of the importance of **clarity** on the communication of test purposes</li><li>Demonstrated an understanding of thoughtful test **design**</li><li>Performance against an automatic marking system with both functional and dysfunctional implementations</li></ul>|
|Git Practices|20%|<ul><li>Meaningful and informative git commit names being used</li><li>Effective use of merge requests (from branches being made) across the team (minimum 12 MRs)</li></ul>|
|Project Management|20%|<ul><li>Effective use of course-provided slack, demonstrating an ability to communicate and manage effectivelly digitally</li><li>Use of task board on Gitlab to track and manage tasks</li><li>Effective use of agile methods such as standups</li></ul>|
|Teamwork|10%|<ul><li>A generally equal contribution between team members</li><li>Clear evidence of reflection on group's performance and state of the team, with initiative to improve in future iterations</li></ul>|
|Assumptions markdown file|10%|<ul><li>Clear and obvious effort and time gone into thinking about possible assumptions that are being made when interpreting the specification</li></ul>|

### Demonstration

When you demonstrate this iteration in your week 4 lab, it will consist of a 15 minute Q&A in front of your tutorial class.

## Interface specifications from Sally and Bob

### Data types

|Variable name|Type|
|-------------|----|
|named exactly **email**|string|
|named exactly **id**|integer|
|named exactly **length**|integer|
|named exactly **password**|string|
|named exactly **token**|string|
|named exactly **message**|string|
|contains substring **name**|string|
|contains substring **code**|string|
|has prefix **is_**|boolean|
|has prefix **time_**|integer (unix timestamp), [check this out](https://www.tutorialspoint.com/How-to-convert-Python-date-to-Unix-timestamp)|
|has suffix **_id**|integer|
|has suffix **_url**|string|
|has suffix **_str**|string|
|has suffix **end**|integer|
|has suffix **start**|integer|
|(outputs only) named exactly **user**|Dictionary containing u_id, email, name_first, name_last, handle_str|
|(outputs only) named exactly **users**|List of dictionaries, where each dictionary contains types u_id, email, name_first, name_last, handle_str|
|(outputs only) named exactly **messages**|List of dictionaries, where each dictionary contains types { message_id, u_id, message, time_created  }|
|(outputs only) named exactly **channels**|List of dictionaries, where each dictionary contains types { channel_id, name }|
|(outputs only) name ends in **members**|List of dictionaries, where each dictionary contains types { u_id, name_first, name_last }|

### Token
Many of these functions (nearly all of them) need to be called from the perspective of a user who is logged in already. When calling these "authorised" functions, we need to know:
1) Which user is calling it
2) That the person who claims they are that user, is actually that user

We could solve this trivially by storing the user ID of the logged in user on the front end, and every time the front end (from Sally and Bob) calls your background, they just sent a user ID. This solves our first problem (1), but doesn't solve our second problem! Because someone could just "hack" the front end and change their user id and then log themselves in as someone else.

To solve this when a user logs in or registers the backend should return a "token" (an authorisation hash) that the front end will store and pass into most of your functions in future. When these "authorised" functions are called, you can check if a token is valid, and determine the user ID.

### Permissions:
 * Members in a channel have one of two channel permissions.
   1) Owner of the channel (the person who created it, and whoever else that creator adds)
   2) Members of the channel
 * Flockr user's have two global permissions
   1) Owners, who can also modify other owners' permissions.
   2) Members, who do not have any special permissions (permission_id 3)
 * All flockr users are by default members, except for the very first user who signs up, who is an owner

A user's primary permissions are their global permissions. Then the channel permissions are layered on top. For example:
* An owner of flockr has owner privileges in every channel they've joined
* A member of flockr is a member in channels they are not owners of
* A member of flockr is an owner in channels they are owners of

### Errors for all functions

**AccessError**
 * For all functions except auth_register, auth_login
 * Error thrown when token passed in is not a valid token

### Pagination
The behaviour in which channel_messages returns data is called **pagination**. It's a commonly used method when it comes to getting theoretially unbounded amounts of data from a server to display on a page in chunks. Most of the timelines you know and love - Facebook, Instagram, LinkedIn - do this.

For example, if we imagine a user with token "12345" is trying to read messages from channel with ID 6, and this channel has 124 messages in it, 3 calls from the client to the server would be made. These calls, and their corresponding return values would be:
 * channel_messages("12345", 6, 0) => { [messages], 0, 50 }
 * channel_messages("12345", 6, 50) => { [messages], 50, 100 }
 * channel_messages("12345", 6, 100) => { [messages], 100, -1 }

### Interface

|Function Name|Parameters|Return type|Exceptions|Description|
|------------|-------------|----------|-----------|----------|
|auth_login|(email, password)|{ u_id, token }|**InputError** when any of:<ul><li>Email entered is not a valid email using the method provided [here](https://www.geeksforgeeks.org/check-if-email-address-valid-or-not-in-python/) (unless you feel you have a better method)</li><li>Email entered does not belong to a user</li><li>Password is not correct</li></ul> | Given a registered users' email and password and generates a valid token for the user to remain authenticated |
|auth_logout|(token)|{ is_success }|N/A|Given an active token, invalidates the taken to log the user out. If a valid token is given, and the user is successfully logged out, it returns true, otherwise false. |
|auth_register|(email, password, name_first, name_last)|{ u_id, token }|**InputError** when any of:<ul><li>Email entered is not a valid email using the method provided [here](https://www.geeksforgeeks.org/check-if-email-address-valid-or-not-in-python/) (unless you feel you have a better method).</li><li>Email address is already being used by another user</li><li>Password entered is less than 6 characters long</li><li>name_first not is between 1 and 50 characters in length</li><li>name_last is not between 1 and 50 characters in length</ul>|Given a user's first and last name, email address, and password, create a new account for them and return a new token for authentication in their session. A handle is generated that is the concatentation of a lowercase-only first name and last name. If the concatenation is longer than 20 characters, it is cutoff at 20 characters. If the handle is already taken, you may modify the handle in any way you see fit to make it unique. |
|channel_invite|(token, channel_id, u_id)|{}|**InputError** when any of:<ul><li>channel_id does not refer to a valid channel that the authorised user is part of.</li><li>u_id does not refer to a valid user</li></ul>**AccessError** when<ul><li>the authorised user is not already a member of the channel</li>|Invites a user (with user id u_id) to join a channel with ID channel_id. Once invited the user is added to the channel immediately|
|channel_details|(token, channel_id)|{ name, owner_members, all_members }|**InputError** when any of:<ul><li>Channel ID is not a valid channel</li></ul>**AccessError** when<ul><li>Authorised user is not a member of channel with channel_id</li></ul>|Given a Channel with ID channel_id that the authorised user is part of, provide basic details about the channel|
|channel_messages|(token, channel_id, start)|{ messages, start, end }|**InputError** when any of:<ul><li>Channel ID is not a valid channel</li><li>start is greater than the total number of messages in the channel</li></ul>**AccessError** when<ul><li>Authorised user is not a member of channel with channel_id</li></ul>|Given a Channel with ID channel_id that the authorised user is part of, return up to 50 messages between index "start" and "start + 50". Message with index 0 is the most recent message in the channel. This function returns a new index "end" which is the value of "start + 50", or, if this function has returned the least recent messages in the channel, returns -1 in "end" to indicate there are no more messages to load after this return.|
|channel_leave|(token, channel_id)|{}|**InputError** when any of:<ul><li>Channel ID is not a valid channel</li></ul>**AccessError** when<ul><li>Authorised user is not a member of channel with channel_id</li></ul>|Given a channel ID, the user removed as a member of this channel|
|channel_join|(token, channel_id)|{}|**InputError** when any of:<ul><li>Channel ID is not a valid channel</li></ul>**AccessError** when<ul><li>channel_id refers to a channel that is private (when the authorised user is not an admin)</li></ul>|Given a channel_id of a channel that the authorised user can join, adds them to that channel|
|channel_addowner|(token, channel_id, u_id)|{}|**InputError** when any of:<ul><li>Channel ID is not a valid channel</li><li>When user with user id u_id is already an owner of the channel</li></ul>**AccessError** when the authorised user is not an owner of the flockr, or an owner of this channel</li></ul>|Make user with user id u_id an owner of this channel|
|channel_removeowner|(token, channel_id, u_id)|{}|**InputError** when any of:<ul><li>Channel ID is not a valid channel</li><li>When user with user id u_id is not an owner of the channel</li></ul>**AccessError** when the authorised user is not an owner of the flockr, or an owner of this channel</li></ul>|Remove user with user id u_id an owner of this channel|
|channels_list|(token)|{ channels }|N/A|Provide a list of all channels (and their associated details) that the authorised user is part of|
|channels_listall|(token)|{ channels }|N/A|Provide a list of all channels (and their associated details)|
|channels_create|(token, name, is_public)|{ channel_id }|**InputError** when any of:<ul><li>Name is more than 20 characters long</li></ul>|Creates a new channel with that name that is either a public or private channel|
|message_send|(token, channel_id, message)|{ message_id }|**InputError** when any of:<ul><li>Message is more than 1000 characters</li></ul>**AccessError** when: <li> the authorised user has not joined the channel they are trying to post to</li></ul>|Send a message from authorised_user to the channel specified by channel_id|
|message_remove|(token, message_id)|{}|**InputError** when any of:<ul><li>Message (based on ID) no longer exists</li></ul>**AccessError** when none of the following are true:<ul><li>Message with message_id was sent by the authorised user making this request</li><li>The authorised user is an admin or owner of this channel or the flockr</li></ul>|Given a message_id for a message, this message is removed from the channel|
|message_edit|(token, message_id, message)|{}|**AccessError** when none of the following are true:<ul><li>Message with message_id was sent by the authorised user making this request</li><li>The authorised user is an admin or owner of this channel or the flockr</li></ul>|Given a message, update it's text with new text. If the new message is an empty string, the message is deleted.|
|user_profile|(token, u_id)|{ user }|**InputError** when any of:<ul><li>User with u_id is not a valid user</li></ul>|For a valid user, returns information about their email, first name, last name, and handle|
|user_profile_setname|(token, name_first, name_last)|{}|**InputError** when any of:<ul><li>name_first is not between 1 and 50 characters in length</li><li>name_last is not between 1 and 50 characters in length</ul></ul>|Update the authorised user's first and last name|
|user_profile_setemail|(token, email)|{}|**InputError** when any of:<ul><li>Email entered is not a valid email using the method provided [here](https://www.geeksforgeeks.org/check-if-email-address-valid-or-not-in-python/) (unless you feel you have a better method).</li><li>Email address is already being used by another user</li>|Update the authorised user's email address|
|user_profile_sethandle|(token, handle_str)|{}|**InputError** when any of:<ul><li>handle_str must be between 3 and 20 characters</li><li>handle is already used by another user</li></ul>|Update the authorised user's handle (i.e. display name)|
|users_all|(token)|{ users}|N/A|Returns a list of all users and their associated details|
|search|(token, query_str)|{ messages }|N/A|Given a query string, return a collection of messages in all of the channels that the user has joined that match the query|


## Due Dates and Weightings

|Iteration|Code and report due                  |Demonstration to tutor(s)      |Assessment weighting of project (%)|
|---------|-------------------------------------|-------------------------------|-----------------------------------|
|   1     |8pm Sunday 4th October (**week 3**)   |In YOUR **week 4** laboratory  |30%                                |
|   2     |8pm Monday 27th October (**week 7**)   |In YOUR **week 7** laboratory  |40%                                |
|   3     |8pm Sunday 15th November (**week 9**)   |In YOUR **week 10** laboratory |30%                                |

There is no late penalty, as we do not accept late submissions.

## Expectations

While it is up to you as a team to decide how work is distributed between you, for the purpose of assessment there are certain key criteria all members must.

* Code contribution
* Documentation contribution
* Usage of git/GitLab
* Attendance
* Peer assessment
* Academic conduct

The details of each of these is below.

While, in general, all team members will receive the same mark (a sum of the marks for each iteration), **if you as an individual fail to meet these criteria your final project mark may be scaled down**, most likely quite significantly.

### Code contribution

All team members must contribute code to the project. Tutors will assess the degree to which you have contributed by looking at your **git history** and analysing lines of code, number of commits, timing of commits, etc. If you contribute significantly less code than your team members, your work will be closely examined to determine what scaling needs to be applied.

### Documentation contribution

All team members must contribute documentation to the project. Tutors will assess the degree to which you have contributed by looking at your **git history** but also **asking questions** (essentially interviewing you) during your demonstration.

Note that, **contributing more documentation is not a substitute for not contributing code**.

### Peer Assessment

You will be required to complete a form in week 10 where you rate each team member's contribution to the project and leave any comments you have about them. Information on how you can access this form will be released closer to Week 10. Your other team members will **not** be able to see how you rated them or what comments you left.

If your team members give you a less than satisfactory rating, your contribution will be scrutinised and you may find your final mark scaled down.

### Attendance

It is generally assumed that all team members will be present at the demonstrations and at weekly check-ins. If you're absent for more than 80% of the weekly check-ins or any of the demonstrations, your mark may be scaled down.

If, due to exceptional circumstances, you are unable to attend your lab for a demonstration, inform your tutor as soon as you can so they can record your absence as planned.

### Plagiarism

The work you and your group submit must be your own work. Submission of work partially or completely derived from any other person or jointly written with any other person is not permitted. The penalties for such an offence may include negative marks, automatic failure of the course and possibly other academic discipline. Assignment submissions will be examined both automatically and manually for such submissions.

Relevant scholarship authorities will be informed if students holding scholarships are involved in an incident of plagiarism or other misconduct.

Do not provide or show your project work to any other person, except for your group and the teaching staff of COMP1531. If you knowingly provide or show your assignment work to another person for any reason, and work derived from it is submitted you may be penalized, even if the work was submitted without your knowledge or consent. This may apply even if your work is submitted by a third party unknown to you.

Note, you will not be penalized if your work has the potential to be taken without your consent or knowledge.
