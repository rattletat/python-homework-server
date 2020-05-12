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
        error = str(e) + "\n" + str(traceback.format_exc())
        failure = ""
    else:
        suite = unittest.TestLoader().loadTestsFromModule(tests)
        result = unittest.TextTestRunner(verbosity=0).run(suite)

        test_count = result.testsRun
        success_count = test_count - len(result.errors) - len(result.failures)
        try:
            first_error = result.errors[0]
            error = str(first_error[0]) + '\n' + str(first_error[1])
        except IndexError:
            error = ""

        try:
            first_failure = result.failures[0]
            failure = str(first_failure[0]) + '\n' + str(first_failure[1])
        except IndexError:
            failure = ""

    print(
        sep
        + str(test_count)
        + sep
        + str(success_count)
        + sep
        + error.strip()
        + sep
        + failure.strip()
        + sep
    )


if __name__ == "__main__":
    main()
