#! python3
import cmd
import sys
import textwrap

DESC = 'desc'
NORTH = 'north'
SOUTH = 'south'
WEST = 'west'
EAST = 'east'
START = 'start'
LEFT = 'left'
RIGHT = 'right'
DIFF = 'diff'
location = 'The Pharaohs Tomb'
dial = ''
puz = ''
main = ''
dark = ''
locked_door = ''
word = 'berm'
string = ''
SCREEN_WIDTH = 70
current_char = 0
rep_doctor = 0
rep_professor = 0
inventory = []
left_view = ['b', 'a', 'r', 'd']
current_view = ['f', 'e', 'l', 'k']
right_view = ['w', 'o', 'c', 'm']
started = False
solved = False
locked = True
showFullExits = True
doc_visited = False
pros_visited = False

npc_Data = {
    'Doctor Peter': {
        'His Name': 'Doctor Peter',
        'His Description': 'Short and stubby man, who has the facial hair of a preteen',
        'His Greetings': '"Well who do you think you are? Interrupting my work! you annoy me"'
    },
    'Professor Dan': {
        'His Name': 'Professor Dan',
        'His Description': 'tall and lanky, smells of incense and rosemary, wears his pants above his waist',
        'His Greetings': '"Hey man.. Got any gum? I smell your breath and its minty"'
    }
}

cryptRooms = {
    'The Pharaohs Tomb': {
        DESC: "---------------------------------------------------------------------- "
              'You are a degenerate gambler, and times have been tough..... '
              'luckily there is a small crypt you heard about, '
              'tales of jewels and riches fill your senses, you must enter. '
              'Welcome to The Pharaohs Tomb.                                       '
              "---------------------------------------------------------------------- "
              'Type "help" to view available commands, or type "start" to begin!. ',
        START: 'Main Room',
    },
    'Main Room': {
        DESC: 'This room is cold and murky, you see three doors to the north, east, west, '
              'a stone door to the south, and a Pharaoh symbol is on the ground',
        DIFF: 'This room is cold and murky, you see three doors to the north, east, west, '
              'and a Pharaoh symbol is on the ground',
        NORTH: 'Puzzle Room',
        WEST: 'Doctors Room',
        EAST: 'Professors Room',
        SOUTH: 'Dark Room',
    },
    'Doctors Room': {
        DESC: 'The room has sticky notes strewn along the walls, it smells of sulphur and pungent male cologne',
        EAST: 'Main Room',

    },
    'Professors Room': {
        DESC: 'The room is tidy, a nice aroma of lemons, wow even a couch is in here too!',
        WEST: 'Main Room',

    },
    'Puzzle Room': {
        DESC: 'The room has tall ceilings, four large sandstone pillers, with marble dials are presented in front of you {_} {_} {_} {_}',
        DIFF: 'The room has tall ceilings, the dials are in front of you unable to be moved',
        SOUTH: 'Main Room',
    },
    'Dark Room': {
        DESC: 'You enter the dark room but a small glimmer of light is in front of you, hope of escape is there',
        NORTH: 'Main Room',
    },
}

items = {
    'treasure': {
        DESC: 'this is the treasure of your most wildest imagination.',
    },
    'tablet': {
        DESC: 'A sandstone tablet, similar to the design to the door in the main room.',
    },
}


