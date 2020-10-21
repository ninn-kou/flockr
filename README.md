# COMP1531 Major Project

## Changelog

 * 08/10: Added section 6.8
 * 08/10: Removed any reference to "admin", clarity about implementing entire interface
 * 12/10: Clarified that even if you modify the handle it must remain less than 20 characters
 * 20/10: Replaced instances of "Slackr" permissions with "Flockr"
## Contents

  1. Aims
  2. Overview
  3. Iteration 1: Basic functionality and tests
  4. Iteration 2: Not yet released
  5. Iteration 3: Not yet released
  6. Interface specifications
  7. Due Dates and Weightings
  8. Other Expectations
  9. Plagiarism

## 1. Aims:

* To provide students with hands on experience testing, developing, and maintaining a backend server in python.
* To develop students' problem solving skills in relation to the software development lifecycle.
* Learn to work effectively as part of a team by managing your project, planning, and allocation of responsibilities among the members of your team.
* Gain experience in collaborating through the use of a source control and other associated modern team-based tools.
* Apply appropriate design practices and methodologies in the development of their solution
* Develop an appreciation for product design and an intuition of how a typical customer will use a product.

## 2. Overview

To manage the transition from trimesters to hexamesters in 2020, UNSW has established a new focus on building an in-house digital collaboration and communication tool for groups and teams to support the high intensity learning environment.

Rather than re-invent the wheel, UNSW has decided that it finds the functionality of **<a href="https://flock.com/">Flock</a>** to be nearly exactly what it needs. For this reason, UNSW has contracted out Pineapple Pty Ltd (a small software business run by Hayden) to build the new product. In UNSW's attempt to connect with the younger and more "hip" generation that fell in love with flickr, Tumblr, etc, they would like to call the new UNSW-based product **flockr**.

Pineapple Pty Ltd has sub-contracted two software firms:

* Catdog Pty Ltd (two software developers, Sally and Bob, who will build the initial web-based GUI)
* YourTeam Pty Ltd (a team of talented misfits completing COMP1531 in 20T3), who will build the backend python server and possibly assist in the GUI later in the project

In summary, UNSW contracts Pineapple Pty Ltd, who sub contracts:

* Catdog (Sally and Bob) for front end work
* YourTeam (you and others) for backend work

Pineapple Pty Ltd met with Sally and Bob (the front end development team) 2 weeks ago to brief them on this project. While you are still trying to get up to speed on the requirements of this project, Sally and Bob understand the requirements of the project very well.

Because of this they have already specified a **common interface** for the frontend and backend to operate on. This allows both parties to go off and do their own development and testing under the assumption that both parties comply will comply with the common interface. This is the interface **you are required to use**

Besides the information available in the interface that Sally and Bob provided, you have been told (so far) that the features of flockr that UNSW would like to see implemented include:

1. Ability to login, register if not registered, and log out
2. Ability to reset password if forgotten
3. Ability to see a list of channels
4. Ability to create a channel, join a channel, invite someone else to a channel, and leave a channel
5. Within a channel, ability to view all messages, view the members of the channel, and the details of the channel
6. Within a channel, ability to send a message now, or to send a message at a specified time in the future
7. Within a channel, ability to edit, remove, pin, unpin, react, or unreact to a message
8. Ability to view user anyone's user profile, and modify a user's own profile (name, email, handle, and profile photo)
9. Ability to search for messages based on a search string
10. Ability to modify a user's admin permissions: (MEMBER, OWNER)
11. Ability to begin a "standup", which is an X minute period where users can send messages that at the end of the period will automatically be collated and summarised to all users

The specific capabilities that need to be built for this project are described in the interface at the bottom. This is clearly a lot of features, but not all of them are to be implemented at once (see below)

## 3. Iteration 1: Basic functionality and tests

Complete. Please see commit history to view old iteration info.

## 4. Iteration 2

### 4.1. Task

**NOTE:** In merging the instructions for this iteration into your repo, you may get a failed pipeline. This is most likely because your code is not pylint compliant. If this is the case, that is the *first* thing you should address for this iteration. It is important you have a *stable* master branch before proceeding to add additional features.

In this iteration, more features were added to the specification, and the focus has been changed to HTTP endpoints. Many of the theory surrounding iteration 2 will be covered in week 4-6 lectures. Note that there will still be 1 or 2 features of the frontend that will not work because the routes will not appear until iteration 3.

