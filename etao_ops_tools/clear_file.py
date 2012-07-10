
import sys, os
import configuration

if len(sys.argv) < 3:
    print >> sys.stderr, 'Usage: ', sys.argv[0], ' hadoop-dir <file-name>'
    sys.exit(1)

hadoop_dir = sys.argv[1]
hadoop_file = sys.argv[2]
hadoop_rm_cmd = 'hadoop_client/bin/hadoop fs -rm '

comboMap = configuration.Configuration().comboMap
for cluster, dirs in comboMap.items():
    for subdir in dirs:
        print hadoop_rm_cmd + hadoop_dir + '/' + subdir + '/' + hadoop_file
        os.system(hadoop_rm_cmd + hadoop_dir + '/' + subdir + '/' + hadoop_file)







