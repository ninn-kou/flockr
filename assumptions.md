# Assumption File

This assumption file contains our group's work when we are doing the main Project in COMP1531.

For every member of our team, please use the below TOC to jump to the chapter you want.

[TOC]

## 0. Change Log

Most recent changing log for this Markdown document here:

> 01 October, Hao Ren: Re-formatted this Markdown file.
>
> 31 September, Xingyu Tan: Created the assumption file.

## 1. Iteration 1

### 1.1 About this Assumption

- It is assumed that **tokens** are produced randomly with possible numbers and characters. Each token is a string with 20 chars.
- Some ASCII characters like `a-z`, `A-Z`, `0-9`, and `!@#$%^&*()-_=+,./?` are allowed to use.
- The **User ID** should generated uniquely and randomly between `0` and `4,294,967,295 (0xFFFFFFFF)`.
- The **channel ID** should generated uniquely and randomly `0` and `4,294,967,295 (0xFFFFFFFF)`.

- It is assumed that the `user struct` is like this:

 ```py
 user = {
    'u_id': u_id,
    'email': email,
    'name_first': name_first,
    'name_last': name_last,
    'handle_str': handle
    'token': token
    'password': password
 }
 ```

- It is assumed that the `token struct` is like this:

 ```py
 token_object = {
    'u_id': u_id,
    'token': token
 }
 ```

### 1.2 Channel

- The user who creates the channel would be the owner automatically.
- It is assumed that the `channel struct` is like this:

 ```py
 channel = {
    'name': 'Hayden',
    'channel_id':' '
    'owner': [
        {
            'u_id': 1,
            'name_first': 'Hayden',
            'name_last': 'Jacobs',
        }
    ],
    'all_members': [
        {
            'u_id': 1,
            'name_first': 'Hayden',
            'name_last': 'Jacobs',
        }
    ],
    'is public': True,
    'messages':[]
 }
 ```
