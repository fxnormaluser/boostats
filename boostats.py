from steem import Steem
from steem.post import Post
from steem.instance import set_shared_steemd_instance
from steem.steemd import Steemd
from steem.amount import Amount
from steem.blockchain import Blockchain

#steemd_nodes = ['https://api.steemit.com']
steemd_nodes = ['https://rpc.buildteam.io'] #worked best
set_shared_steemd_instance(Steemd(nodes=steemd_nodes))
steem = Steem(nodes=steemd_nodes)

blockchain = Blockchain()

timeframe = 24 * 60 * 60

last_block = blockchain.get_current_block_num()
print('Current Block:', str(last_block), )
trail_24h_block = int(last_block - ( timeframe / 3 ))
print('24-hours-ago block:', str(trail_24h_block), )

boosters = ['votebuster', 'smartsteem', 'mrswhale', 'adriatik', 'ipromote', 'voterunner', 'buildawhale', 'postpromoter', 'boomerang', 'mercurybot', 'upme', 'appreciator', 'moneymatchgaming', 'msp-bidbot', 'upmewhale', 'jerrybanfield', 'bid4joy', 'seakraken', 'aksdwi', 'smartsteem', 'sneaky-ninja', 'minnowhelper', 'upgoater', 'pushup', 'allaz', 'upmyvote', 'steembloggers', 'sleeplesswhale', 'lays', 'ebargains', 'bumper', 'upvotewhale', 'treeplanter' 'morewhale', 'minnowpond', 'drotto', 'moonbot', 'blockgators', 'tipu', 'steemvote', 'originalworks', 'withsmn', 'echowhale', 'siditech', 'steemvoter',  ] 

total_posts = 0
boosties = 0
total_claims = Amount('0.000 SBD')
total_booster_share = Amount('0.000 SBD')

for author_reward in blockchain.history(start_block = trail_24h_block, end_block = last_block, filter_by = 'author_reward'):

    author = author_reward['author']
    permlink = author_reward['permlink']
    sbd_payout = author_reward['sbd_payout']
    steem_payout = author_reward['steem_payout']    
    vesting_payout = author_reward['vesting_payout']
    identifier = (author + '/' + permlink)

    if not 're-' in permlink:
        
        post = Post(identifier)
        
        if post.is_main_post():

            print('Post:', identifier, 'Payout:', str(sbd_payout), str(steem_payout), str(vesting_payout), )
            print('Reward:', str(post.get("total_payout_value")))
            total_claims = Amount(total_claims) + Amount(post.get("total_payout_value"))
            print('Total Claims:', str(total_claims), )

            total_posts = total_posts + 1

            total_r_shares = 0
            booster_r_shares = 0

            for active_vote in post.get("active_votes", []):

                total_r_shares = total_r_shares + int(active_vote['rshares'])
            
                if active_vote['voter'] in boosters:

                    print('Boostie :)', )
                    boosties = boosties + 1      #this needs to be fixed ...
                    booster_r_shares = booster_r_shares + int(active_vote['rshares'])

            booster_ratio = (booster_r_shares / total_r_shares)
            booster_share = Amount(post.get("total_payout_value")) * booster_ratio
            total_booster_share = Amount(total_booster_share) + Amount(booster_share)

print('\n################\n')
print('Posts:', str(total_posts), )
print('Boosties:', str(boosties), )
print('Total Rewards:', str(total_claims), )
print('Rewards from Boosters:', str(total_booster_share), )
print('\n################\n')   
