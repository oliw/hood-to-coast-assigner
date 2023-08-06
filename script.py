from ortools.sat.python import cp_model
from prettytable import PrettyTable
from course_data import LEGS, SHIFTS

def legs_of_top_n_easiest_shifts(n):
    legs = []
    for shift_legs in sorted(SHIFTS, key = lambda x : x["difficulty"], reverse = False)[:n]:
        legs += shift_legs["legs"]
    return legs

def legs_of_top_n_hardest_shifts(n):
    legs = []
    for shift_legs in sorted(SHIFTS, key = lambda x : x["difficulty"], reverse = True)[:n]:
        legs += shift_legs["legs"]
    return legs

def steepest_n_downhill_legs(n):
    legs = sorted(LEGS, key = lambda x : x["Elevation Loss"], reverse = True)[:n]
    return [x["Leg"] for x in legs]

def steepest_n_uphill_legs(n):
    legs = sorted(LEGS, key = lambda x : x["Elevation Gain"], reverse = True)[:n]
    return [x["Leg"] for x in legs]

people = [
    {
        "name": "Tim",
        "best_buds": [],
        "preferred_legs": [],
        "against_legs": steepest_n_downhill_legs(6) + [36], # downhill
        "preferences_summary": "Avoid too much dewnhill"
    },
    {
        "name": "Kyle",
        "best_buds": ["Oli", "Terence"],
        "preferred_legs": [],
        "against_legs": [], # any,
        "preferences_summary": "No preferences"
    },
    {
        "name": "Terence",
        "best_buds": ["Kyle"],
        "preferred_legs": legs_of_top_n_hardest_shifts(2), # hardest two shifts
        "against_legs": [], # any
        "preferences_summary": "Gimme the hard stuff"
    },
    {
        "name": "Marvin",
        "best_buds": ["Ashok"],
        "preferred_legs": legs_of_top_n_easiest_shifts(4), # lower third
        "against_legs": [],
        "preferences_summary": "Fine with downhill, ideally easier shifts"
    },
    {
        "name": "Melissa",
        "best_buds": ["Jessica"],
        "preferred_legs": [], 
        "against_legs": legs_of_top_n_hardest_shifts(3), # not the hardest
        "preferences_summary": "Not the hardest!"
    },
    {
        "name": "John",
        "best_buds": ["Lucas"],
        "preferred_legs": [], # shortest
        "against_legs": [],
        "preferences_summary": "Fine with hills, but not the longest please"
    },
    {
        "name": "Leah",
        "best_buds": ["Christopher", "Melissa", "Marvin"],
        "preferred_legs": [4,16,28],
        "against_legs": steepest_n_uphill_legs(6), # no uphill
        "preferences_summary": "No uphill, ideally legs 4, 16, 28"
    },
    {
        "name": "Ashok",
        "best_buds": ["Marvin"],
        "preferred_legs": [],
        "against_legs": [6], # against too long and uphill
        "preferences_summary": "Decent shape but would avoid too long a distance and uphill climbs in same leg"
    },
    {
        "name": "Lucas",
        "best_buds": ["John"], #TBA
        "preferred_legs": [],
        "against_legs": [],
        "preferences_summary": "No preferences"
    },
    {
        "name": "Oli",
        "best_buds": ["Kyle"],
        "preferred_legs": [],
        "against_legs": [],
        "preferences_summary": "No preferences"
    },
    {
        "name": "Christopher",
        "best_buds": ["Leah"],
        "preferred_legs": legs_of_top_n_hardest_shifts(2), # pretty good shape
        "against_legs": [],
        "preferences_summary": "Give me the hard stuff"
    },
    
    {
        "name": "Jessica",
        "best_buds": ["Melissa"],
        "preferred_legs": [], # any
        "against_legs": [],
        "preferences_summary": "No preferences aside from the usual haha. 3 am leg not ideal,"
    }
]

def common_member(a, b):
    a_set = set(a)
    b_set = set(b)
    if (a_set & b_set):
        return True
    else:
        return False

# define a class called an Assignment that represents a person being assigned to a shift
class Assignment:
    def __init__(self, person, shift):
        self.person = person
        self.shift = shift
    
    def __str__(self):
        return f'{self.person["name"]} assigned to shift {self.shift["number"]} in van {self.shift["van"]}'


num_shifts = len(SHIFTS)
num_people = len(people)

def j_for_name(name):
    for i in range(len(people)):
        if people[i]["name"] == name:
            return i
    return -1

