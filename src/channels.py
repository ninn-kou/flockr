'''
data = {
    'user': [
        { 
            'u_id': ,
            'name_first':'',
            'name_last':'',
            'token':'',
        },
        ...
    ]
    'channels': [
        {
            'name':'',
            'channel_id':'',
            'is public' = ,
            'owner_members':[
                {
                    'u_id': ,
                    'name_first': '',
                    'name_last': '',
                },
                ...
            ]
            'all_members':[
                {
                    'u_id': ,
                    'name_first': '',
                    'name_last': '',
                },
                ...
            ]
            'messages':[
                {
                    'message_id': ,
                    'u_id': ,
                    'message': '',
                    'time_created': ,
                },
                ...
            ]
        },
        ...   
    ]
}
'''
def channels_list(token):
'''
    return {
        'channels': [
        	{
        		'channel_id': 1,
        		'name': 'My Channel',
        	}
        ],
    }
'''
    #get the u_id of the authorised user
    i = 0
    user_id = 0
    for i in range(len(data['user']):
        if data['user'][i]['token'] == token:
            user_id = data['user'][i]['u_id']
            break
    #make a loop to check each channels       
    i = 0
    channel_list = []
    for i in range(len(data['channels'][i]):
        j = 0
        #check if the user in this channel
        for j in range(len(data['channels'][i]['all_members']:
            if data['channels'][i]['all_members'][j]['u_id'] == user_id:        
                channel_list.append(data['channel'][i])
        
    return channel_list
def channels_listall(token):
'''
    return {
        'channels': [
        	{
        		'channel_id': 1,
        		'name': 'My Channel',
        	}
        ],
    }
'''
    #just return all channels? sure about that?
    return data['channels']
def channels_create(token, name, is_public):
'''
    return {
        'channel_id': 1,
    }
'''
    if len(name) > 20:
        print("name is too lone")
        exit(1)
        
    channel_id = len(data['channels']) + 1
    channel_new['channel_id'] = channel_id
    channel_new['name'] = name
    channel_new['is_public'] = is_public
    data['channels'].append(channel_new)
    return channel_id
