import parse
import numpy as np

VAR_ORDER = "xmas"
def parse_rules(rules):
    rule_dict = {}
    for rule in rules:
        key, value = parse.search("{}{{{}}}", rule) # Searches for something like "<0>{<1>}"
        rule_dict[key] = value
    return rule_dict

def parse_objects(objects):
    new_objects = []
    for object_ in objects:
        x, m, a, s = parse.parse("{{x={:d},m={:d},a={:d},s={:d}}}", object_)
        new_objects.append(np.array([x, m, a, s]))
    return new_objects
    

def initial_conditions():
    # in form of (-inf, inf). bounds are always open on either side
    return np.array([[-np.inf, np.inf], [-np.inf, np.inf], [-np.inf, np.inf], [-np.inf, np.inf]])

def parse_conditional_rule(rule: str, current_bounds: np.array):
    """
    Parse a rule in the form of {[xmas][<>][\d]:[(key)]}
    
    return a tuple of accept, reject
    """
    var_, op, value_, branch = parse.parse("{}{}{:d}:{}", rule)
    dimension_to_change = VAR_ORDER.index(var_)
    accept_bounds = current_bounds.copy()
    reject_bounds = current_bounds.copy()
    if op == "<":
        accept_bounds[dimension_to_change, 1] = value_
        reject_bounds[dimension_to_change, 0] = value_ - 1e-2 # Makes it "closed", For example x<2006, reject bounds will include x=2006
    elif op == ">":
        accept_bounds[dimension_to_change, 0] = value_
        reject_bounds[dimension_to_change, 1] = value_ + 1e-2 # Makes it closed, i.e x>2006, reject bounds will include x = 2006
    else:
        raise ValueError("Unknown op: {op}")
    return accept_bounds, reject_bounds, branch

def add_boundaries(bounds, branch, accept_boundaries, reject_boundaries, stack):
    if branch == "A":
        accept_boundaries.append(bounds)
    elif branch == "R":
        reject_boundaries.append(bounds)
    else:
        stack.append((branch, bounds))

def create_boundaries(rule_dict):
    accept_boundaries = []
    reject_boundaries = []
    stack = [("in", initial_conditions())]
    while len(stack):
        current_key, current_bounds = stack.pop()
        ruleset = rule_dict[current_key]
        rules = ruleset.split(",")
        for rule in rules:
            if ":" in rule:
                accept_bounds, reject_bounds, new_branch = parse_conditional_rule(rule, current_bounds)
                current_bounds = reject_bounds
                add_boundaries(accept_bounds, new_branch, accept_boundaries, reject_boundaries, stack)
            else: # Rule is just the branch to go to
                add_boundaries(current_bounds, rule, accept_boundaries, reject_boundaries, stack)

    return accept_boundaries, reject_boundaries

def parse_data(input_file):
    with open(input_file) as f:
        rules, objects = f.read().split("\n\n")
    rules = [rule for rule in rules.split("\n")]
    objects = [object_ for object_ in objects.split("\n")]
    return rules, objects

# vectorizable, but too lazy
def part_one(accept_boundaries, objects):
    accepted_objects = []
    for object_ in objects:
        right_within = (accept_boundaries[:, :, 1] > object_)
        left_within = (accept_boundaries[:, :, 0] < object_)
        accepted = (left_within & right_within)
        if accepted.all(axis=1).any():
            accepted_objects.append(object_)
    
    print(np.stack(accepted_objects).sum())
    
def part_two(accept_boundaries: np.array):
    bounds = np.clip(accept_boundaries, 0.99, 4000.01)
    bounds[:, :, 0] += 1e-4 # add a small thing to make all left bounds closed
    rounded = np.ceil(bounds)
    total = np.prod((rounded[:, :, 1] - rounded[:, :, 0]), axis=1).sum()
    print(total)

if __name__ == "__main__":
    
    rules, objects = parse_data("day19/input.txt") 
    rules = parse_rules(rules)
    objects = parse_objects(objects)
    accept_boundaries, reject_boundaries = create_boundaries(rules)
    accept_boundaries, reject_boundaries = np.stack(accept_boundaries), np.stack(reject_boundaries)
    part_one(accept_boundaries, objects)
    part_two(accept_boundaries)