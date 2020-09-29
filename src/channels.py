#import data
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
     
    owner_id = 
    owner_FN =
    owner_LN = 
        
    channel_id = len(channels) + 1
    channel_new = {}
    channel_new['channel_id'] = channel_id
    channel_new['name'] = name
    channel_new['public'] = is_public
    channel_new['owner']['u_id'] = owner_id
    channel_new['owner']['FirstN'] = owner_FN
    channel_new['owner']['LastN'] = owner_LN
    channel_new['all_members']['u_id'] = owner_id
    channel_new['all_members']['FirstN'] = owner_FN
    channel_new['all_members']['LastN'] = owner_LN
    channels.append(channel_new)
    
    return channel_id
    

