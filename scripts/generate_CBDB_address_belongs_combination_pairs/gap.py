import pandas as pd
import re

def rstrip_word(string, word):   
    return re.sub(f'{word}$', '', string)

# addr_upper + addr_lower
def combine_addr(addr_upper, addr_lower):
	if len(addr_lower) <=1 or len(addr_upper) <=1:
		return None
	# skip dynasty names
	if addr_upper[-1]=="朝" or addr_lower[-1] == "朝":
		return None
	if addr_lower != addr_upper:
		return [addr_upper+belongs_lower, addr_upper, belongs_lower]
	else:
		return None

def remove_duplicates(arr):
    return list(set(tuple(row) for row in arr))

def write_list_to_csv(list_, file_name):
    df = pd.DataFrame(list_)
    df.to_csv(file_name, index=False, header=False)

output = []

# belongs_list = pd.read_excel('input/ADDR_BELONGS_DATA_small.xlsx').values.tolist()
belongs_list = pd.read_excel('input/ADDR_BELONGS_DATA.xlsx').values.tolist()
belongs_list = [i[:2] for i in belongs_list if (i[0] != 0 and i[1] != 0)]
addr_list = pd.read_excel('input/ADDR_CODES.xlsx').values.tolist()
addr_id_to_name_dict = {i[0]: i[2] for i in addr_list}
addr_type_list = [i[0] for i in pd.read_csv('input/cbdb_entity_address_types.csv').values.tolist()[1:]]

# 1. addr_upper + addr_lower
for belongs_row in belongs_list:
	if (belongs_row[0] not in addr_id_to_name_dict) or (belongs_row[1] not in addr_id_to_name_dict):
		continue
	else:
		belongs_lower = addr_id_to_name_dict[belongs_row[0]]
		belongs_upper = addr_id_to_name_dict[belongs_row[1]]
		combined_list = combine_addr(belongs_upper, belongs_lower)
		if combined_list != None:
			output.append(combined_list)

# 2. addr_upper + addr_lower_shorter
for belongs_row in belongs_list:
	if (belongs_row[0] not in addr_id_to_name_dict) or (belongs_row[1] not in addr_id_to_name_dict):
		continue
	else:
		belongs_lower = addr_id_to_name_dict[belongs_row[0]]
		belongs_upper = addr_id_to_name_dict[belongs_row[1]]
		for addr_type_row in addr_type_list:
			belongs_lower_shorter = rstrip_word(belongs_lower,addr_type_row)
			combined_list = combine_addr(belongs_upper, belongs_lower_shorter)
			if combined_list != None:
				output.append(combined_list)
				break

# 3. addr_upper_shorter + addr_lower
for belongs_row in belongs_list:
	if (belongs_row[0] not in addr_id_to_name_dict) or (belongs_row[1] not in addr_id_to_name_dict):
		continue
	else:
		belongs_lower = addr_id_to_name_dict[belongs_row[0]]
		belongs_upper = addr_id_to_name_dict[belongs_row[1]]
		for addr_type_row in addr_type_list:
			belongs_upper_shorter = rstrip_word(belongs_upper,addr_type_row)
			combined_list = combine_addr(belongs_upper_shorter, belongs_lower)
			if combined_list != None:
				output.append(combined_list)
				break
# 4. addr_upper_shorter + addr_lower_shorter
for belongs_row in belongs_list:
	if (belongs_row[0] not in addr_id_to_name_dict) or (belongs_row[1] not in addr_id_to_name_dict):
		continue
	else:
		belongs_lower = addr_id_to_name_dict[belongs_row[0]]
		belongs_upper = addr_id_to_name_dict[belongs_row[1]]
		for addr_type_row in addr_type_list:
			belongs_upper_shorter = rstrip_word(belongs_upper,addr_type_row)
			for addr_type_row in addr_type_list:
				belongs_lower_shorter = rstrip_word(belongs_lower,addr_type_row)
				combined_list = combine_addr(belongs_upper_shorter, belongs_lower_shorter)
				if combined_list != None:
					output.append(combined_list)
					break

# 5. remove possible duplicates
output = remove_duplicates(output)

# 6. sort by length of address name combinations
sorted_output = sorted(output, key=lambda x: len(x[0]), reverse=True)

# 7. write to csv
write_list_to_csv(sorted_output, 'cbdb_address_belongs_combination_pairs.csv')

# 8. print finished
print("Finished!")
