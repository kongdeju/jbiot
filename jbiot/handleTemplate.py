
jbior = "http://www.genescret.com:6636/jbior"

def handleTemplate(rpt):
    
    url = "%s/%s/%s_template.md" % (jbior,rpt,rpt)
    return url



if __name__ == "__main__":
    import sys
    print handleTemplate("qc_report")

