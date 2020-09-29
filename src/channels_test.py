from channels import *

def test_channels_list():
    user = [
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
  
    
    assert channels_list('12345') == [{'name': 'Team4R', 'channel_id': '1', 'is_public': True, 'owner_members': [{'u_id': 1, 'name_first': 'Liuyuzi', 'name_last': 'He'}], 'all_members': [{'u_id': 1, 'name_first': 'liuyuzi', 'name_last': 'He'}]}]
'''    
def test_channels_listall():
    
    token = '12345'
    channels = channels_listall(token)
    assert channels == [{'name': 'Team4R', 'channel_id': '1', 'is_public': True, 'owner_members': [{'u_id': 1, 'name_first': 'Liuyuzi', 'name_last': 'He'}], 'all_members': [{'u_id': 1, 'name_first': 'liuyuzi', 'name_last': 'He'}]},{'name': 'Team4W', 'channel_id': '2', 'is_public': True, 'owner_members': [{'u_id': 2, 'name_first': 'Steve', 'name_last': 'Tan'}], 'all_members': [{'u_id': 2, 'name_first': 'Steve', 'name_last': 'Tan'}]}]
    
def channels_create():
    token = '12345'
    name = 'name'
    is_public = True
    channel_id = channels_create(token, name, is_public)
    assert channel_id == 1
'''