In this iteration, you are expected to:

1. Implement and test the HTTP Flask server according to the entire interface provided in the specification.

    Part of this section may be automarked.

    Pylint has been added to your continuous integration file, meaning that code that isn't pylint compliant will now fail the pipeline. The provided `.pylintrc` file is *very* lenient, so there is no reason you should have to disable any additional checks.

    Additionally, CI pipelines will measure *branch* coverage for all `.py` files that aren't tests. The coverage percentage for master is visible in a badge at the top of this repo and changes in coverage will appear in Merge Requests. Do note that coverage of `server.py` is not measured, nor will what is executed by your HTTP tests. This is because, when running HTTP tests, the server is run in a separate process.

    Your implementation should build upon your work in iteration 1, and ideally your HTTP layer is just a wrapper for underlying functions you've written that handle the logic. Your implementation will rely on topics taught in week 4 (HTTP servers and testing) as well as week 5 (authentication and authorisation).

    You can structure your tests however you choose, as long as they are appended with `_test.py`. It's important you consider how to separate (or combine) your integration tests from iteration 1 with the extra integration tests (HTTP with requests library) in iteration 2. You will be marked on both tests being present/used in this iteration. **An example of a HTTP test has been provided for you in `src/echo_http_test.py`**.

2. Continue demonstrating effective project management and effective git usage

    Part of this section may be automarked.

    You will be heavily marked for your use of thoughtful project management and use of git effectively. The degree to which your team works effectively will also be assessed.

To run the server you should always use the command

```bash
python3 src/server.py
```

This will start the server on the next available port. If you get any errors relating to `flask_cors`, ensure you have installed all the necessary Python libraries for this course (the list of libraries was updated for this iteration). You can do this with:

```bash
pip3 install $(curl https://www.cse.unsw.edu.au/~cs1531/20T3/requirements.txt)
```

A frontend has been built by Sally & Bob that you can use in this iteration, and use your backend to power it (note: an incomplete backend will mean the frontend cannot work). **You can, if you wish, make changes to the frontend code, but it is not required for this iteration.** The source code for the frontend is only provided for your own fun or curiosity.

### 4.2. Implementing and testing features

You should first approach this project by considering its distinct "features". Each feature should add some meaningful functionality to the project, but still be as small as possible. You should aim to size features as the smallest amount of functionality that adds value without making the project more unstable. For each feature you should:

1. Create a new branch.
2. Write tests for that feature and commit them to the branch.
3. Implement that feature.
4. Make any changes to the tests such that they pass with the given implementation. You should not have to do a lot here. If you find that you are, you're not spending enough time on step 2.
5. Create a merge request for the branch.
6. Get someone in your team who **did not** work on the feature to review the merge request. When reviewing, **not only should you ensure the new feature has tests that pass, but you should also check that the coverage percentage has not been significantly reduced.**
7. Fix any issues identified in the review.
8. Merge the merge request into master.

For this project, a feature is typically sized somewhere between a single function, and a whole file of functions (e.g. `auth.py`). It is up to you and your team to decide what each feature is.

There is no requirement that each feature be implemented by only one person. In fact, we encourage you to work together closely on features, especially to help those who may still be coming to grips with python.

Please pay careful attention to the following:

Your tests, keep in mind the following:
* We want to see **evidence that you wrote your tests before writing the implementation**. As noted above, the commits containing your initial tests should appear *before* your implementation for every feature branch. If we don't see this evidence, we will assume you did not write your tests first and your mark will be reduced.
* You should have black-box tests for all tests required (i.e. testing each function/endpoint). However, you are also welcome to write whitebox unit tests in this iteration if you see that as important.
* Merging in merge requests with failing pipelines is **very bad practice**. Not only does this interfere with your teams ability to work on different features at the same time, and thus slow down development, it is something you will be penalised for in marking.
* Similarly, merging in branches with untested features is also **very bad practice**. We will assume, and you should too, that any code without tests does not work.
* Pushing directly to `master` is not possible for this repo. The only way to get code into master is via a merge request. If you discover you have a bug in `master` that got through testing, create a bugfix branch and merge that in via a merge request.

### 4.3. Recommended approach

Our recommendation with this iteration is that you:

1. Start out trying to implement the new functions the same way you did in iteration 1 (a series of implemented functions, categorised in files, with black-box pytests testing them).
2. Write another layer of HTTP tests that test the inputs/outputs on routes according to the specific, and while writing tests for each component/feature, write the Flask route/endpoint for that feature too.

