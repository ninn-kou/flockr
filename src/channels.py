#import data
'''
user= [
    { 
        'u_id':1 ,
        'name_first':'Liuyuzi',
        'name_last':'He',
        'token':'12345'
    }, {
        'u_id':2 ,
        'name_first':'Steve',
        'name_last':'Tan',
        'token':'67890'
    }
]
channels= [
    {
        'name':'Team4R',
        'channel_id':'1',
        'is_public' : True,
        'owner_members':[
            {
                'u_id': 1,
                'name_first': 'Liuyuzi',
                'name_last': 'He',
            }
        ],
        'all_members':[
            {
                'u_id': 1,
                'name_first': 'liuyuzi',
                'name_last': 'He',
            }
        ]
        
    }, {
        'name':'Team4W',
        'channel_id':'2',
        'is_public' :True,
        'owner_members':[
            {
                'u_id': 2,
                'name_first': 'Steve',
                'name_last': 'Tan',
            }
        ],
        'all_members':[
            {
                'u_id': 2,
                'name_first': 'Steve',
                'name_last': 'Tan',
            }
        ]
    }
]
'''    
def channels_list(token):
    #get the u_id of the authorised user
    global user
    global channels
    i = 0
    user_id = 0
    for i in range(len(user)):
        if user[i]['token'] == token:
            user_id = user[i]['u_id']
            break
            
    #make a loop to check each channels       
    i = 0
    channel_list = []
    for i in range(len(channels)):
        j = 0
        #check if the user in this channel
        for j in range(len(channels[i]['all_members'])):
            if channels[i]['all_members'][j]['u_id'] == user_id:        
                channel_list.append(channels[i])
        
    return channel_list
def channels_listall(token):

    #just return all channels? sure about that?
    return channels
def channels_create(token, name, is_public):

    if len(name) > 20:
        print("name is too lone")
        exit(1)
        
    channel_id = len(channels) + 1
    channel_new = {}
    channel_new['channel_id'] = channel_id
    channel_new['name'] = name
    channel_new['is_public'] = is_public
    channels.append(channel_new)
    return channel_id
    

