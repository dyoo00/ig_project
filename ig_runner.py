import os

# define where you want to keep these scripts and run from
os.chdir(r"")

from ig_fetch_function import *

# define a filepath where you want to save the output
input_filePath = ""


# create list of hashtags we're interested in
input_hashtags = ['kyliejenner','monday']

# pipe list into getHashTagEdge function
# see notes in the function for validation of assumptions
hashtagList = list(map(getHashtagEdge,input_hashtags))

# concatenate the list of dataframes into 1
hashtagDF = pd.concat(hashtagList).drop_duplicates(['id'], inplace = True)

# pipe user ids from the hashtagDF object into the getUserInfo function
# see notes in the function for validation of logic/assumptions
hashtagDF[['user_id','inputuser','followers','following']] = hashtagDF.owner.astype('str').apply(getUserInfo)

# will pass only on the first run of the script
try:
    inputFile = pd.read_pickle(input_filePath)
    outputFile = pd.concat([inpuFile, hashtagDF])
except:
    outputFile = hashtagDF
    del hashtagDF

# in case we pull duplicate posts, take the most recent version of the post--sort by likes in decreasing order 
outputFile=outputFile.sort_values(['taken_at_timestamp','edge_liked_by'],ascending = False).drop_duplicates('id')

outputFile.to_pickle(input_filepath)




