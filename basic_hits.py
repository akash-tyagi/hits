'''
Created on 14-Jan-2015

@author: akash
'''
import json
import copy
import twitter_crawler
from collections import defaultdict

class Basic_Hits():
    '''
        Class to find the hubs and authorities
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
    
    def get_hits(self):
        '''
            calculate hubs and authority scores
        ''' 
        new_score_list = defaultdict(dict)
        
        for i in range(6):
            for user_id, data_dict in self.user_list.iteritems():
                new_score_list[user_id] = {'auth':0,'hub':0}
                #Calculate the auth score
                for in_user_id in data_dict['in']:
                    new_score_list[user_id]['auth'] += self.user_score_list[in_user_id]['hub']
                new_score_list[user_id]['auth'] /= 100
                
                #Calculate the hub score
                for out_user_id in  data_dict['out']:
                    new_score_list[user_id]['hub'] += self.user_score_list[out_user_id]['auth']
                new_score_list[user_id]['hub'] /= 100
                
            self.user_score_list = copy.deepcopy(new_score_list)
            
        top_hubs = sorted(self.user_score_list.iteritems(), key= lambda x: x[1]['hub'], reverse = True)[:10]
        top_auth = sorted(self.user_score_list.iteritems(), key= lambda x: x[1]['auth'], reverse = True)[:10]
        
        print "Top Hubs Are:"
        for user in top_hubs:
            print user
        print "Top Auth Are:"
        for user in top_auth:
            print user

        print 'Hits Calculation Done'
        return

def main():
    hits = Basic_Hits()
    hits.parse_json()
    hits.get_hits()

if __name__ == "__main__":
    main()