This approach means that you can essentially finish the project/testing logic without worrying about HTTP, and then simply wrap the HTTP/Flask layer on top of it at the end.

### 4.4. Storing data

You are not required to store data persistently in this iteration. However, basic persistence will be covered in lectures and you are welcome to implement this if you find it convenient.

### 4.5. Submission

This iteration is due to be submitted at 8pm Monday 26th October (**week 7**). You will then be demonstrating this in your week 7 lab. All team members **must** attend this lab session, or they will not receive a mark.

At the due date provided, we will automatically collect and submit the code that is on the `master` branch of your repository. If the deadline is approaching and you have features that are either untested or failing their tests, **DO NOT MERGE IN THOSE MERGE REQUESTS**. Your tutor will look at unmerged branches and may allocate some reduced marks for incomplete functionality, but `master` should only contain working code.

### 4.6. Marking Criteria

|Section|Weighting|Criteria|
|---|---|---|
|Testing|30%|<ul><li>Distinct use of unit tests for any helper functions you write, integration tests on the functions used in iteration 1, and integration/system tests on the HTTP endpoints</li><li>Tests provide excellent test **coverage** with the coverage tool</li><li>Demonstrated an understanding of the importance of **clarity** on the communication of test purposes</li><li>Demonstrated an understanding of thoughtful test **design**</li><li>Performance against an automatic marking syste<m/li><li>Compliance with standard pylint requirements</li></ul>|
|Implementation|40%|<ul><li>Correctly implemented entire backend server interface that satisfies requirements</li><li>Pythonic programming approach (where possible)</li><li>Thought out code design</li><li>Compliance with standard pylint requirements</li></ul>|
|Git practices & Project Management|20%|<ul><li>Meaningful and informative git commit names being used</li><li>Effective use of merge requests (from branches being made) across the team</li><li>Effective use of course-provided flockr, demonstrating an ability to communicate and manage effectivelly digitally</li><li>Use of task board on Gitlab to track and manage tasks</li><li>Effective use of agile methods such as standups</li></ul>|
|Teamwork|10%|<ul><li>A generally equal contribution between team members</li><li>Clear evidence of reflection on group's performance and state of the team, with initiative to improve in future iterations</li></ul>|

For this and for all future milestones, you should consider the other expectations as outlined in section 8 below.

### 4.7. Demonstration

