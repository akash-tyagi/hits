'''
Created on 14-Jan-2015

@author: akash
'''
from collections import defaultdict
import copy
import json


class Basic_Hits():
    '''
        Class to find the hubs and authorities in a given list
    '''
    def __init__(self):
        self.user_list = {}
        self.user_score_list = {}
        return
    
    def parse_json(self):
        '''
            Parse the sports_list.json and generate a user list
            with all the necessary data
        '''
        for line in open('sports_list.json'):
            user_data = json.loads(line)
            self.user_list[user_data[0]] = user_data[1]
            
            self.user_score_list[user_data[0]] = {}
            self.user_score_list[user_data[0]]['auth'] = 1.0
            self.user_score_list[user_data[0]]['hub'] = 1.0
        print "Parsing Done"

    def update_auth_hub_score(self):
        new_score_list = defaultdict(dict)
        for user_id, data_dict in self.user_list.iteritems():
            new_score_list[user_id] = {'auth':0.0,'hub':0.0}
            #Calculate the auth score
            for in_user_id in data_dict['in']:
                new_score_list[user_id]['auth'] += self.user_score_list[in_user_id]['hub']
            new_score_list[user_id]['auth'] /= 50
            
            #Calculate the hub score
            for out_user_id in  data_dict['out']:
                new_score_list[user_id]['hub'] += self.user_score_list[out_user_id]['auth']
            new_score_list[user_id]['hub'] /= 50
                
        self.user_score_list = copy.deepcopy(new_score_list)
            
    def get_hits(self):
        '''
            calculate hubs and authority scores
        ''' 
        for i in range(6):
            self.update_auth_hub_score()
            
        top_hubs = self.get_top_n_hubs()
        top_auth = self.get_top_n_auths()
        print "Top Hubs Are:"
        for user in top_hubs:
            print user
        print "Top Auth Are:"
        for user in top_auth:
            print user

        print 'Hits Calculation Done'
        return
    
    def get_top_n_hubs(self, n = 10):
        return sorted(self.user_score_list.iteritems(), key= lambda x: x[1]['hub'], reverse = True)[:n]

    def get_top_n_auths(self, n =10):
        return sorted(self.user_score_list.iteritems(), key= lambda x: x[1]['auth'], reverse = True)[:n]

    def generate_spammy_hub(self, id):
        top10_auth = self.get_top_n_auths(10)
        spam_user_data = {"in":[], "out":[], "auth":1.0, "hub":1.0}
        self.user_list[id] = spam_user_data  
              
        for auth in top10_auth:
            self.user_list[id]["out"].append(auth[0])
        self.update_auth_hub_score()
        
#         print "Spam Hub Score:"
#         print self.user_score_list[id]
        
#         rank = 0
#         for user in sorted(self.user_score_list.iteritems(), key= lambda x: x[1]['hub'], reverse = True):
#             rank += 1
#             if user[0] == id:
#                 print "SpamHub Rank is:"+str(rank)
#                 break
    
    def generate_spammy_auth(self, id):
        spam_user_data = {"in":[], "out":[], "auth":1.0, "hub":1.0}
        self.user_list[id] = spam_user_data 
        
        for i in range(10):
            self.generate_spammy_hub(i)
            self.user_list[id]["in"].append(i)
        
        self.update_auth_hub_score()
        print "Spam Auth Score"
        print self.user_score_list[id]
        rank = 0
        for user in sorted(self.user_score_list.iteritems(), key= lambda x: x[1]['auth'], reverse = True):
            rank += 1
            if user[0] == id:
                print "SpamAuth Rank is:"+str(rank)
                break

def main():
    hits = Basic_Hits()
    hits.parse_json()
    hits.get_hits()
#     hits.generate_spammy_hub(1)
    hits.generate_spammy_auth(1)

if __name__ == "__main__":
    main()