"""
Inside conditions.json, you will see a subset of UNSW courses mapped to their
corresponding text conditions. We have slightly modified the text conditions
to make them simpler compared to their original versions.

Your task is to complete the is_unlocked function which helps students determine
if their course can be taken or not.

We will run our hidden tests on your submission and look at your success rate.
We will only test for courses inside conditions.json. We will also look over the
code by eye.

NOTE: This challenge is EXTREMELY hard and we are not expecting anyone to pass all
our tests. In fact, we are not expecting many people to even attempt this.
For complete transparency, this is worth more than the easy challenge.
A good solution is favourable but does not guarantee a spot in Projects because
we will also consider many other criteria.
"""
import json
import re

# NOTE: DO NOT EDIT conditions.json
with open("./conditions.json") as f:
    CONDITIONS = json.load(f)
    f.close()

operators = ["OR", "AND"]

# I didn't do UOC and level stuff


def is_unlocked(courses_list, target_course):
    """Given a list of course codes a student has taken, return true if the target_course
    can be unlocked by them.

    You do not have to do any error checking on the inputs and can assume that
    the target_course always exists inside conditions.json

    You can assume all courses are worth 6 units of credit
    """

    # There are no pre-reqs
    if len(CONDITIONS[target_course]) == 0:
        return True
    # There are pre-reqs, but we are given no courses that are done
    if len(courses_list) == 0:
        return False

    clean_prereqs = ' '.join(CONDITIONS[target_course].split())
    return helper(courses_list, clean_prereqs)


def find_middle_operator(prereqs):
    """Given pre-requisites, find the operator to convert the equation
    into LHS and RHS. The operator must be the first occuring, non-bracket covered
    operator.

    Also find it's count, in case of duplicates - this can be used by
    split() to thus split the correct operator.
    """
    brackets = 0
    operator_count = {}
    operator_split = ""
    operator_pos = 0
    for word in prereqs.split():
        brackets += word.count('(')
        brackets -= word.count(')')
        if word in operators:
            if word in operator_count:
                operator_count[word] += 1
            else:
                operator_count[word] = 1
            operator_split = word
        else:
            operator_split = ""
        if brackets == 0 and operator_split != "":
            operator_pos = operator_count[operator_split]
            break
    return operator_split, operator_pos


def helper(courses_list, prereqs):
    # Only 1 course needed, just check if already done
    if len(prereqs.split()) == 1:
        return prereqs in courses_list
    # Split by middle operator (cannot be enclosed by brackets)
    prereqs = prereqs.upper()
    operator_split, operator_pos = find_middle_operator(prereqs)
    # Length of this should always be 2 ie. LHS and RHS
    sides = prereqs.split(operator_split, operator_pos)
    lhs = sides[0].strip()
    rhs = sides[1].strip()

    # We want to remove outermost brackets for above middle operator logic to work on recursive call
    regex_lhs = re.match(r"^\((.*)\)$", lhs)
    regex_rhs = re.match(r"^\((.*)\)$", rhs)

    if regex_lhs:
        lhs = regex_lhs.group(1)
    if regex_rhs:
        rhs = regex_rhs.group(1)

    # Recursively calculate the subproblems
    lhs_res = helper(courses_list, lhs)
    rhs_res = helper(courses_list, rhs)
    if operator_split == "OR":
        return lhs_res or rhs_res
    elif operator_split == "AND":
        return lhs_res and rhs_res
    else:
        print("Somehow you got here")
        return False


# Custom testing
if __name__ == '__main__':
    print(is_unlocked(["MATH1081", "COMP1511"], "COMP2111"))
