import data
import random
from error import InputError

def channels_list(token):
    #get the u_id of the authorised user
    
    user_id = 
    
            
    #make a loop to check each channels       
    i = 0
    channel_list = []
    for i in range(len(data.channels)):
        j = 0
        #check if the user in this channel
        for j in range(len(data.channels[i]['all_members'])):
            if data.channels[i]['all_members'][j]['u_id'] == user_id:        
                channel_list.append(data.channels[i])
        
    return channel_list
def channels_listall(token):

    #just return all channels? sure about that?
    return data.channels
    
def create_channel_id(channels):
    # create a random 32 bit unsigned integer
    channel_id = random.randint(0, 0xFFFFFFFF)

    # a recursive function to check whether the channel_id is unique
    for channel in channels:
        if channel['channel_id'] == channel_id:
            channel_id = create_channel_id(channel_id, channels)
            break
    
    return channel_id
    
def channels_create(token, name, is_public):

    if len(name) > 20:
        raise InputError
    return
     
    owner_id = 
    owner_FN = 
    owner_LN = 
        
    channel_id = create_channel_id(data.channels)
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
    data.append_channels(channel_new)
    
    return channel_id
    

