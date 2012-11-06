
for every apsara cluster in runtime apsaraClusters:
    1. copy index to apsara cluster, success or failed
    2. user ha2 tool to start service
    3. check start service start success, timeout, failed or success
    4. send several search request to service, check service is normally started.



1.copy index to apsara cluster:

modify destnuwa, dest_pangu_cap in ha2.conf
start yugong copy with ha2 tool
check copy success


2.use ha2 tool to start service

gongcao login to cluster
deploy combo and short configuration if need
run ha2 sts command to start service.


3. check sercie start success.

if service is waiting then
    if timeout then return false
elif service is running then
    if all load success then return true
    if failed or timeout return failed
elif service is failed then
    return failed
 
