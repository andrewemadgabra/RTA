class GetIndexOfListOftuples:

    def get_index(self, list_of_tuples, search_value, search_index=0):
        for index, tuples in enumerate(list_of_tuples):
            if tuples == search_value:
                return index
        return None
