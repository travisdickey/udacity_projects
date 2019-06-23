# IPND Stage 2 Final Project

# A fill-in-the-blanks quiz, providing a paragraph in which users are prompted to give the missing
# words. Users must type the answers with exactly the correct spelling in order to get the answer correct.

# List of blanks to be passed in to the start quiz function.
blanks  = ["___1___", "___2___", "___3___", "___4___", "___5___"]


# quiz_strings: 3 levels of difficulty along with answers for each

easy = '''When writing ___1___ programs, it is important to be concise. Just as when writers write
novels, they want the language to be elegant and tight, ___2___s want programs to execute tasks
in as few lines as possible. One useful way to accomplish this is by writing ___3___. These are
blocks of code which perform specific tasks and can be called using their pre-defined name and
passing in ___4___. In Python, they are defined using the def keyword and the ___4___, followed
by a block of code and usually ending with a ___5___ statement.'''

answers_easy = ["computer", "programmer", "functions", "parameters", "return"]

medium = '''It can be rather complicated to write elegant, tight code for ___1___s, also known as ___2___s,
especially when writing nested ___2___s. It requires some rather complicated mental gymnastics
to step through the multiple tasks, which utilize multiple parameters, to clearly understand what
is happening. This is where a sound, logical approach to problem solving and ___3___ is so useful.
If you can identify the ___4___s and ___5___s, break the tasks into small chunks, test your code as
you go, and recognize that all programmers make mistakes, you'll be well on your way to writing
robust and elegant code.'''

answers_medium = ["function", "procedure", "debugging", "input", "output"]


hard = '''No, the process of writing computer programs is not that different from writing text.
Plan, write, and revise. Re-write and re-revise, until the text, or ___1___, is as clear and concise
as possible. The only real difference is that elegance in text is for aesthetic purposes, whereas
in programming, it conserves valuable ___2___ power. It affects productivity. Maximum ___3___
efficiency minimizes the use of limited computational resources. If the algorithms we employ are
loose and inelegant, they will suck up too much ___4___ or take too much ___5___ to execute.'''

answers_hard = ["code", "processing", "algorithmic",  "memory", "time"]

# Starts game, prompts user to decide difficulty level; calls play_game at appropriate level
# I got the idea for how to handle this function from jjfreeley on the Udacity forums
def difficulty():
    print "\nWelcome to my fill-in-the-blanks quiz.\n"
    level = raw_input("Please choose difficulty level. Type easy, medium, or hard.\n")
    if level == "easy":
        print "\nYou've chosen easy.\n\nYou get 5 guesses per problem."
        return play_game(easy, answers_easy)
    if level == "medium":
        print "\nYou've chosen medium.\n\nYou get 5 guesses per problem."
        return play_game(medium, answers_medium)
    if level == "hard":
        print "\nYou've chosen hard.\n\nYou get 5 guesses per problem."
        return play_game(hard, answers_hard)
    return difficulty()

# Checks if a word in answers is a substring of the word passed in.
def is_blank(word, blanks):
    for blank in blanks:
        if blank in word:
            return blank
    return None

# Checks if user_answer is in answers; returns boolean
def is_correct(user_answer, replacement, answers):
    if replacement == blanks[0]:
        return user_answer == answers[0]
    elif replacement == blanks[1]:
        return user_answer == answers[1]
    elif replacement == blanks[2]:
        return user_answer == answers[2]
    elif replacement == blanks[3]:
        return user_answer == answers[3]
    elif replacement == blanks[4]:
        return user_answer == answers[4]
    return None

# takes word, replacement, user_answer, revised; prints text for a correct response,
# also returns word, revised
def display_corrected(word, replacement, user_answer, revised):
    word = word.replace(replacement, user_answer)
    revised = corrected_string(replacement, user_answer, revised)
    print "\nThat is correct! The paragraph now reads as follows:\n" + revised + "\n"
    print "Well done!"
    return word, revised

# Takes current blank, user_answer, and quiz_string and returns revised quiz_string.
def corrected_string(word, user_answer, quiz_string):
    revised = quiz_string
    revised = revised.replace(word, user_answer, 1)
    return revised

# prompts user and checks answers after first incorrect response; takes attempts, max_attempts, word,
# replacement, revised, and answer; returns word, revised
def not_correct(attempts, max_attempts, word, replacement, revised, answers):
    while attempts < max_attempts:
        if (max_attempts - attempts) > 1:
            print "\nI'm sorry. That is not correct. Try again. You have " + str(max_attempts - attempts) + " tries left."
            user_answer = raw_input("What should be substitued for " + replacement + "?" + " ")
            if is_correct(user_answer, replacement, answers):
                word, revised = display_corrected(word, replacement, user_answer, revised)
                break
        elif (max_attempts - attempts) == 1:
            print "\nI'm sorry. That is not correct. You have only " + str(max_attempts - attempts) + " try left."
            user_answer = raw_input("What should be substitued for " + replacement + "?" + " ")
            if is_correct(user_answer, replacement, answers):
                word, revised = display_corrected(word, replacement, user_answer, revised)
                break
            print "I'm sorry. You have reached the maximum number of incorrect responses. Please try again later."
            quit()
        attempts += 1
    return word, revised

# Runs a fill-in-the-blanks quiz; takes quiz_string and answers; prompts user
#to replace blanks in quiz_string; displays corrected quiz_string
def play_game(quiz_string, answers):
    replaced = []
    attempts, max_attempts = 1, 5
    revised = quiz_string
    print "\n" + quiz_string + "\n"
    quiz_string = quiz_string.split()
    for word in quiz_string:
        replacement = is_blank(word, blanks)
        if replacement != None:
            user_answer = raw_input("What should be substitued for " + replacement + "?" + " ")
            if is_correct(user_answer, replacement, answers):
                word, revised = display_corrected(word, replacement, user_answer, revised)
            else:
                word, revised = not_correct(attempts, max_attempts, word, replacement, revised, answers)
        replaced.append(word)
    replaced = " ".join(replaced)
    print "Congratulations! You won."
    return replaced

difficulty()
