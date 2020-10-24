import pickle

with open('src/data/JWT_SECRET.p', 'rb') as file:
    token_secret = pickle.load(file)
    print(token_secret)

