import sys

sys.path.append("../")

from {{projName}}.reporter.report import report

ymlfile:"data/report.yml"}

def test_report():
    report(ymlfile)


if __name__ == "__main__":
    test_report()



