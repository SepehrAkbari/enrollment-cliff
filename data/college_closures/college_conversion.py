import pandas as pd

# Read the text file
with open('college_closures.txt', 'r') as file:
    data = file.readlines()


years = []
names = []
states = []
school_types = []
enrollments = []
reasons = []

for i in range(0, len(data), 5):
    temp = data[i].strip("\n").split(" - ")
    years.append(int(temp[0]))
    temp = temp[1].split(", ")

    names.append(temp[0])
    states.append(temp[1])

    temp = data[i+1].strip("\n").split(": ")

    school_types.append(temp[1])

    temp = data[i+2].strip("\n").split(": ")
    enrollments.append(temp[1])

    temp = data[i+3].strip("\n").split(": ")
    reasons.append(temp[1])

data_dict = {"name":names, "closure year":years, "state":states, "type":school_types, "size":enrollments, "reason for closure":reasons}

df = pd.DataFrame(data_dict)

df.to_csv('college_closures.csv', index=False)