def view_map():
    global puz
    global dial
    global main
    global dark
    global locked_door

    dial = "           +----------+" \
           "\n           |          |"

    puz = "           |          |" \
          "\n           |   Puz.   |" \
          "\n           |          |" \
          "\n           |          |"
    main = "+----------+----OO----+----------+" \
           "\n|          |          |          |" \
           "\n|   Doc.   |   Main   |   Prof.  |" \
           "\n|          O          O          |" \
           "\n|          |          |          |" \
           "\n|          |          |          |"
    locked_door = "+----------+----XX----+----------+"
    dark = "           |          |" \
           "\n           |          |" \
           "\n           |   Dark   |" \
           "\n           |          |" \
           "\n           |          |" \
           "\n           +----------+"
    if location == 'Puzzle Room':
        if not solved:
            dial = "           +----------+" \
                   "\n           | ֍ ֍  ֍ ֍ |"
        puz = "           |          |" \
              "\n           |   Puz.   |" \
              "\n           |    ¶     |" \
              "\n           |          |"

    if not locked:
        locked_door = "+----------+----00----+----------+"

    if location == 'Main Room':
        main = "+----------+----OO----+----------+" \
               "\n|          |          |          |" \
               "\n|   Doc.   |   Main   |   Prof.  |" \
               "\n|          O    ¶     O          |" \
               "\n|          |    ╔╣    |          |" \
               "\n|          |          |          |"

    if location == 'Doctors Room':
        main = "+----------+----OO----+----------+" \
               "\n|          |          |          |" \
               "\n|   Doc.   |   Main   |   Prof.  |" \
               "\n|          O          O          |" \
               "\n| ₭    ¶   |          |          |" \
               "\n|          |          |          |"

    if location == 'Professors Room':
        main = "+----------+----OO----+----------+" \
               "\n|          |          |          |" \
               "\n|   Doc.   |   Main   |   Prof.  |" \
               "\n|          O          O      ₭   |" \
               "\n|          |          |  ¶       |" \
               "\n|          |          |          |"
    print(dial)
    print(puz)
    print(main)
    print(locked_door)
    print(dark)
    print()
    print("\tKey "
          "\n---------------"
          "\nUnlocked Doors = 0"
          "\nLocked Doors = X"
          "\nWall = -,+,|"
          "\nPuz. = Puzzle Room"
          "\nDoc. = Doctors Room"
          "\nProf. = Professors Room"
          "\n¶. = Player (You)"
          "\n֍ = Stone Dial"
          "\n₭ = Character"
          "\n╔╣ = Pharaoh Symbol")


def displayLocation(loc):
    """A helper function for displaying an area's description and exits."""

    # Print the room name.
    print(loc)
    print('=' * len(loc))

    # Print the room's description (using textwrap.wrap())
    if (location == 'Puzzle Room' and solved) or (location == 'Main Room' and not locked):
        print('\n'.join(textwrap.wrap(cryptRooms[loc][DIFF], SCREEN_WIDTH)))
    else:
        print('\n'.join(textwrap.wrap(cryptRooms[loc][DESC], SCREEN_WIDTH)))

    if loc == 'Puzzle Room':
        puzzle('center', 0)

    # Print all the exits.
    exits = []
    for direction in (NORTH, SOUTH, EAST, WEST):
        if direction in cryptRooms[loc].keys():
            exits.append(direction.title())
    print()
    if showFullExits:
        # Prints a full descriptions of the exits with direction and location
        for direction in (NORTH, SOUTH, EAST, WEST):
            if direction in cryptRooms[location]:
                print('%s: %s' % (direction.title(), cryptRooms[location][direction]))
    else:
        # Shows the brief direction of the exits without showing the connected rooms.
        print('Exits: %s' % ' '.join(exits))


def moveDirection(direction):
    """A helper function that changes the location of the player."""
    global location
    global started

    if direction in cryptRooms[location]:
        if direction == START:
            print('Starting Game...')
            started = True
        else:
            print('You move to the %s.' % direction)
        location = cryptRooms[location][direction]
        displayLocation(location)
    else:
        if direction == START:
            print('Game already started..')
        else:
            if location == 'The Pharaohs Tomb':
                print('Game not started')
                return
            else:
                print('You cannot move in that direction')


def puzzle(rotation, selection):
    print()
    global current_view
    global left_view
    global right_view
    global current_char
    global string
    global word
    temp = [None] * 5
    current_char = selection

    temp[0] = current_view[current_char]
    if not solved:
        if rotation == RIGHT:
            current_view[current_char] = left_view[current_char]
            temp[1] = right_view[current_char]
            right_view[current_char] = temp[0]
            left_view[current_char] = temp[1]
        if rotation == LEFT:
            current_view[current_char] = right_view[current_char]
            temp[1] = left_view[current_char]
            left_view[current_char] = temp[0]
            right_view[current_char] = temp[1]
        string = '} {'.join(str(x) for x in current_view)
        print("{" + string + '}')
        string = string.replace('} {', '')
        return
    else:
        print('The dials are locked into place, unable to be used again.')


