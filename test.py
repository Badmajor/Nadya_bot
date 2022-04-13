from states.ChoiceTime import ChoiceTimeUser, ChoiceTimeAdmin

find = 'ChoiceTimeUser:user_choice_month'

a = ChoiceTimeAdmin.__all_states__
b = (ChoiceTimeAdmin.__all_states_names__, ChoiceTimeUser.__all_states_names__)
qw = find.split(':')[0]
print(b)

for i in b:
    if find in i:
        print(i)
        print(i.index(find))
        if i.index(find):
            print(i[i.index(find)])
            break
        print('Хуй, не индекс')

