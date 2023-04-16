from itertools import combinations


class Node:
    def __init__(self, data, positive_child=None, negative_child=None):
        self.data = data
        self.positive_child = positive_child
        self.negative_child = negative_child


class Record:
    def __init__(self, illness, symptoms):
        self.illness = illness
        self.symptoms = symptoms


def parse_data(filepath):
    with open(filepath) as data_file:
        records = []
        for line in data_file:
            words = line.strip().split()
            records.append(Record(words[0], words[1:]))
        return records


class Diagnoser:
    def __init__(self, root: Node):
        self.root = root

    def diagnose(self, symptoms):
        tree_traveler = self.root
        while tree_traveler.positive_child and tree_traveler.negative_child:
            if tree_traveler.data in symptoms:
                tree_traveler = tree_traveler.positive_child
            else:
                tree_traveler = tree_traveler.negative_child
        return tree_traveler.data

    def calculate_success_rate(self, records):
        if len(records) == 0:
            raise ValueError("'records' must contain Record/s")
        success_ratio = 0
        for rec in records:
            diagnosis = self.diagnose(rec.symptoms)
            if diagnosis == rec.illness:
                success_ratio += 1
        ratio = success_ratio / len(records)
        return ratio

    def __all_illnesses_core(self, traveler, illnesses):
        if not traveler or not traveler.data:
            return
        if (not traveler.positive_child) and (not traveler.negative_child) and traveler.data:
            if traveler.data in illnesses:
                illnesses[traveler.data] += 1
            else:
                illnesses[traveler.data] = 1
        self.__all_illnesses_core(traveler.positive_child, illnesses)
        self.__all_illnesses_core(traveler.negative_child, illnesses)

    def all_illnesses(self):
        tree_traveler = self.root
        illnesses = dict()
        self.__all_illnesses_core(tree_traveler, illnesses)
        illnesses = list(sorted(illnesses.items(), key=lambda item: item[1], reverse=True))
        illnesses = [ill[0] for ill in illnesses]
        return illnesses

    def __paths_to_illness_core(self, traveler, illness, lst, result):
        if not traveler:
            return

        if (traveler.data == illness) and (not traveler.positive_child) and (not traveler.negative_child):
            result.append(lst[:])
            return

        lst.append(True)
        self.__paths_to_illness_core(traveler.positive_child, illness, lst, result)
        lst.pop()

        lst.append(False)
        self.__paths_to_illness_core(traveler.negative_child, illness, lst, result)
        lst.pop()

    def paths_to_illness(self, illness):
        traveler = self.root
        all_roads = list()
        self.__paths_to_illness_core(traveler, illness, [], all_roads)
        return all_roads

    def minimize(self, remove_empty=False):
        pass


def _get_most_ill(records):
    if len(records) == 0:
        return None
    illnesses = list()
    counts_ills = dict()

    for rec in records:
        ill = rec.illness
        if ill in illnesses:
            counts_ills[ill] += 1
            continue
        illnesses.append(ill)
        counts_ills[ill] = 1

    illnesses = list(sorted(counts_ills, key=counts_ills.get, reverse=True))
    return illnesses[0]


def _tree_constructor(records, symptoms):
    if len(symptoms) == 0:
        most_ill_data = _get_most_ill(records)
        return Node(most_ill_data)

    in_rec_symptoms = list()
    not_in_rec_symptoms = list()

    for rec in records:
        if symptoms[0] in rec.symptoms:
            in_rec_symptoms.append(rec)
        else:
            not_in_rec_symptoms.append(rec)

    sliced_symptom = symptoms[1:]
    positive_child = _tree_constructor(in_rec_symptoms, sliced_symptom)
    negative_child = _tree_constructor(not_in_rec_symptoms, sliced_symptom)
    return Node(symptoms[0], positive_child, negative_child)


def _params_check_build_tree(records, symptoms):
    for rec in records:
        if type(rec) is not Record:
            raise TypeError("Only 'Record' allowed in list: 'records'")
    for sym in symptoms:
        if type(sym) is not str:
            raise TypeError("Only 'String' allowed in list: 'symptoms'")


def build_tree(records, symptoms):
    _params_check_build_tree(records, symptoms)
    tree_root = _tree_constructor(records, symptoms)
    return Diagnoser(tree_root)


def _params_check_optimal_tree(records, symptoms, depth):
    if not (0 <= depth <= len(symptoms)):
        raise ValueError("'depth' is out of range")

    for symptom in symptoms:
        if symptoms.count(symptom) > 1:
            raise ValueError("Twice or more symptom in 'symptoms'")
        if type(symptom) is not str:
            raise TypeError("Only 'String' allowed in list: 'symptoms'")

    for rec in records:
        if type(rec) is not Record:
            raise TypeError("Only 'Record' allowed in list: 'records'")


def optimal_tree(records, symptoms, depth):
    _params_check_optimal_tree(records, symptoms, depth)
    max_success = (0, "Diagnoser()")

    for combine in combinations(symptoms, depth):
        diag_tree = build_tree(records, combine)
        tree_success = diag_tree.calculate_success_rate(records)
        if tree_success >= max_success[0]:
            max_success = (tree_success, diag_tree)

    return max_success[1]


if __name__ == "__main__":
    #            diagnoser4:
    #                          cough
    #                    Yes /       \ No
    #                  fever        influenza
    #             Yes /     \ No
    #            headache   cold
    #       Yes /     \ No
    #    influenza influenza
    pass
