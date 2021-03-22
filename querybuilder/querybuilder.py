import warnings


class QueryBuilder:
    _query = {"SELECT": [], "FROM": [], "WHERE": [], "GROUP BY": [], "ORDER BY": [], "LIMIT": -1}
    _parameters = []

    def __del__(self):
        [value.clear() if isinstance(value, list) else -1 for _, value in
         self._query.items()]  # Because the context does not disappear when the request is complete...
        self._parameters.clear()

    def distinct(self):
        if "DISTINCT" not in self._query["SELECT"]: self._query["SELECT"].insert(0, "DISTINCT")

    def select(self, column):
        [self._query["SELECT"].append(col) for col in column] if isinstance(column, list) else self._query["SELECT"].append(column)

    def join(self, join_type: str, table: str, on=None):
        if not on and " ON " not in table.upper():
            raise ValueError("You have to merge on something, please add an ON statement or add the ON statement to the table value.")
        self._query["FROM"].append(join_type + table + "" if not on else (" ON " + on))

    def inner_join(self, table: str, on=None):
        self.join("INNER JOIN", table, on)

    def left_join(self, table: str, on=None):
        self.join("LEFT JOIN", table, on)

    def right_join(self, table: str, on=None):
        self.join("RIGHT JOIN", table, on)

    def from_table(self, table):
        if not self._query["FROM"] or " ON " in self._query["FROM"][0]:
            self._query["FROM"].insert(0, table)
        elif self._query["FROM"][0] == table:
            self._query["FROM"].append("," + table)
            warnings.warn("You are performing a self join.")
        else:
            raise ValueError("You must use a join to add additional tables.")

    def where(self, clause):
        # TODO: Split this and make an 'and' and an 'or' method.
        [self._query["WHERE"].append(("" if len(self._query["WHERE"]) > 0 else "AND ") + cla) for cla in clause]\
            if isinstance(clause, list) else self._query["WHERE"].append(("" if len(self._query["WHERE"]) > 0 else "AND ") + clause)

    def group_by(self, column):
        [self._query["GROUP BY"].append(col) for col in column] if isinstance(column, list) else self._query["GROUP BY"].append(column)

    def order_by(self, column):
        [self._query['ORDER BY'].append(col) for col in column] if isinstance(column, list) else self._query['ORDER BY'].append(column)

    def limit(self, count: int):
        self._query['LIMIT'] = count

    @property
    def query(self) -> str:
        """Generates a composed query.

        Right now it's just an SQLite query but I want to add in a return for different databases.

        Returns:
             A string SQL query.
        """
        parts = ["SELECT " + (", ".join(self._query['SELECT'])).replace("DISTINCT,", "DISTINCT"),
                 "FROM " + ("\n".join(self._query['FROM'])),
                 ("WHERE " + ("\n".join(self._query['WHERE']))) if self._query['WHERE'] else "",
                 ("GROUP BY " + (", ".join(self._query['GROUP BY']))) if self._query['GROUP BY'] else "",
                 ("ORDER BY " + (", ".join(self._query['ORDER BY']))) if self._query['ORDER BY'] else "",
                 ("LIMIT " + str(self._query['LIMIT'])) if self._query['LIMIT'] != -1 else ""]
        return "\n".join([x for x in parts if x != ""])