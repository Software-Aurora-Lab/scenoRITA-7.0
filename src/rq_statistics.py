from mylib.stats import effect_size_test, statistical_difference_test

values = """11	16	15	1	0	2
5	8	8	1	0	1
11	31	60	0	0	0
8	11	6	0	0	0
5	5	8	0	0	0
4	3	5	0	0	0
146	215	166	0	0	0
27	7	17	0	0	0
846	740	714	22	20	19
29	80	83	11	5	10
1019	1007	963	23	20	21
73	109	119	12	5	11"""

if __name__ == "__main__":
    for row in values.split("\n"):
        numbers = [float(x) for x in row.split()]
        middle = len(numbers) // 2
        lhs = numbers[:middle]
        rhs = numbers[middle:]
        U1, p = statistical_difference_test(lhs, rhs, verbose=False)
        a12, significance = effect_size_test(lhs, rhs, verbose=False)
        print(f"{p:.3f}\t{a12:.3f}")
