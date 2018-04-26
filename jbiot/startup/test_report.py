import sys

sys.path.append("../")

from {{projName}}.reporter.report import report

indict = {"yaml":"data/report.yml"}

def test_report():
    report(indict)


if __name__ == "__main__":
    test_report()