When you demonstrate this iteration in your week 7 lab, it will consist of a 15 minute Q&A in front of your tutorial class via zoom. Webcams are required to be on during this Q&A (your phone is a good alternative if your laptop/desktop doesn't have a webcam).

## 5. Iteration 3

Not yet released

## 6. Interface specifications

These interface specifications come from Sally and Bob, who are building the frontend to the requirements set out below.

### 6.1. Data types

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

### 6.2. Interface

|Function Name|HTTP Method|Parameters|Return type|Exceptions|Description|
|------------|-------------|----------|-----------|----------|----------|
|auth/login|POST|(email, password)|{ u_id, token }|**InputError** when any of:<ul><li>Email entered is not a valid email using the method provided [here](https://www.geeksforgeeks.org/check-if-email-address-valid-or-not-in-python/) (unless you feel you have a better method)</li><li>Email entered does not belong to a user</li><li>Password is not correct</li></ul> | Given a registered users' email and password and generates a valid token for the user to remain authenticated |
|auth/logout|POST|(token)|{ is_success }|N/A|Given an active token, invalidates the token to log the user out. If a valid token is given, and the user is successfully logged out, it returns true, otherwise false. |
|auth/register|POST|(email, password, name_first, name_last)|{ u_id, token }|**InputError** when any of:<ul><li>Email entered is not a valid email using the method provided [here](https://www.geeksforgeeks.org/check-if-email-address-valid-or-not-in-python/) (unless you feel you have a better method).</li><li>Email address is already being used by another user</li><li>Password entered is less than 6 characters long</li><li>name_first not is between 1 and 50 characters inclusively in length</li><li>name_last is not between 1 and 50 characters inclusively in length</ul>|Given a user's first and last name, email address, and password, create a new account for them and return a new token for authentication in their session. A handle is generated that is the concatentation of a lowercase-only first name and last name. If the concatenation is longer than 20 characters, it is cutoff at 20 characters. If the handle is already taken, you may modify the handle in any way you see fit (maintaining the 20 character limit) to make it unique. |
|channel/invite|POST|(token, channel_id, u_id)|{}|**InputError** when any of:<ul><li>channel_id does not refer to a valid channel.</li><li>u_id does not refer to a valid user</li></ul>**AccessError** when<ul><li>the authorised user is not already a member of the channel</li>|Invites a user (with user id u_id) to join a channel with ID channel_id. Once invited the user is added to the channel immediately|
|channel/details|GET|(token, channel_id)|{ name, owner_members, all_members }|**InputError** when any of:<ul><li>Channel ID is not a valid channel</li></ul>**AccessError** when<ul><li>Authorised user is not a member of channel with channel_id</li></ul>|Given a Channel with ID channel_id that the authorised user is part of, provide basic details about the channel|
|channel/messages|GET|(token, channel_id, start)|{ messages, start, end }|**InputError** when any of:<ul><li>Channel ID is not a valid channel</li><li>start is greater than the total number of messages in the channel</li></ul>**AccessError** when<ul><li>Authorised user is not a member of channel with channel_id</li></ul>|Given a Channel with ID channel_id that the authorised user is part of, return up to 50 messages between index "start" and "start + 50". Message with index 0 is the most recent message in the channel. This function returns a new index "end" which is the value of "start + 50", or, if this function has returned the least recent messages in the channel, returns -1 in "end" to indicate there are no more messages to load after this return.|
|channel/leave|POST|(token, channel_id)|{}|**InputError** when any of:<ul><li>Channel ID is not a valid channel</li></ul>**AccessError** when<ul><li>Authorised user is not a member of channel with channel_id</li></ul>|Given a channel ID, the user removed as a member of this channel|
|channel/join|POST|(token, channel_id)|{}|**InputError** when any of:<ul><li>Channel ID is not a valid channel</li></ul>**AccessError** when<ul><li>channel_id refers to a channel that is private (when the authorised user is not a global owner)</li></ul>|Given a channel_id of a channel that the authorised user can join, adds them to that channel|
|channel/addowner|POST|(token, channel_id, u_id)|{}|**InputError** when any of:<ul><li>Channel ID is not a valid channel</li><li>When user with user id u_id is already an owner of the channel</li></ul>**AccessError** when the authorised user is not an owner of the flockr, or an owner of this channel</li></ul>|Make user with user id u_id an owner of this channel|
|channel/removeowner|POST|(token, channel_id, u_id)|{}|**InputError** when any of:<ul><li>Channel ID is not a valid channel</li><li>When user with user id u_id is not an owner of the channel</li></ul>**AccessError** when the authorised user is not an owner of the flockr, or an owner of this channel</li></ul>|Remove user with user id u_id an owner of this channel|
|channels/list|GET|(token)|{ channels }|N/A|Provide a list of all channels (and their associated details) that the authorised user is part of|
|channels/listall|GET|(token)|{ channels }|N/A|Provide a list of all channels (and their associated details)|
|channels/create|POST|(token, name, is_public)|{ channel_id }|**InputError** when any of:<ul><li>Name is more than 20 characters long</li></ul>|Creates a new channel with that name that is either a public or private channel|
|message/send|POST|(token, channel_id, message)|{ message_id }|**InputError** when any of:<ul><li>Message is more than 1000 characters</li></ul>**AccessError** when: <li> the authorised user has not joined the channel they are trying to post to</li></ul>|Send a message from authorised_user to the channel specified by channel_id|
|message/remove|DELETE|(token, message_id)|{}|**InputError** when any of:<ul><li>Message (based on ID) no longer exists</li></ul>**AccessError** when none of the following are true:<ul><li>Message with message_id was sent by the authorised user making this request</li><li>The authorised user is an owner of this channel or the flockr</li></ul>|Given a message_id for a message, this message is removed from the channel|
|message/edit|PUT|(token, message_id, message)|{}|**AccessError** when none of the following are true:<ul><li>Message with message_id was sent by the authorised user making this request</li><li>The authorised user is an owner of this channel or the flockr</li></ul>|Given a message, update it's text with new text. If the new message is an empty string, the message is deleted.|
|user/profile|GET|(token, u_id)|{ user }|**InputError** when any of:<ul><li>User with u_id is not a valid user</li></ul>|For a valid user, returns information about their user_id, email, first name, last name, and handle|
|user/profile/setname|PUT|(token, name_first, name_last)|{}|**InputError** when any of:<ul><li>name_first is not between 1 and 50 characters inclusively in length</li><li>name_last is not between 1 and 50 characters inclusively in length</ul></ul>|Update the authorised user's first and last name|
|user/profile/setemail|PUT|(token, email)|{}|**InputError** when any of:<ul><li>Email entered is not a valid email using the method provided [here](https://www.geeksforgeeks.org/check-if-email-address-valid-or-not-in-python/) (unless you feel you have a better method).</li><li>Email address is already being used by another user</li>|Update the authorised user's email address|
|user/profile/sethandle|PUT|(token, handle_str)|{}|**InputError** when any of:<ul><li>handle_str must be between 3 and 20 characters</li><li>handle is already used by another user</li></ul>|Update the authorised user's handle (i.e. display name)|
|users/all|GET|(token)|{ users}|N/A|Returns a list of all users and their associated details|
|admin/userpermission/change|POST|(token, u_id, permission_id)|{}|**InputError** when any of:<ul><li>u_id does not refer to a valid user<li>permission_id does not refer to a value permission</li></ul>**AccessError** when<ul><li>The authorised user is not an owner</li></ul>|Given a User by their user ID, set their permissions to new permissions described by permission_id|Given a User by their user ID, set their permissions to new permissions described by permission_id|
|search|GET|(token, query_str)|{ messages }|N/A|Given a query string, return a collection of messages in all of the channels that the user has joined that match the query|
|clear|DELETE|()|{}|N/A|Resets the internal data of the application to it's initial state|

### 6.3. Errors for all functions

Either an `InputError` or `AccessError` is thrown when something goes wrong. All of these cases are listed in the **Interface** table.

One exception is that, even though it's not listed in the table, for all functions except `auth/register` and `auth/login`, an `AccessError` is thrown when the token passed in is not a valid token.

### 6.4. Token

Many of these functions (nearly all of them) need to be called from the perspective of a user who is logged in already. When calling these "authorised" functions, we need to know:
1) Which user is calling it
2) That the person who claims they are that user, is actually that user

We could solve this trivially by storing the user ID of the logged in user on the front end, and every time the front end (from Sally and Bob) calls your background, they just sent a user ID. This solves our first problem (1), but doesn't solve our second problem! Because someone could just "hack" the front end and change their user id and then log themselves in as someone else.

To solve this when a user logs in or registers the backend should return a "token" (an authorisation hash) that the front end will store and pass into most of your functions in future. When these "authorised" functions are called, those tokens returned from register/login will be passed into those functions, and from there you can check if a token is valid, and determine the user ID.

Passwords must be stored in an encrypted form, and tokens must use JWTs (or similar).

### 6.5. Pagination
The behaviour in which channel_messages returns data is called **pagination**. It's a commonly used method when it comes to getting theoretially unbounded amounts of data from a server to display on a page in chunks. Most of the timelines you know and love - Facebook, Instagram, LinkedIn - do this.

For example, if we imagine a user with token "12345" is trying to read messages from channel with ID 6, and this channel has 124 messages in it, 3 calls from the client to the server would be made. These calls, and their corresponding return values would be:
 * channel_messages("12345", 6, 0) => { [messages], 0, 50 }
 * channel_messages("12345", 6, 50) => { [messages], 50, 100 }
 * channel_messages("12345", 6, 100) => { [messages], 100, -1 }

### 6.6. Permissions:
 * Members in a channel have one of two channel permissions.
   1) Owner of the channel (the person who created it, and whoever else that creator adds)
   2) Members of the channel
 * Flockr users have two global permissions
   1) Owners (permission id 1), who can also modify other owners' permissions.
   2) Members (permission id 2), who do not have any special permissions
