# Adds numbers inputted until 0, gives average, sum, max, positive least number, repeats sorted list

# Dictionary holding useful format variables. They get changed as you play
# Stored in format int;int;int except when all are 0, which reduces to 0
import math

formats = {
    "green": "\x1b[0;92;48m",
    "white": "\x1b[0;97;48m"
}


# Wrapper of print and set_format
# @param s String message to print to terminal and gets user input
# @returns in String whatever the user typed
def get_input(s=""):
    return input(formats["white"] + s + "\t\u2192 ").strip()


nums = []
print(f"{formats['white']}Enter a list of numbers, type {formats['green']}0{formats['white']} when finished.")

repeat = True
while repeat:
    try:
        num = float(get_input("").strip())
        if num == 0:
            repeat = False
        else:
            nums.append(num)
    except ValueError:
        repeat = False

nums.sort()
sum_ = 0.0
high = 0.0
low_positive = math.inf
print_list = ""

# Calculate width of max number column by multiplying to get max, and taking log10
width = int(math.log(nums[-1], 10)) + 5  # add 5 for decimal and decimal points

for i in range(len(nums)):

    sum_ += nums[i]
    print_list += f"{nums[i]: {width}} "

    if (i + 1) % 10 == 0:
        print_list += "\n"

    high = max(high, nums[i])
    if nums[i] > 0:
        low_positive = min(low_positive, nums[i])


avg = sum_/len(nums)
print(len(nums))
print(f"Sum: {formats['green']}{sum_: 15}{formats['white']} Average: {formats['green']}{avg: 11}\n"
      f"{formats['white']}Largest: {formats['green']}{high: 11}{formats['white']} Small > 0: {formats['green']}"
      f"{low_positive: 9}{formats['white']}\nSorted List: {formats['green']}\n{print_list}")
