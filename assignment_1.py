class Oil:
    def __init__(self, n1_count, n3_count, n5_count, k_liters, cost, n1_price, n3_price, n5_price, result_file_path):
        self.n1_count = n1_count
        self.n3_count = n3_count
        self.n5_count = n5_count
        self.k_liters = k_liters
        self.cost = cost
        self.n1_price = n1_price
        self.n3_price = n3_price
        self.n5_price = n5_price

        self.__check_data_validity()

        self.bowls = [(5, self.n5_count, self.n5_price),
                      (3, self.n3_count, self.n3_price),
                      (1, self.n1_count, self.n1_price)]

        self.result_file = result_file_path

    def __check_data_validity(self):
        if self.n1_count < 1:
            raise Exception('n1_count value not valid.')

        if self.n5_count > 35:
            raise Exception('n5_count value not valid.')

        if self.k_liters < 1 or self.k_liters > 1000:
            raise Exception('k_liters value not valid.')

        if self.n1_price <= 0 or self.n3_price <= 0 or self.n5_price <= 0:
            raise Exception('Price value not valid.')

    def __calc_bowls_filled(self, liters, with_limit=True):
        bowls_filled = []
        liters_of_oil_left = liters

        for bowl in self.bowls:
            count_of_bowls_used = liters_of_oil_left // bowl[0]
            if with_limit:
                count_of_bowls_used = count_of_bowls_used if bowl[1] > count_of_bowls_used else bowl[1]

            liters_of_oil_left -= count_of_bowls_used * bowl[0]
            bowls_filled.append((bowl[0], count_of_bowls_used))

        return bowls_filled, liters_of_oil_left

    def __calc_bowls_missing(self, bowls_filled):
        bowls_missing = []

        for idx, bowl in enumerate(self.bowls):
            bowls_missing.append((bowl[0], bowl[1] - bowls_filled[idx][1]))

        return bowls_missing

    def __calc_bowls_profit(self, bowls_filled, bowls_needed):
        return sum([(bowls_filled[i][1] + bowls_needed[i][1]) * self.bowls[i][2] for i in range(len(self.bowls))]) - self.cost

    def __bowls_list_to_str(self, bowls):
        return map(lambda x: str(x), list(zip(*bowls))[1][::-1])

    def calculate(self):
        bowls_filled, liters_left = self.__calc_bowls_filled(liters=self.k_liters)
        bowls_missing = self.__calc_bowls_missing(bowls_filled=bowls_filled)
        bowls_needed, liters_left_1 = self.__calc_bowls_filled(liters=liters_left, with_limit=False)
        bowls_profit = self.__calc_bowls_profit(bowls_filled, bowls_needed)

        with open(self.result_file, 'w') as f:
            f.write(' '.join(self.__bowls_list_to_str(bowls_filled)))
            f.write(' ' + str(liters_left) + '\n')
            f.write(' '.join(self.__bowls_list_to_str(bowls_missing)) + '\n')
            f.write(' '.join(self.__bowls_list_to_str(bowls_needed)) + '\n')
            f.write(str(bowls_profit))

    def display(self):
        with open(self.result_file, 'r') as f:
            print(f.read())

    def __repr__(self):
        return """
        n1_count - %s,
        n3_count - %s,
        n5_count - %s,
        k_liters - %s,
        cost - %s,
        n1_price - %s,
        n3_count - %s,
        n5_price - %s
        """ % (self.n1_count,
               self.n3_count,
               self.n5_count,
               self.k_liters,
               self.cost,
               self.n1_price,
               self.n3_price,
               self.n5_price)

    @classmethod
    def from_file(cls, input_file_path, result_file_path):
        with open(input_file_path, 'r') as f:
            first_line_values = map(lambda x: int(x), f.readline().split())
            second_line_values = map(lambda x: int(x), f.readline().split())

            return cls(*first_line_values, *second_line_values, result_file_path)


if __name__ == '__main__':
    oil = Oil.from_file(input_file_path='data/U1_sample_1.txt', result_file_path='data/U1rez.txt')
    print(oil)
    oil.calculate()
    oil.display()

