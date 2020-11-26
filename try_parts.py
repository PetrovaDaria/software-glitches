from parallel_processing import get_indices, get_arr_parts

arr = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14]
parts_count = 4
indices = get_indices(len(arr), parts_count)
print(indices)
parts = get_arr_parts(arr, indices)
print(parts)