* All flockr users are members by default, except for the very first user who signs up, who is an owner

A user's primary permissions are their global permissions. Then the channel permissions are layered on top. For example:
* An owner of flockr has owner permissions in every channel they've joined
* A member of flockr is a member in channels they are not owners of
* A member of flockr is an owner in channels they are owners of

### 6.7. Working with the frontend

There is a SINGLE repository available for all students at https://gitlab.cse.unsw.edu.au/COMP1531/20T3/project-frontend. You can clone this frontend locally. The course notice said you will receive your own copy of this, however, that isn't necessary anymore since most groups will not modify the frontend repo. If you'd like to modify the frontend repo (i.e. teach yourself some frontend), please FORK the repository.

If you run the frontend at the same time as your flask server is running on the backend, then you can power the frontend via your backend.

#### 6.7.1.

A working example of the frontend can be used at http://flockr-unsw.herokuapp.com/

The data is reset daily, but you can use this link to play around and get a feel for how the application should behave.

#### 6.7.2. Error raising for the frontend

For errors to be appropriately raised on the frontend, they must be raised by the following:

```python
if True: # condition here
    raise InputError(description='Description of problem')
```

The descriptions will not be assessed, they are just there for the frontend to help users.

The types in error.py have been modified appropriately for you.

### 6.8. Other Points

