import data
import random
from error import InputError
import auth
from other import clear

def channels_list(token):
    #get the u_id of the authorised user
    for i in data.users:
        if i['token'] == token:
            user_id = i['u_id']
            break   
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
            channel_id = create_channel_id(channels)
            break
    
    return channel_id

def channels_create(token, name, is_public):    
    #initialise the channels list
    data.init_channels()
    
    if len(name) > 20:
        raise InputError
        return
    #find the detail of the user by token
    for i in data.users:
        if i['token'] == token:
            owner_id = i['u_id']
            owner_FN = i['name_first']
            owner_LN = i['name_last']
            break    
    #make a random channel id
    channel_id = create_channel_id(data.channels)
    channel_new = {
        'name': name,
        'channel_id':channel_id,
        'owner': [
            {
                'u_id': owner_id,
                'name_first': owner_FN,
                'name_last': owner_LN,
            }
        ],
        'all_members': [
            {
                'u_id': owner_id,
                'name_first': owner_FN,
                'name_last': owner_LN,
            }
        ],   
        'is_public': is_public,
    }
    #add it to the data
    data.append_channels(channel_new)
    

    return channel_id
