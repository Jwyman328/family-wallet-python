# start up an electrum server

#set up regtest environment in separate container
nigiri start
sleep 10 #wait for regtest nigiri to start up
flask run -h localhost -p 5011
