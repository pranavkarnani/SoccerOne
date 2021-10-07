from data_processors.SoccerOneMaster import makeMaster

makeMaster()

while(True):
    print("""
1. Our Picks
2. PLayer Stats
3. Upcoming Fixtures
4. League Standings""")
    first_selection = input()
    if (first_selection == "1"):
        while(True):
            print("""Here are our Picks.
            #Populate from a function and then display here
            1. 
            2.
            3.
            4.
            5.
            6.
            7.
            8.
            9.
            10.
            11.
            12.
            
            1.1 Why we choose the team
            1.2 Player performance Analysis
            1.3 Player Alternatives
            1.4 Why this formation
            1.5 Why not certain players
            1.6 Back to main menu""")
            player_pick_selection = input()
            if(player_pick_selection=="1"):
                print("Reasons for choosing the team")
            elif(player_pick_selection=="2"):
                print("Player Performance")
            elif (player_pick_selection == "3"):
                print("Player Alternatives")
            elif (player_pick_selection == "4"):
                print("Formation reasoning")
            elif (player_pick_selection == "5"):
                print("Why we didn't choose...")
            elif (player_pick_selection == "6"):
                break
    elif (first_selection == "2"):
        while(True):
            print("""
            2.1 Which position?
                1. Forward
                2. Mid
                3. Defense
                4. Goalkeeper
                5. Back to main menu"""
            )

            player_stat_position = input()
            if (player_stat_position == "1"):
                while(True):
                    print("""Which Attack positions?
                    1.
                    2.
                    3.
                    4.
                    """)
            elif (player_stat_position == "2"):
                print("Player Performance")
            elif (player_stat_position == "3"):
                print("Player Alternatives")
            elif (player_stat_position == "4"):
                print("Formation reasoning")
            elif (player_stat_position == "5"):
                break
    elif (first_selection == "3"):
        print("Upcoming Fixtures")
    elif (first_selection == "4"):
        print("League Standings")


