#ATD SELECTION SIMULATOR
"""
A program aimed to simulate solo drafting a team of 5-10 players
This program utilizes baseline fit checks, 
a database of previous draft positions, and weighted randomness 
to simulate what players would be availible for a person
in an NBA standard All-Time Draft
"""
"""
stuff to note:

selection value = ((adp - current selection) + (faller rating)) * (positional value * positional scarcity)
lower = higher chance of getting selected

"""
import random
import csv
import statistics

#Class Initialization
class Player:
    #Class Intended to Store Values, with getter methods
    def __init__(self, name=str, position=str, selection_history=list):
        self.name = name
        self.position = position
        self.adp = sum(selection_history) / len(selection_history)
        try:
            self.faller_rating = statistics.stdev(selection_history)
        except statistics.StatisticsError:
            self.faller_rating = 20
    
    def get_position_value(self):
        position_dict = {'Guard': 1.25, 'Wing': .75, 'Forward': 1, 'Big': 1.5}
        positions = self.position.split('/')
        value = 0
        if (len(positions) == 1):
            return position_dict[positions[0]]
        for pos in positions:
            value += position_dict[pos]
        return value / (len(positions) * 1.25)
    
    def get_position_order(self):
        position_dict = {'Guard': 1, 'Wing': 2, 'Forward': 3, 'Big': 4}
        positions = self.position.split('/')
        value = 0
        for pos in positions:
            value += position_dict[pos]
        return value / len(positions) 
    
    def get_position_score(self):
        position_dict = {'Guard': 1, 'Wing': 1.5, 'Forward': 2, 'Big': 2.5}
        positions = self.position.split('/')
        value = 0
        for pos in positions:
            value += position_dict[pos]
        return value / len(positions) 

    def get_name(self):
        return self.name

    def get_position(self):
        return self.position
    
    def get_adp(self):
        return self.adp
    
    def get_faller_rating(self):
        return self.faller_rating
    
    def __str__(self) -> str:
        return f'{self.get_name()} - {self.get_position()}'

class Team:
    def __init__(self, selection=int, num_players=int):
        self.order = selection
        self.max_players = num_players
        self.starters = []
        self.bench = []

    def add_player(self, player=Player):
        if (len(self.starters) < 5):
            self.starters.append(player)
        else:
            self.bench.append(player)      
   
    def fit_value(self, player=Player, center_clause=bool) -> int:
        if (len(self.starters) < 5):
            return self.calculate_fit(self.starters, player, FIT_THRESHOLD, center_clause)
        return self.calculate_fit(self.bench, player, FIT_THRESHOLD, center_clause)

    def calculate_fit(self, team=list, player=Player, threshold=int, center_clause=bool) -> int:
        position_check = player.get_position()
        fit = player.get_position_score()
        hard_threshold = threshold / 2
        rating = 1
        for teammate in team:
            if (center_clause and (position_check.find('Big') > -1 and teammate.get_position().find('Big') > -1)):
                return 1.5
            if (abs(fit - teammate.get_position_score()) <= hard_threshold):
                rating += .5 
            elif (abs(fit - teammate.get_position_score()) <= threshold):
                rating += .25
            else:
                rating -= .25

        if (rating < .25):
            return .25
        return rating
    
    def get_order(self):
        return self.order
    
    def __str__(self) -> str:
        returned_string = (f'TEAM {self.order}:')
        starting_lineup = sorted(self.starters, key=lambda x: x.get_position_order())
        for starter in starting_lineup:
            returned_string += f'\n{starter}'
        bench_lineup = sorted(self.bench, key=lambda x: x.get_position_order())
        returned_string += f'\n-'
        for sub in bench_lineup:
            returned_string += f'\n{sub}'
        return returned_string

