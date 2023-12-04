import regex as re

def partone(lines):
    sum_ = 0
    for line in lines:
        vals = re.findall(r"\d", line)
        line_value = int(vals[0] + vals[-1])
        sum_ += line_value
    print(sum_)
    
def _change_to_digit(value: str, numbers: list[str]):
    if value.isnumeric():
        return value
    return str(numbers.index(value) + 1)
    
def parttwo(lines):
    sum_ = 0
    valid_numbers = ["one", "two", "three", "four", "five", "six", "seven", "eight", "nine"]
    regex_ = "|".join(valid_numbers) 
    regex_ = regex_ + r"|\d"
    for line in lines:
        vals = re.findall(regex_, line, overlapped=True) # ex: twone
        first = _change_to_digit(vals[0], valid_numbers)
        last = _change_to_digit(vals[-1], valid_numbers)
        line_value = int(first + last)
        sum_ += line_value
    print(sum_)
        

if __name__ == "__main__":
    with open("day1/input.txt") as f:
        lines = f.readlines()
    # partone(lines)
    parttwo(lines)
        