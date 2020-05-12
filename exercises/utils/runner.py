#!/usr/bin/env python3
"""
Runs the test suite and prints the results to standard output.
It uses the given separator in the following way:

<Separator>
#Tests
<Separator>
#Succeeded Tests
<Separator>
First Error
<Separator>
First Failure
<Separator>
"""
import unittest
import traceback
import sys


def main():
    sep = sys.argv[1]

    try:
        import tests
    except SyntaxError as e:
        test_count = 1
        success_count = 0
        error = '\n'.join(map(str, e, traceback.format_exc()))
        failure = ""
    else:
        suite = unittest.TestLoader().loadTestsFromModule(tests)
        result = unittest.TextTestRunner(verbosity=0).run(suite)

        test_count = result.testsRun
        success_count = test_count - len(result.errors) - len(result.failures)
        try:
            error = '\n'.join(map(str, result.errors[0]))
        except IndexError:
            error = ""

        try:
            failure = '\n'.join(map(str, result.failures[0]))
        except IndexError:
            failure = ""

    print(
        sep
        + str(test_count)
        + sep
        + str(success_count)
        + sep
        + error
        + sep
        + failure
        + sep
    )


if __name__ == "__main__":
    main()