class AllTimeDraft:
    def __init__(self, teams=int, rounds=int, selections=int, database=list):
        self.teams = teams
        self.rounds = rounds
        self.selections = selections
        self.search_depth = 1
        self.availible_players = self.data_create(database)
        self.list_of_teams = self.teams_create(teams, rounds)
    
    def data_create(self, database=list):
        player_list = []
        for i in range(len(database[0])):
            player_list.append(Player(database[0][i], database[1][i], database[2][i]))
        return player_list

    def teams_create(self, teams=int, rounds=int):
        teams_list = []
        for i in range (1, teams + 1):
            teams_list.append(Team(i, rounds))
        return teams_list
    
    def find_team(self, selection=int) -> Team:
        for team in self.list_of_teams:
            if (team.get_order() == selection):
                return team
        return (f'Not Found')
    
    def find_player(self, name):
        for player in self.availible_players:
            if (player.get_name() == name):
                return player
        return (f'Not Found')

    def sorted_list(self, players=list):
        return sorted(players, key=lambda x: x.get_adp())

    def positional_scarcity(self, player=Player):
        sorted_players = self.sorted_list(self.availible_players)
        players_checked = 20
        similar_players = 0
        
        for i in range(players_checked):
            if (abs(sorted_players[i].get_position_value() - player.get_position_value()) <= FIT_THRESHOLD / 2):
                similar_players += 1
        return ((similar_players / players_checked) * 2)

    def auto_select(self, selection=int, selection_number=int):
        #The amount of players searched depends on what selection it is, deeper into the draft = more players considered for selection since talent drop off isn't as hard
        match selection_number:
            case 40:
                self.search_depth = 3
            case 90:
                self.search_depth = 5
            case 140:
                self.search_depth = 7
        
        selecting_team = self.find_team(selection)
        players_considered = []
        sorted_players = self.sorted_list(self.availible_players)
        teams_searched = 0
        
        #Collects players for consideration, there is a two center clause in the 'True'
        try:
            while (len(players_considered) <= self.search_depth):
                if (selecting_team.fit_value(sorted_players[teams_searched], True) < ADDING_THRESHOLD):
                    players_considered.append(sorted_players[teams_searched])
                teams_searched += 1
        except IndexError:
            teams_searched = 0
            while (len(players_considered) <= self.search_depth):
                if (selecting_team.fit_value(sorted_players[teams_searched], False) <= ADDING_THRESHOLD):
                    players_considered.append(sorted_players[teams_searched])
                teams_searched += 1

        #Weights choices of players based on fit, positional scarcity, etc.
        chance_weights = []
        for considered in players_considered:
            #selection value = ((adp - current selection) + (faller rating)) * (positional value * positional scarcity)
            #lower = higher chance of getting selected
            chance_weights.append(((considered.get_adp() - selection_number) + considered.get_faller_rating()) * (considered.get_position_value() * self.positional_scarcity(considered)))
        
        negative_weights = []
        zero_weights = []
        for count, weight in enumerate(chance_weights):
            if (weight < 0):
                negative_weights.append([weight, players_considered[count]])
            elif (weight == 0):
                zero_weights.append(players_considered[count])

        if len(negative_weights) > 0:
            return self.team_select(selecting_team, random.choices([i[1] for i in negative_weights], [abs(i[0]) for i in negative_weights], k=1), selection_number, selection)
        if len(zero_weights) > 0:
            return self.team_select(selecting_team, random.choice(zero_weights), selection_number, selection)
    
        sum_weights = sum(chance_weights)
        return self.team_select(selecting_team, random.choices(players_considered, [(sum_weights - i) for i in chance_weights], k=1), selection_number, selection)
    
    def team_select(self, selecting_team=Team, selected_player=Player, selection_number=int, selection=int):
        try:
            self.availible_players.remove(selected_player)
            selecting_team.add_player(selected_player)
            return f'{selection_number}. {selection} - {selected_player.get_name()}'
        except ValueError:
            self.availible_players.remove(selected_player[0])
            selecting_team.add_player(selected_player[0])
            return f'{selection_number}. {selection} - {selected_player[0].get_name()}'
    
    def get_availible_players(self) -> str:
        sorted_players = self.sorted_list(self.availible_players)
        returned_string = ''
        for player in sorted_players:
            returned_string += f'\n{player} - Average Draft Position: {player.get_adp()}'
        return returned_string
    
    def __str__(self) -> str:
        string_returned = ''
        for team in self.list_of_teams:
            string_returned += f'\n****************************'
            string_returned += f'\n{team}'
        return string_returned

#Functions For Utilization
def int_selection(valid_answers=set, message=str, error_message=str):
    while True:
        try:
            selection = int(input(message))
            if (selection in valid_answers):
                return selection
            print(f'Selection not availible: {error_message}')
        except ValueError:
            print(f'Invalid Selection: {error_message}')

#Initialization of variables that will be continuously used
file_path = ('text.txt') #change this for where you want your availible selections to show up 
file_path_2 = ('adpsheet.csv') 
number_of_teams = int_selection(set(range(2, 31)), 'What number of teams will you be running? ', 'Your number wasn\'t valid.')
captain_position = int_selection(set(range(1, number_of_teams + 1)), 'What draft position would you want? ', 'Your number wasn\'t valid.')
draft_rounds = int_selection(set(range(5, 11)), 'How many rounds would you like to run? ', 'Your number wasn\'t valid.')

#Data Points to be used
player_names = []
player_position = []
player_selection_history = []

with open(file_path_2, encoding="utf8") as f:
    csv_reader = csv.reader(f)
    for line in csv_reader:
        player_names.append(line[0])
        player_position.append(line[1])
        player_selection_history.append([int(x) for x in line[2:] if len(x) > 0])

#Initial Setup
draft_selections = number_of_teams * draft_rounds
current_selection = 1
total_selections = 1
selection_incrementer = 1
current_round = 1
FIT_THRESHOLD = 0.5
ADDING_THRESHOLD = 1.5
STANDARD_DRAFT = AllTimeDraft(number_of_teams, draft_rounds, draft_selections, [player_names, player_position, player_selection_history])

#The Main Thing
while (current_round <= draft_rounds):
    if (current_selection == 0): #captain_position):
        with open(file_path, 'w') as file:
            file.write(STANDARD_DRAFT.get_availible_players())
        print(STANDARD_DRAFT.find_team(current_selection))
        player_chosen = input(f'Select a player, the whole list of avaiible players is in {file_path}: ')
        while ((STANDARD_DRAFT.find_player(player_chosen)) ==  'Not Found'):
            print(f'Your input, ({player_chosen}), is either taken or not available. Refer to {file_path} for availible players')
            player_chosen =  input(f'Select a player, the whole list of avaiible players is in {file_path}: ')
        print(STANDARD_DRAFT.team_select(STANDARD_DRAFT.find_team(current_selection), STANDARD_DRAFT.find_player(player_chosen), total_selections, current_selection))
    else:
        print(STANDARD_DRAFT.auto_select(current_selection, total_selections))
    total_selections += 1
    current_selection += selection_incrementer
    if (current_selection > number_of_teams):
        selection_incrementer = -1
        current_selection = number_of_teams
        current_round += 1
        if (current_round == 3):
            current_selection = number_of_teams
            selection_incrementer = -1
        print(f'Round {current_round}')
    elif (current_selection == 0):
        selection_incrementer = 1
        current_selection = 1
        current_round += 1
        if (current_round == 3):
            current_selection = number_of_teams
            selection_incrementer = -1
        print(f'Round {current_round}')

print('\nCOMPLETED TEAMS:')
print(STANDARD_DRAFT)