def shift_details(shift):
    return f'Shift {shift["number"]} - Rank {shift["rank"]} - Van {shift["van"]}'

model = cp_model.CpModel()

# Create the variables
# x[i, j] is an array of 0-1 variables, which will be 1
# if person i is assigned to shift j.

# Job Assigments
x = {}
for i, person in enumerate(people):
    for j, shift in enumerate(SHIFTS):
        x[i, j] = model.NewBoolVar(f'x[{person["name"]},shift-{shift["number"]}]')


# --- Constraints

# Each shift is assigned to exactly one person in the schedule period.
for i, person in enumerate(people):
    model.AddAtMostOne(x[i, j] for j in range(num_shifts))

# Each task is assigned to exactly one worker.
for task in range(num_shifts):
    model.AddExactlyOne(x[person_i, task] for person_i in range(num_people))

# Each person is assigned to tasks matching their van assignment
for i, person in enumerate(people):
    for j, shift in enumerate(SHIFTS):
        van = shift["van"]
        buddy_is = [j_for_name(buddy_name) for buddy_name in person["best_buds"]]
        # get the js of the shifts in different vans
        other_van_shift_js = [j for j in range(len(SHIFTS)) if SHIFTS[j]["van"] != van]
        for buddy_i in buddy_is:
            for shift_j in other_van_shift_js:
                model.Add(x[buddy_i, shift_j] == False).OnlyEnforceIf(x[i, j])
        

# preference_n/a = 2
# preference_yes = 1
# preference_no = 5
# Its the same cost 
costs = []
for i in range(len(people)):
    costs.append([])
    for j in range(len(SHIFTS)):
        cost = 0
        for leg in SHIFTS[j]["legs"]:
            if leg in people[i]["preferred_legs"]:
                cost += 1
            elif leg in people[i]["against_legs"]:
                cost += 10
            else:
                cost += 5
        costs[i].append(cost)


# ---- Objective
objective_terms = []
for i in range(len(people)):
    for j in range(len(SHIFTS)):
        objective_terms.append(costs[i][j] * x[i, j])
model.Minimize(sum(objective_terms))

solver = cp_model.CpSolver()
status = solver.Solve(model)

assignments = []

if status == cp_model.OPTIMAL or status == cp_model.FEASIBLE:
    print(f'Total cost = {solver.ObjectiveValue()}\n')
    for i in range(len(people)):
        for j in range(len(SHIFTS)):
            if solver.BooleanValue(x[i, j]):
                worker = people[i]
                task = SHIFTS[j]
                assignments.append(Assignment(worker, task))
else:
    print('No solution found.')
    exit(0)

# sort assignments by shift number
assignments.sort(key=lambda x: x.shift["number"])

# print assignments as a table with shift number, van number, and person name
t = PrettyTable(['Shift number', 'Van', 'Suggested Person', 'Difficulty (1-hardest)','Legs', 'Prefs', 'Respected Prefs?', 'Leg remarks'], align="l", max_width=50)
for assignment in assignments:
    shift = assignment.shift
    person = assignment.person
    # check if the shift contains any of the person's preferred legs
    respects_preferred_legs = len(person["preferred_legs"]) == 0 or common_member(person["preferred_legs"], shift["legs"])
    respects_avoid_legs = len(person["against_legs"]) == 0 or not common_member(person["against_legs"], shift["legs"])
    respect_remark = "Yes"
    if not respects_avoid_legs:
        respect_remark = "No - Avoided legs not respected"
    elif not respects_preferred_legs:
        respect_remark = "No - Preferred legs not respected"

    legs = shift["legs"]
    leg_remarks = []
    for leg in legs:
        leg_info = next((x for x in LEGS if x["Leg"] == leg), None)
        if leg_info is None:
            leg_remarks.append(f'Leg {leg} not found')
        else:
            leg_remark = f'{leg}-({leg_info["Miles"]})-{leg_info["Remarks"]}'
            leg_remarks.append(leg_remark)
    leg_remarks = '\n'.join(leg_remarks)

    t.add_row([
        shift["number"], 
        shift["van"], 
        person["name"], 
        shift["rank"], 
        ','.join([str(leg) for leg in shift["legs"]]),
        person["preferences_summary"],
        respect_remark,
        leg_remarks
    ])

print(t)

# convert a shifts leg into a comma seperated string
def leg_to_string(leg):
    return ','.join(f'{leg}')