import BitUtils
import Posit

def test(name, func, tests):
    print("-" * 10)
    print("Running {} tests for \033[;;1m{}()".format(len(tests), name))
    passed = 0
    failed = []
    
    for i in range(len(tests)):
        if func(*tests[i][0]) == tests[i][1]:
            passed += 1
        else:
            failed.append(i)

    print("\033[1;32m{}\033[0;37m out of {} tests passed".format(passed, len(tests)))
    for i in failed:
        print("\033[1;31mTest {} failed: \033[0;37mInput: {}. Expected: {}. Actual: {}.".format(i, tests[i][0], func(*tests[i][0]), tests[i][1]))

# comprehensive tests
def test_method(name, generator, method, tests):
    print("-" * 10)
    print("Running {} tests for \033[;;1m{}()".format(len(tests), name))
    passed = 0
    failed = []
    for i in range(len(tests)):
        if getattr(generator(*(tests[i][0])), method)() == tests[i][1]:
            passed += 1
        else:
            failed.append(i)

    print("\033[1;32m{}\033[0;37m out of {} tests passed".format(passed, len(tests)))
    for i in failed:
        print("\033[1;31mTest {} failed: \033[0;37mInput: {}. Expected: {}. Actual: {}.".format(i, tests[i][0], getattr(generator(*(tests[i][0])), method)(), tests[i][1]))
    
    print("-" * 10)

# comprehensive tests
def test_operator(name, generator, method, tests):
    print("-" * 10)
    print("Running {} tests for \033[;;1m{}()".format(len(tests), name))
    passed = 0
    failed = []
    for i in range(len(tests)):
        a = generator(*(tests[i][0]))
        b = generator(*(tests[i][1]))
        c = generator(*(tests[i][2]))
        d = getattr(a, method)(b)
        if d == c:
            passed += 1
        else:
            failed.append(i)

    print("\033[1;32m{}\033[0;37m out of {} tests passed".format(passed, len(tests)))
    for i in failed:
        a = generator(*(tests[i][0]))
        b = generator(*(tests[i][1]))
        c = generator(*(tests[i][2]))
        d = getattr(a, method)(b)
        print("\033[1;31mTest {} failed: \033[0;37mInput: {}. Expected: {}. Actual: {}.".format(i, (a,b), c, d))
    
    print("-" * 10)


def make_posit_from_bit_pattern(es, bit_pattern):
    p = Posit.Posit(len(bit_pattern), es)
    p.set_bit_pattern(bit_pattern)
    return p


test("lastSetBit", BitUtils.lastSetBit, [
    ((int("1", 2),), 0),
    ((int("110", 2),), 2),
    ((int("1101010", 2),), 6),
    ((int("100101000", 2),), 8),
])
test("lastUnsetBit", BitUtils.lastUnsetBit, [
    ((int("1", 2),), -1),
    ((int("110", 2),), 0),
    ((int("1101010", 2),), 4),
    ((int("100101000", 2),), 7),
])
test("ceilLog2", BitUtils.ceilLog2, [
    ((4,), 2),
    ((5,), 3),
    ((7,), 3),
    ((17,), 5),
])
test("removeTrailingZeroes", BitUtils.removeTrailingZeroes, [
    ((int("111000000", 2),), int("111", 2)),
    ((int("111000100", 2),), int("1110001", 2))
])
test("align", BitUtils.align, [
     ((int("1", 2), int("10", 2)), (int("1", 2), int("1", 2))),
     ((int("1000", 2), int("1001000", 2)), (int("1000", 2), int("1001", 2))),
     ((int("1000000010101", 2), int("1001000", 2)), (int("1000000010101", 2), int("1001000000000", 2))),
])

test_method("Posit.decode", make_posit_from_bit_pattern, "decode", [
    ((3, "0111111001001111"), (0, 5, 2, 47)), 
    ((4, "0000001010101100"), (0, -5, 5, 11)),
    ((4, "0111110100"), (0, 4, 8, 1)),
    ((8, "0111110"), (0, 4, 0, 1)),
    ((8, "0000000"), None),
    ((8, "1000000"), None)
])

test_operator("Posit.__add__", make_posit_from_bit_pattern, "__add__", [
    ((1, "00001011"), (1, "00001111"), (1, "00010010")), 
    ((1, "00000010"), (1, "00000011"), (1, "00000100")),
])