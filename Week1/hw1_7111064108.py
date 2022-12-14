# %%
filename = 'assn1_input.txt'
file_text = []
with open(filename,'r') as f:
    for text in f:
        file_text.append(text.rstrip('\n'))

print(file_text[:3])

# %%
integer_list = [int(text) for text in file_text if text.isdigit()]
print(integer_list[:3])

# %%
sorted_int_list = sorted(integer_list, reverse=True)
print(sorted_int_list[:10])

# %%
import math
sum_of_int_list = sum(sorted_int_list)
print(f'The sum : {sum_of_int_list}')
ln_of_sum   = math.log(sum_of_int_list)
print(f'ln of sum : {ln_of_sum}')
ln_of_sum_sci_notation = format(ln_of_sum,'.2E')
print(ln_of_sum_sci_notation)

wb_list = [sum_of_int_list,ln_of_sum,ln_of_sum_sci_notation]
wb_list = [str(i) for i in wb_list]

# %%
#Write file to animals.out
# open file in write mode
with open(r'animals.out', 'w') as f:
    f.write(str(sorted_int_list))
    f.write("\n")
    f.write('\n'.join(wb_list))

    print('WB Done')

# %%
# Read in the file
fixed_out = []
with open(filename, 'r') as f:
  for text in f:
    fixed_out.append(text.replace("zerba","zebra").rstrip('\n'))

text_to_check = 'zerba'
print(f'Zerba exist in list? Ans:{text_to_check in fixed_out}')

# %%
#Write file to fixed.out
# open file in write mode
with open(r'fixed.out', 'w') as f:
    for item in fixed_out:
        # write each item on a new line
        f.write("%s\n" % item)

    print('WB Done')

# %%
splited_text = [text.split("%") for text in fixed_out if not text.isdigit()]
print(splited_text[:5])

animals_out = {}

for text in splited_text:
    for animal in text:
        if animal in animals_out:
            animals_out[animal] += 1
        else:
            animals_out[animal] = 1

print(animals_out)

vegetable = ['corn','carrot','tomato']

splited_text = [text.split("%") for text in fixed_out if not text.isdigit() and all(item not in text for item in vegetable)]

print(splited_text[:5])

animals_out = {}

for text in splited_text:
    for animal in text:
        if animal in animals_out:
            animals_out[animal] += 1
        else:
            animals_out[animal] = 1

print(animals_out)

# %%
sum_of_animal = {'total_count': sum(animals_out.values())}
print(sum_of_animal)

# %%
import json
#Write file to fixed.out
# open file in write mode
with open(r'animals.out', 'a+') as f:
    # write each item on a new line
    f.write('\n' + json.dumps(animals_out))
    f.write('\n' + json.dumps(sum_of_animal))

    print('WB Done')
