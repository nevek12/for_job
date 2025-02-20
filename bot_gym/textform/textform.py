

from lexicon.lexicon import TRANSLATION
def formatter(type_training, user_days):
    ans = f'{type_training}\n'
    for day_of_week in user_days:
        string = f'День недели:\n{TRANSLATION[day_of_week].title()} \n'
        for workout, approuch_level in user_days[day_of_week].items():
            lsst = [f'{approuch_level["level"]} уровень', workout, '', '', '', '']
            for i in range(1, int(approuch_level['approuch'])+1):
                temp = "подход " + str(i) + ":"
                shift = 50 - len(lsst[i-1]) - len(temp)

                string += f'{lsst[i-1]}{"-" * shift}{temp}\n'
        ans += string
    return ans

def formatter_train(workout_approuch: dict[str, dict]):
    for workout in workout_approuch:
        for approuch in range(1, int(workout_approuch[workout]['approuch'])+1):
            yield f' {approuch} подходе упражнения \'{workout}\':'



