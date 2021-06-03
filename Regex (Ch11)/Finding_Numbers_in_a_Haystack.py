import re

#handle = open('test1.txt')
handle = open('test2.txt')
lst = list()

for lines in handle:
    lines = lines.rstrip()
    nums = re.findall('[0-9]+', lines)

    if len(nums) < 1:
        continue

    for ele in nums:
        temp = float(ele)
        lst.append(temp)

print(sum(lst))
