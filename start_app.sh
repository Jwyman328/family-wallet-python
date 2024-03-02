# start up an electrum server

#set up regtest environment in separate container
source environment.sh
nigiri start
sleep 10 #wait for regtest nigiri to start up
# fund testing address
for value in {1..5} ## changing this number will alter test results.
do
    nigiri faucet bcrt1qkmvk2nadgplmd57ztld8nf8v2yxkzmdvwtjf8s #same address as test_address in env variables.
done
sleep 5 # sleep 5 give nigiri extra start up time before flask run can be run.
flask run -h localhost -p 5011 --reload
