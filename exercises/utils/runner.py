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
import sys
import traceback
import unittest


def main():
    sep = sys.argv[1]

    try:
        import tests
    except Exception as e:
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
            error1 = first_error[0]
            error2 = first_error[1]
            error = f"{error1}\n{error2}"
        except IndexError:
            error = ""

        try:
            first_failure = result.failures[0]
            failure1 = first_failure[0]
            failure2 = first_failure[1]
            failure = f"{failure1}\n{failure2}"
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