class TextAdventureCmd(cmd.Cmd):
    prompt = '\n> '

    # I added this for the npc dialogue
    def __init__(self):
        super().__init__()
        self.location = 'Main Room'
        self.inventory = []
        self.showFullExits = True

    def dialogue_w_doc(self):
        global rep_doctor
        global doc_visited

        while True:
            room_info = cryptRooms[self.location]
            if room_info and rep_doctor < 10:
                print("What your senses detect as you enter")
                for keys, values in npc_Data['Doctor Peter'].items():
                    print(keys + ': ' + str(values))
                print()
            # First Meeting Doctor
            if (rep_doctor > -4) and (rep_doctor < 4):
                print("What do you want to say in response?")
                print("1:Who are you to talk to me like that? Where even is your PHD?")
                print("2:Listen, we are stuck here together. Help me help us escape ")
                print("3:Well you annoy me too but am I crying about it? Lets work together ")
                print("4: Leave Conversation")

                doc_visited = True
                user_input = input("> ").strip().lower()
                if user_input == '1' or user_input.startswith('Who'):  # Main response 1
                    like_counter = -2
                    print('bad response [Reputation: ' + str(like_counter) + ']')
                    print("Doc Peter: WHERE IS YOUR DAMN DEGREE?? I WORKED FOR 8 YEARS..(he rambles for 2 minutes)")

                    print("Doc Peter: Fine, whatever, why and WHO are you??")
                    print("1: A fool, cant believe I am stuck here")
                    print("2: Doesnt matter, I am trapped here same as you")
                    print("3: Leave Conversation")

                    user_input = input("> ").strip().lower()
                    if user_input == '1' or user_input.startswith('A'):  # Side response 1-1
                        like_counter = +1
                        print('ok response [Reputation: ' + str(like_counter) + ']')
                        print(
                            "Doc Peter: Yes I know that, whatever, I have been stuck here with one bumbling idiot already, dont make it two")
                        print("1: Okay fine fine.. can you help me with the puzzle?")
                        print("2: What do you have against the other guy?")
                        print("3: Leave Conversation")
                        user_input = input("> ").strip().lower()
                        if user_input == '1' or user_input.startswith('Okay'):
                            print('ok response [Reputation: ' + str(like_counter) + ']')
                            print(
                                "Doc Peter: Yeah sure kid, by the way you smell like acid, the word starts with B as in boy get out my WAY")
                            self.cmdloop()
                            break

                        elif user_input == '2' or user_input.startswith('What'):
                            like_counter = -2
                            rep_doctor = rep_doctor - 2
                            print('bad response [Reputation: ' + str(like_counter) + ']')
                            print("Doc Peter: He TRICKED me into coming, and now look at what HE did!!")
                            self.cmdloop()
                            break

                        elif user_input == '3' or user_input.startswith('Leave'):
                            self.cmdloop()
                            break
                        else:
                            print('Not a valid response\n')
                        break
                    elif user_input == '2':  # Side Response 1-2
                        like_counter = +1
                        rep_doctor = rep_doctor + like_counter
                        print('bad response [Reputation: ' + str(like_counter) + ']')
                        print("Doc Peter: Okay fine, it is nice to see a new face but ...")

                        print(
                            "Do dont you think I know that?, but yeah.. I guess I will help, I have some outdated textbooks here")
                        print("1: What do yout textbooks do??")
                        print("2: Do you think we can make a bomb thats big enough?")
                        print("3: Leave Conversation")

                        user_input = input("> ").strip().lower()
                        if user_input == '1' or user_input.startswith('What'):
                            like_counter = 1

                            print('ok response [Reputation: ' + str(like_counter) + ']')
                            print(
                                "Doctor Peter: They explain how the dials work, you twist them from right to left to find the correct combination")
                            print("Doc Peter: Go and try it")
                            self.cmdloop()

                            break

                        elif user_input == '2' or user_input.startswith('Bomb'):
                            like_counter = -2
                            rep_doctor = rep_doctor + like_counter
                            print('bad response [Reputation: ' + str(like_counter) + ']')
                            print("Doctor Peter: you must be braindead")
                            self.cmdloop()
                            break

                        elif user_input == '3':
                            self.cmdloop()
                            break
                        else:
                            print('Not a valid response\n')
                    elif user_input == '3' or user_input.startswith('Leave'):
                        break
                    else:
                        print('Not a valid response\n')
                elif user_input == '2':  # Main response 2
                    like_counter = 0
                    rep_doctor = rep_doctor + like_counter
                    print('neutral response [Reputation: ' + str(like_counter) + ']')

                    print(
                        " Doc Peter: Yeah I guess so, my textbooks have told me how the puzzle works, I just cant get the right COMBINATION!")
                    print("1: Would you want me to go check it out?")
                    print("2: Have you tried to ask the other guy?")
                    print("3: Leave Conversation")

                    user_input = input("> ").strip().lower()
                    if user_input == '1' or user_input.startswith('Would'):  # Side Response 2-1
                        like_counter = 1
                        rep_doctor = rep_doctor + like_counter
                        print('ok response [Reputation: ' + str(like_counter) + ']')

                        print(
                            "Doc Peter: Took the words out of my mouth, before you go, move the dials right and left for the right word combo")
                        print("1: Thanks Doctor Peters!")
                        print("2: ok")
                        print("3: Leave Conversation")

                        user_input = input("> ").strip().lower()
                        if user_input == '1' or user_input.startswith('thanks'):
                            print('bad response [Reputation: ' + str(like_counter) + ']')
                            print("Doc Peter: You are a twerp")
                            print("Doc Peter: get out and try it wuss")
                            self.cmdloop()
                            break

                        elif user_input == '2' or user_input.startswith('ok'):
                            like_counter = +3
                            rep_doctor = rep_doctor + like_counter
                            print('goof response [Reputation: ' + str(like_counter) + ']')
                            print("Doc Peter: *Huffs in agreement*")
                            self.cmdloop()
                            break

                        elif user_input == '3' or user_input.startswith('Leave'):
                            self.cmdloop()
                            break
                        else:
                            print('Not a valid response\n')
                    elif user_input == '2':  # Side Response 2-2
                        like_counter = -2
                        rep_doctor = rep_doctor + like_counter
                        print('bad response [Reputation: ' + str(like_counter) + ']')

                        print("Doc Peter: Are you braindead?")
                        print("1:wow tough crowd *awkward laugh*")
                        print("2: Leave Conversation")

                        user_input = input("> ").strip().lower()
                        if user_input == '1' or user_input.startswith('wow'):
                            like_counter = -3
                            rep_doctor = rep_doctor + like_counter
                            print('bad response [Reputation: ' + str(like_counter) + ']')
                            print("Look buddy, this ain't fun and games, "
                                  "that idiot professor is what got us trapped in the first place.")
                            print('[The doctor refuses to talk to you]')
                            self.cmdloop()
                            break

                        elif user_input == '2' or user_input.startswith('Leave Conversation'):
                            self.cmdloop()
                            break
                        else:
                            print('Not a valid response\n')
                    elif user_input == '3' or user_input.startswith('Leave Conversation'):
                        break
                    else:
                        print('Not a valid response\n')
                elif user_input == '3':  # Main response 3
                    like_counter = +2
                    rep_doctor = rep_doctor + like_counter
                    print('good response [Reputation: ' + str(like_counter) + ']')

                    print("*You challenge him*")
                    print("Doc Peter: You know what.. my bad what do you want")
                    print("1: How can I get the treasure and escape?")
                    print("2: What does the dark room do?")
                    print("3: Leave Conversation")
                    user_input = input("> ").strip().lower()

                    if user_input == '1' or user_input.startswith('How'):  # Side Response 3-1
                        like_counter = 1
                        rep_doctor = rep_doctor + like_counter
                        print('ok response [Reputation: ' + str(like_counter) + ']')

                        print("If you solve the puzzle to the treasure, and the dark room is the way out")
                        print("1: How do I get through the dark room??")
                        print("2: So if I solve the puzzle, the treasure is mine")
                        print("3: Leave Conversation")
                        user_input = input("> ").strip().lower()

                        if user_input == '1':
                            like_counter = 1
                            rep_doctor = rep_doctor + like_counter
                            print('ok response [Reputation: ' + str(like_counter) + ']')
                            print("Doc Peter: If I give you the key, you can escape, but I need the puzzle solved")
                            print('[tablet has been added to your inventory]')
                            inventory.append('tablet')
                            self.cmdloop()
                            break

                        elif user_input == '2':
                            like_counter = -1
                            rep_doctor = rep_doctor + like_counter
                            print('bad response [Reputation: ' + str(like_counter) + ']')
                            print("Doc Peter: Well that's a start, but make sure we share the treasure,"
                                  "I dont want you taking it all")

                        elif user_input == '3' or user_input.startswith('Leave'):
                            self.cmdloop()
                            break
                        else:
                            print('Not a valid response\n')
                    elif user_input == '2':  # Side Response 3-2
                        like_counter = 0
                        rep_doctor = rep_doctor + like_counter
                        print('neutral response [Reputation: ' + str(like_counter) + ']')

                        print("Doc Peter: Keeps us locked in here, I cant have it open unless I get that treasure")
                        print("1: Wait so you can get us out now??")
                        print("2: Soo if I get the treasure you will let us out?")
                        print("3: Leave Conversation")

                        user_input = input("> ").strip().lower()
                        if user_input == '1' or user_input.startswith('wait'):
                            like_counter = -1
                            rep_doctor = rep_doctor + like_counter
                            print('ok response [Reputation: ' + str(like_counter) + ']')
                            print(
                                "Doc Peter: Yeah, you will either have to kill me or get the treasure, and I was a boxer")
                            self.cmdloop()
                            break

                        elif user_input == '2':
                            like_counter = +2
                            rep_doctor = rep_doctor + like_counter
                            print('good response [Reputation: ' + str(like_counter) + ']')
                            print("Doc Peter: Couldn't have said it better myself, "
                                  "here's a ancient key for the southern door, now get along")
                            print('[tablet has been added to your inventory]')
                            inventory.append('tablet')
                            self.cmdloop()

                        elif user_input == '3' or user_input.startswith('Leave'):
                            self.cmdloop()
                            break
                        else:
                            print('Not a valid response\n')
                    elif user_input == '3' or user_input.startswith('Leave'):
                        self.cmdloop()
                        break
                    else:
                        print('Not a valid response\n')
                elif user_input == '4' or user_input.startswith('Leave'):  # Main response 4
                    break
                else:
                    print('Not a valid response\n')

            elif rep_doctor <= -4:
                print("You arent talking this seriously, go away!")
                break

            elif rep_doctor >= 4:
                print("Hey, thanks for helping me out")
                if ('tablet' not in inventory) & locked:
                    print('Hey dont forget this, you will need it for the stone door')
                    print('[tablet has been added to your inventory]')
                    inventory.append('tablet')
                break

    # The default() method is called when none of the other do_*() command methods match.

    def dialogue_w_prf(self):
        global rep_professor
        global pros_visited
        like_counter = 0

        while True:
            room_info = cryptRooms[self.location]
            if room_info and like_counter < 10:
                print("What you see and hear as you enter")
                for keys, values in npc_Data['Professor Dan'].items():
                    print(keys + ': ' + str(values))
                print()
            # First Meeting Professor
            if (rep_professor > -4) or (rep_professor < 4):
                print("What would you like to respond with?")
                print("1: Uhhh no gum.. do you know how to get out of here?")
                print("2: Hey, how did you get locked in here??")
                print("3: Listen, not sure if you are sane or not, are you going to help or what? ")
                print("4: Leave Conversation")

                pros_visited = True
                user_input = input("> ").strip().lower()
                if user_input == '1' or user_input.startswith('uhh'):  # Main response 1
                    like_counter = 0
                    rep_professor = rep_professor + like_counter
                    print('neutral response [Reputation: ' + str(like_counter) + ']')
                    print("Prof Dan:No gum?... lame...")

                    print("Prof Dan: well from what I've deduced.. we are trapped")
                    print("1: How should we try and escape?")
                    print("2: Okay, I heard noises from the other room, whats the dude about?")
                    print("3: Soooooooo.. why am I trapped here?")

                    user_input = input("> ").strip().lower()
                    if user_input == '1' or user_input.startswith('How'):  # Side response 1-1
                        like_counter = +2
                        rep_professor = rep_professor + like_counter
                        print('good response [Reputation: ' + str(like_counter) + ']')
                        print("*Professor Dan gets visibly excited*")
                        print(
                            "Prof Dan: WELL, I have been stuck here for what feels like centuries, I am more than qualified to explain")

                        print("1: How is this place locked so tight?")
                        print("2: What led you to be here in the first place?")
                        print("3: Leave Conversation")
                        user_input = input("> ").strip().lower()

                        if user_input == '1':
                            print(
                                "Prof Dan:The ancient Pharoh that once built this place wanted to prevent grave robbers.. guess it worked")
                            print(
                                "Prof Dan: The only way to truly escape is to solve his riddle, maybe you can give me some insight?")
                            like_counter = +2
                            rep_professor = rep_professor + like_counter
                            print('good response [Reputation: ' + str(like_counter) + ']')
                            print("1: What do you know about it?")
                            print("2: Yeah I have no clue, I just need to get out of here")
                            print("3: Leave Conversation")
                            user_input = input("> ").strip().lower()
                            if user_input == '1' or user_input.startswith('What'):
                                print("Prof Dan: Only one thing, the third letter is r. That is all I know")
                                print("Prof Dan: But hey, that should help us get out of here.")
                                self.cmdloop()
                                break
                            elif user_input == '2' or user_input.startswith("Yeah"):
                                print("Prof Dan:Bud.. work with me here, go check the puzzle and come back")
                                self.cmdloop()
                                break
                            elif user_input == '3' or user_input.startswith('Leave'):
                                self.cmdloop()
                                break
                            else:
                                print("Invalid Input")

                        elif user_input == '2':
                            like_counter = +1
                            rep_professor = rep_professor + like_counter
                            print(
                                "Prof Dan: I have been studying this Pharoh for years.. he was overthrown, and his enemies burned his records. I want to bring them back")
                            print(
                                "Prof Dan: That is where you come in, if you find the treasure it will prove his existance and secure my funding")
                            print('ok response [Reputation: ' + str(like_counter) + ']')

                            print("a: I dont care about funding, but treasure sounds nice, how can I get it?")
                            print("b: We can do that, how can I get the treasure?")
                            user_input = input("> ").strip().lower()

                            if user_input == 'a' or user_input.startswith("I"):
                                print("Prof Dan: Thanks jerk, anyway go solve the puzzle")
                                self.cmdloop()
                                break
                            elif user_input == 'b' or user_input.startswith('We'):
                                print("Prof Dan: Brilliant, what I have discovered is that the third letter is r")
                                self.cmdloop()

                            break

                        elif user_input == '3':
                            self.cmdloop()
                            break
                        else:
                            print('Not a valid response\n')
                    elif user_input == '2' or user_input.startswith('Who'):  # Side Response 1-2
                        like_counter = +0
                        rep_professor = rep_professor + like_counter
                        print('ok response [Reputation: ' + str(like_counter) + ']')

                        print(
                            "Prof Dan:Oh him? hes just a salty jerk who doesnt like to have his masculinity challenged... I have been stuck with him for 20 years")
                        print("1: Do you think he will help us?")
                        print("2: Yeah I noticed... what can I say to convince him")
                        print("3: Leave Conversation")

                        user_input = input("> ").strip().lower()
                        if user_input == '1':
                            print(
                                'Prof Dan: Us? no, help you? maybe... hes a interesting guy I guess, just let him ramble [Reputation: ' + str(
                                    like_counter) + ']')
                            print("Prof Dan: He has some letters I don't maybe go check him out")
                            break

                        elif user_input == '2':
                            like_counter = +2
                            rep_professor = rep_professor + like_counter
                            print('good response [Reputation: ' + str(like_counter) + ']')
                            print("Prof Dan: Could not tell you, he hates my guts")
                            print(
                                "Prof Dan: I never wanted him to come in the first place so I dont know why he resents me but whatever")
                            break

                        elif user_input == '3':
                            self.cmdloop()
                            break
                        else:
                            print('Not a valid response\n')
                    elif user_input == '3' or user_input.startswith('so'):
                        print("Prof Dan: Dude you came here I dont know why")

                        break
                    else:
                        print('Not a valid response\n')
                elif user_input == '2' or user_input.startswith('Who'):  # Main response 2
                    like_counter = +0
                    print('ok response [Reputation: ' + str(like_counter) + ']')

                    print(
                        "Prof Dan: Well yes, I wanted to expand my professional career and uh the other guy? he wants money")
                    print("1: Seriously I have to convince him? Can I solve it on my own?")
                    print("2: Well he told me some stuff already, I will just go solve it")
                    print("3: Leave Conversation")

                    user_input = input("> ").strip().lower()
                    if user_input == '1':  # Side Response 2-1
                        print('ok response [Reputation: ' + str(like_counter) + ']')

                        print(
                            "Prof Dan: Yeah seriously, unless you can figure out the code, which more power to you if you can")
                        print("Prof Dan: Think of a river, its related trust me")

                        self.cmdloop()
                        break
                    elif user_input == '2':  # Side Response 2-2
                        like_counter = -1
                        rep_professor = rep_professor + like_counter
                        print('bad response [Reputation: ' + str(like_counter) + ']')

                        print("Prof Dan: Good! I bet it was a pain to get though, good luck man")
                        self.cmdloop()
                        break
                    elif user_input == '3':
                        self.cmdloop()

                        break
                    else:
                        print('Not a valid response\n')
                elif user_input == '3':  # Main response 3
                    like_counter = -3
                    rep_professor = rep_professor + like_counter
                    print('bad first impression [Reputation: ' + str(like_counter) + ']')

                    print(
                        "Prof Dan: Not sure if I am sane? well what about you?? Youre the idiot who got stuck in here recently ")
                    print("Prof Dan: Even so, I need your help just like you need mine. Better not betray me")

                    print("1: What should I do first")
                    print("2: Leave Conversation")
                    user_input = input("> ").strip().lower()

                    if user_input == '1' or user_input.startswith('What'):  # Side Response 3-1
                        like_counter = +0
                        print('neutral response [Reputation: ' + str(like_counter) + ']')

                        print("Prof Dan: Maybe just maybe work on your tact")
                        print("Prof Dan: Check the puzzle out and come back")
                        self.cmdloop()
                        break
                    elif user_input == '2' or user_input.startswith('Leave'):  # Side Response 3-2
                        self.cmdloop()
                        break

                elif user_input == '4' or user_input.startswith('Leave'):  # Main response 4
                    self.cmdloop()
                    break
                else:
                    print('Not a valid response\n')

            elif rep_professor <= -4:
                print("Im not talking anymore")
                break

            elif rep_professor >= 4:
                print("Thank you for helping me, dont forget that the third letter is {r}")
                break

    def default(self, arg):
        print('I do not understand that command. Type "help" for a list of commands.')

    def do_quit(self, arg):
        """Quit the game."""
        return True  # Breaks out of the cmd loop

    def do_north(self, arg):
        """Moves the character north if able."""
        moveDirection('north')

    def do_south(self, arg):
        """Moves the character south if able."""
        if location == 'Main Room' and locked:
            print('The door wont budge')
        else:
            moveDirection('south')

    def do_east(self, arg):
        """Moves the character east if able."""
        moveDirection('east')
        if location == 'Professors Room':
            self.dialogue_w_prf()

    # dialogue being tied to direction maybe isn't a good idea lol, player can get dialogue trigger in wrong room.
    # probably aware already just thought I'd mention.
    def do_west(self, arg):
        """Moves the character west if able."""
        moveDirection('west')
        if location == 'Doctors Room':
            self.dialogue_w_doc()

    def do_start(self, arg):
        """Starts the game"""
        moveDirection('start')

    def do_exits(self, arg):
        """Shows full descriptions of where exits lead too vs all available exits."""
        global showFullExits

        if not started:
            print('Game not started')
            return
        showFullExits = not showFullExits
        if showFullExits:
            print('Showing the description of the exit')
        else:
            print('Showing a brief description of the exits')

    def do_map(self, arg):
        """View the in-game map (shows all the room connections)"""
        if not started:
            print('Game not started')
        else:
            view_map()

    def do_left(self, arg):
        """Brings a character in the word puzzle from right to left with position input"""
        if location != 'Puzzle Room':
            print('You are not in the puzzle Room')
            return
        else:
            while True:
                try:
                    pos = int(input('Select what character position: \n'))
                    break
                except:
                    print('Input a number!')
            pos = pos - 1
            puzzle('left', pos)
            if pos < 0 or pos > 3:
                print('Not a valid character position!')
                return

    def do_right(self, arg):
        """Brings a character in the word puzzle from left to right with position input"""
        if location != 'Puzzle Room':
            print('You are not in the puzzle Room')
            return
        else:
            while True:
                try:
                    pos = int(input('Select what character position: \n'))
                    break
                except:
                    print('Input a number!')
            pos = pos - 1
            puzzle('right', pos)
            if pos < 0 or pos > 3:
                print('Not a valid character position!')
                return

    def do_location(self, arg):
        """View Information about the current location incase it is lost"""
        displayLocation(location)

    def do_submit(self, arg):
        """Submit your guess for the puzzle"""
        global solved
        if not started:
            print('Game not started')
        elif location == 'Puzzle Room':
            if word == string:
                print(
                    'the stone dials sink into the floor, opening the door revealing the door. the treasure is yours.')
                inventory.append('treasure')
                solved = True
            else:
                print('Pressing the button, nothing happens with the dials.')
        else:
            print('You are not in the Puzzle Room')

    def do_inventory(self, arg):
        """Access the players inventory"""
        if not started:
            print('Game not started')
            return

        elif len(inventory) == 0:
            print('Inventory:\n (Contains no Items)')
            return
        # Prints out each item in inventory
        print('Inventory:')
        for item in set(inventory):
            print('  ' + item)

    def do_view_item(self, arg):
        """View an item in your inventory"""
        if not started:
            print('Game not started')
            return
        elif not inventory:
            print('Inventory contains no items')
            return
        else:
            item = input('What item do you want to view: \n')
            if item in inventory:
                print('\n' + item + ": " + "".join(textwrap.wrap(items[item][DESC], SCREEN_WIDTH)))
            else:
                print('You do not have this item.')

    def do_escape(self, arg):
        """Escape if you can"""
        if not started:
            print('Game not started')
            return
        elif location != 'Dark Room':
            print('You are not in the dark room.')
            return
        else:
            while True:
                confirm = input("Are you sure you want to escape (Yes or no): \n")
                confirm = confirm.lower()
                if confirm == 'yes' or 'y' or confirm == 'no' or 'n':
                    break
                else:
                    print('Please enter Yes or No')

            if confirm == 'yes' or confirm == 'y':
                if 'treasure' in inventory:
                    print('You escape with the treasure')
                    print('[GAME WIN]')
                    sys.exit()
                else:
                    print('You escape without the treasure.')
                    print('[GAME LOSE]')
                    sys.exit()
            else:
                return

    def do_unlock(self, arg):
        """Attempt to unlock the locked door"""
        global locked
        if not started:
            print('Game not started')
            return
        elif 'tablet' in inventory and location == 'Main Room':
            print('You insert the tablet into the door, as it disappears, the door opens in front of you')
            locked = False
            inventory.remove('tablet')
            return
        elif 'tablet' not in inventory and location == 'Main Room':
            print('You attempt to open the door, but you do not have the item to do so.')
            return
        else:
            print('There is no door to unlock here')

    def do_reputation(self, arg):
        """View reputation with a character you have visited"""
        if not started:
            print('Game not started')
        if (not pros_visited) & (not doc_visited):
            print('You have not visited anyone')
        if pros_visited:
            print('{Total Professor Reputation: [' + str(rep_professor), end='')
            if rep_professor <= -4:
                print('] (LOW REPUTATION)}')
            elif rep_professor >= 4:
                print('] (GOOD REPUTATION)}', )
            else:
                print('] (Neutral Reputation)}')
        if doc_visited:
            print('{Total Doctor Reputation: [' + str(rep_doctor), end='')
            if rep_doctor <= -4:
                print('] (LOW REPUTATION)}')
            elif rep_doctor >= 4:
                print('] (GOOD REPUTATION)}', )
            else:
                print('] (Neutral Reputation)}')

    do_inv = do_inventory
    do_n = do_north
    do_s = do_south
    do_e = do_east
    do_w = do_west
    do_loc = do_location
    do_view = do_view_item
    do_rep = do_reputation


# Commented out the welcome, I moved alot of it to the "start menu",
# I didn't delete chance, so you can get a chance to look and see how it compares.
if __name__ == '__main__':
    print()
    displayLocation(location)
    TextAdventureCmd().cmdloop()
    print('Thank you for playing!')
