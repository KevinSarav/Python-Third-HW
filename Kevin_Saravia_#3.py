""" Kevin Saravia, PeopleSoft ID: 1478627
    Program #3: Detecting Trends and Foul Language in Twitter
    COSC 1306, Fall 2017
    This program will write all tweets containing foul language and rank the most popular trends."""

punctDict = {}                                                                      #will be a dictionary with all your punctuations
punctList = [".", ";", ":", "!", "?", "/", ",", "@", "$", "&", ")",                 #a list of all possible punctuation marks
             "(", "\"", "\'", "\\", "[", "]", ">", "<", "#","-", "_",
             "*", "=", "+", "%", "^", "~", "`", "{", "}"]

for punct in punctList:                                                             #basically adds every punctuation mark in your list to your dictionary
    punctDict[punct] = 0

def findSwearWords(punctuationDict):
    tweet = open('twitter_data.txt', encoding="utf8")                               #opens your files to write
    swear = open('swear_words.txt', encoding = "utf8")
    offensive = open('potentially_offensive_tweets.txt', 'w')                       #opens file to write
    swearDict = {}                                                                  #will be a dictionary of swear words
    duplicateTweets = {}                                                            #will be a dictionary to prevent writing the same recurring tweet twice
    newWord = ""                                                                    #will be a substring without punctuation
    value = 0                                                                       #will determine if at least one swear word is in a tweet
    counter = 0

    for swearing in swear:                                                          #splits swear file into swear words
        swearing = swearing.rstrip()                                                #gets rid of \n at the end of every swear word
        swearDict[swearing] = 0                                                     #adds swear words to swear dictionary

    for line in tweet:                                                              #splits tweet file into lines (tweets)
        wordList = line.split()                                                     #splits tweet into a list of words
        for word in wordList:                                                       #splits list of words into individual words
            word = word.lower()                                                     #makes everything in word lower case so can compare capital to lower case
            for indec in word:                                                      #splits word into each character
                if indec not in punctuationDict:                                    #if character is not in dictionary of punctuation, then:
                    newWord += indec                                                #add character to substring
                else:                                                               #else if character is in punctuation dictionary:
                    for ind in range(len(newWord)):                                 #gets every index in newWord (your substring without punctuation)
                        if (newWord[ind : ind + 4] or newWord[ind : ind + 5] or     #if you splice newWord to be 4, 5 or 7 characters long (since the swear words are this long)...
                                newWord[ind : ind + 7]) in swearDict:               #...and the spliced string is equal to a word in the swear dictionary, then:
                            value += 1                                              #add 1 to the value (tells you if you encounter at least one swear word in your word)
                            break                                                   #stops the for loop, getting indeces of your substring (you already found a swear word)
                    newWord = ""                                                    #starts your substring anew

            if value > 0 and line not in duplicateTweets:                           #if value > 0 (if you found at least one swear word in your word) and the line isn't already written:
                offensive.write(line)                                               #then write your line into your file
                duplicateTweets[line] = 0                                           #add your line to the duplicate dictionary (so you won't write the same tweet again)
                value = 0                                                           #start your value anew to loop back and check if the next word has a swear word
                counter += 1                                                        #stop the word for loop and move on to the next line (you already found at least one swear word in your tweet)
                break

    swear.close()                                                                   #close your files
    offensive.close()
    tweet.close()
    print(counter)

def findTopTrends(punctuationDict, N):
    tweet = open('twitter_data.txt', encoding="utf8")                               #opens your files to write
    topTags = open('top_hashtags.txt', 'w')
    topTagsDict = {}                                                                #will be a dictionary with all the tweets as keys and their frequency as value
    topNTags = []                                                                   #will be a list of all your hashtag frequencies that will later be used to sort
    correctHash = ""                                                                #will be a hashtag substring that ends when experiencing a punctuation mark

    for line in tweet:                                                              #splits your tweet file into lines (tweets)
        wordList = line.split()                                                     #splits tweet into a list of words
        for word in wordList:                                                       #splits list of words into words
            if "#" in word:                                                         #if a hashtag is encountered in the word:
                hashTag = word[word.index("#") : ]                                  #then make a substring (hashtag) that starts at the # and ends at the end of word
                hashTag = hashTag.lower()                                           #turn everything in hashtag lower case so can compare capital to lower case
                for indec in hashTag:                                               #splits hashtag into characters
                    if indec in punctuationDict and hashTag.index(indec) > 0:       #if character in punctuation dictionary and not looking at very beginning (which is obviously a #, a punctuation):
                        correctHash = hashTag[ : hashTag.index(indec)]              #then make correcthash a substring from start of hashtag to until you reach a punctuation mark
                        break                                                       #stop your for loop (you found your hashtag in your word)
                    else:                                                           #else if character not in punctuation dictionary or you are looking at the first hashtag:
                        correctHash = hashTag                                       #correcthash is just your hashtag (you don't find a punctuation mark at all)

                if len(correctHash) > 1:                                            #if your correcthash isn't just a # by itself:
                    if correctHash in topTagsDict:                                  #then if your correcthash is already a tophashtag:
                        topTagsDict[correctHash] += 1                               #adds 1 to the value of your correcthash in the toptags dictionary (you encountered you tophash another time)
                    else:                                                           #else if your correcthash is a unique hashtag:
                        topTagsDict[correctHash] = 1                                #adds your correcthash into your toptags dictionary and gives it a value of 1(it occured once)

    for value in topTagsDict:                                                       #basically adds every value in your toptags dictionary into your list
        topNTags.append(topTagsDict[value])

    topNTags.sort()                                                                 #sorts your list of values you got from your dictionary

    for count in range(N):                                                          #keeps going until you write N tophashtags into your file
        for ind in topTagsDict:                                                     #gets every value in your toptags dictionary
            if topTagsDict[ind] == topNTags[-1]:                                    #if value is equal to last value in list(the greatest value in toptagsdict, or the highest frequency):
                topTags.write(ind + ": " + str(topTagsDict[ind]) + "\n")            #then write your most popular hashtag (toptagsdict key), followed by its frequency (toptagsdict value)
                topNTags.pop()                                                      #delete the last value in list(so you can move on to the next most popular hashtag)
                topTagsDict.pop(ind)                                                #delete the key and value of your most popular hashtag in your dictionary so you can proceed
                break                                                               #stops the for loop so you can move on to the next most popular hashtag

    tweet.close()                                                                   #closes your files
    topTags.close()

findSwearWords(punctDict)                                                           #calls your swear method to write all tweets with swear words into a file
inp = int(input("Enter the number of top hash tags you want to see: "))             #asks for user input of how many of the top hashtags you want to see
findTopTrends(punctDict, inp)                                                       #calls your top trends method to write all your most trendy hashtags into a file