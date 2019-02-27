# MQTT
## How to run

1. Get started with broker
```
python broker.py
```

2. Start subscriber 
```
python subscriber.py 
```
then type the input with following format 
```
subscribe  broker_ip_address  'topic_name'
```

3. Start publisher
```
python publisher.py
```
then type the input with following format
```
publish  'broker_ip_address'  'topic_name'  'data to publish'
```

4. If you want to terminate connection type
```
quit
```

### Note:
You can run subscriber and publisher at the same time and
      publisher can publish a message to subscriber several times
      before subscriber terminate the connection
  
    
