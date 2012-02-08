# A script for creating wholly unique groups of students -- groups where no student in the group has previously worked with any other student in the group
# Algorithm is both fairly stupid and not deterministic; for highly constrained data sets, you may have to run it multiple times before it will find a full solution.
# Fortunately, it tells you when it stalls / won't find a full solution this run.

# Can be run from the command line as 'python grouping-script.py'.

import random

# expected data format is a dictionary of lists
# 'students' --> list of students (strings)
# 'projects' --> list of project names
# 'project_name' -> list of lists, where each interior list is a group of students who worked together for that project

# here's some sample data:
data = { 
'students' : ['alison', 'andy', 'anne', 'bridget', 'bobby', 'devinder',  'donald', 'ellie', 'emmeline', 'gary', 'george', 'gunnar', 'kamran', 'indira' ,'jane', 'marco', 'nestor', 'remy', 'shaun', 'zoe'], 

'projects': ['project_1', 'project_2', 'project_3'],

'project_1' : [['bobby', 'emmeline', 'anne'],
['andy','gunnar'],
['bridget','donald'],
['george','indira','marco','alison'],
['gary','zoe'],
['shaun','ellie','jane'],
['nestor','kamran'],
['remy','devinder'],], 

'project_2' : [['shaun','alison'],
['george','bridget','jane'],
['zoe','indira'],
['bobby','kamran','marco'], 
['nestor','gary'],
['andy','ellie','anne','remy'],
['devinder','emmeline','gunnar','donald']],

'project_3' : [['remy','indira','emmeline'],
['bobby','bridget','nestor'],
['ellie','jane'],
['devinder','alison','gary'],
['shaun','george','gunnar'],
['marco','andy','anne'],
['zoe','donald','kamran']]
}

students_list = data['students']
random.shuffle(students_list)
projects_list = data['projects']
groups = []
group_size = 3

def main():
    '''Outputs a list of entirely novel, semi-random groups based on the student data, and/or returns an unprocessable remainder'''
    print "New groups: "
    while len(students_list) > group_size:
        root_student = students_list.pop(0)
        make_group([root_student])
    
    # deal with the remaining students
    counter = 0
    while len(students_list) > 0 or counter < len(data['students']) * group_size:
        student = students_list[0]
        for group in groups:
            if new_to_group(student, group) and len(group) < group_size + 1:
                if student in students_list:
                    students_list.remove(student)
                    group.append(student)
                continue
        counter = counter + 1
    
    # print groups
    for group in groups:
        print "Group: " + serial(group)
    
    # if necessary, print remainder
    if students_list:
        print "Remainder: " + serial(students_list)

def make_group(current_group, counter=0):
    '''Recursively creates a group of size group_size, by adding a new member (chosen randomly) once at a time and checking if they've worked with any of the group members previously. If it runs out of tries, will print out a message saying it stalled, and giving the remainder.'''
    if len(current_group) == group_size:
        groups.append(current_group)
    elif counter > 15 or len(students_list) < 1:
        print 'Stalled on group [' + serial(current_group) + '] with remainder [' + serial(students_list) + ']'
    else:
        index = random.randint(0, len(students_list)-1)
        new_student = students_list[index]
        if new_to_group(new_student,current_group):
            current_group.append(new_student)
            students_list.pop(index)
            make_group(current_group,counter)
        else:
            make_group(current_group,counter+1)
        
def new_to_group(new_student, group):
    '''Checks if a given student has worked with any of the members of a given group before'''
    is_new = True
    for student in group:
        if have_worked_together(student, new_student):
            is_new = False
            break
    return is_new
        
def have_worked_together(student1, student2):
    '''Takes two students, returns True if they've worked together in the past'''
    fact = False
    # if any loop through returns True, fact will become True
    for project_name in projects_list:
        fact = fact or work_together_helper(data[project_name], student1, student2)
    return fact
    
def work_together_helper(project, student1, student2):
    for team in project:
        if student1 in team and student2 in team:
            return True
    return False
    
def has_worked_with(student):
    '''Returns a list of people that a given student has worked with in the past, checking for repeats'''
    # Not called by the main function in any way, but useful for testing/checking results
    # dictionary is for performance / ease of lookup; kind of silly
    worked_with_dico = {}
    worked_with_list = []
    for project_name in projects_list:
        for team in data[project_name]:
            if student not in team:
                continue
            for person in team:
                if person != student and not person in worked_with_dico:
                    worked_with_list.append(person)
                    worked_with_dico[person] = 1
    return worked_with_list
    
def serial(list):
    '''Takes either a string or a list of strings; if it's a string, returns the string, if it's a list, turns it into a comma-delineated string'''
    if type(list) == str:
        return list
    elif list:
        return ', '.join(list)
    else:
        raise ValueError
        
if __name__ == '__main__':
    main()
