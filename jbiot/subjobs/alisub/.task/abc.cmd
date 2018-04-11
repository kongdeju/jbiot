oss2tools.py mapdown oss://jbiobio/working/tmp
oss2tools.py absdown oss://bio/tmp/hg19.fq
oss2tools.py reldown oss://jbiobio/working/tmp fai
bwa mem -t 4 -R "RG\tiullid" reference /tmp/jbiobio/fq1 fq2
oss2tools.py relup oss://jbiobio/working/tmp test.bam
