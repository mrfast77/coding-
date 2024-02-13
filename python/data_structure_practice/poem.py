dictionary = {}

with open('poem.txt', 'r') as file:
    for line in file:
        word_list = line.strip(',.\n;:!').split(' ')
        for word in word_list:
            if word in dictionary:
                dictionary[word] += 1
            else:
                dictionary[word] = 1

print(dictionary['I'])

        