* Each message should have it's own unique ID. I.E. No messages should share an ID with another message, even if that other message is in a different channel.

## 7. Due Dates and Weightings

|Iteration|Code and report due                  |Demonstration to tutor(s)      |Assessment weighting of project (%)|
|---------|-------------------------------------|-------------------------------|-----------------------------------|
|   1     |8pm Sunday 4th October (**week 3**)   |In YOUR **week 4** laboratory  |30%                                |
|   2     |8pm Monday 26th October (**week 7**)   |In YOUR **week 7** laboratory  |40%                                |
|   3     |8pm Sunday 15th November (**week 9**)   |In YOUR **week 10** laboratory |30%                                |

There is no late penalty, as we do not accept late submissions.

## 8. Other Expectations

While it is up to you as a team to decide how work is distributed between you, for the purpose of assessment there are certain key criteria all members must.

* Code contribution
* Documentation contribution
* Usage of git/GitLab
* Attendance
* Peer assessment
* Academic conduct

The details of each of these is below.

While, in general, all team members will receive the same mark (a sum of the marks for each iteration), **if you as an individual fail to meet these criteria your final project mark may be scaled down**, most likely quite significantly.

### 8.1. Progress check-in

During your lab class, in weeks without demonstrations (see below), you and your team will conduct a short stand-up in the presence of your tutor. Each member of the team will briefly state what they have done in the past week, what they intend to do over the next week, and what issues they faced or are currently facing. This is so your tutor, who is acting as a representative of the client, is kept informed of your progress. They will make note of your presence and may ask you to elaborate on the work you've done.

### 8.2. Code contribution

All team members must contribute code to the project. Tutors will assess the degree to which you have contributed by looking at your **git history** and analysing lines of code, number of commits, timing of commits, etc. If you contribute significantly less code than your team members, your work will be closely examined to determine what scaling needs to be applied.

### 8.3. Documentation contribution

All team members must contribute documentation to the project. Tutors will assess the degree to which you have contributed by looking at your **git history** but also **asking questions** (essentially interviewing you) during your demonstration.

Note that, **contributing more documentation is not a substitute for not contributing code**.

### 8.4. Peer Assessment

You will be required to complete a form in week 10 where you rate each team member's contribution to the project and leave any comments you have about them. Information on how you can access this form will be released closer to Week 10. Your other team members will **not** be able to see how you rated them or what comments you left.

If your team members give you a less than satisfactory rating, your contribution will be scrutinised and you may find your final mark scaled down.

### 8.5. Attendance

It is generally assumed that all team members will be present at the demonstrations and at weekly check-ins. If you're absent for more than 80% of the weekly check-ins or any of the demonstrations, your mark may be scaled down.

If, due to exceptional circumstances, you are unable to attend your lab for a demonstration, inform your tutor as soon as you can so they can record your absence as planned.

## 9. Plagiarism

The work you and your group submit must be your own work. Submission of work partially or completely derived from any other person or jointly written with any other person is not permitted. The penalties for such an offence may include negative marks, automatic failure of the course and possibly other academic discipline. Assignment submissions will be examined both automatically and manually for such submissions.

Relevant scholarship authorities will be informed if students holding scholarships are involved in an incident of plagiarism or other misconduct.

Do not provide or show your project work to any other person, except for your group and the teaching staff of COMP1531. If you knowingly provide or show your assignment work to another person for any reason, and work derived from it is submitted you may be penalized, even if the work was submitted without your knowledge or consent. This may apply even if your work is submitted by a third party unknown to you.

Note, you will not be penalized if your work has the potential to be taken without your consent or knowledge.
