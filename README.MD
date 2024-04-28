
## We need db tables for:

####    Example data:
    {
        "pc_name": "LucasComputer",
        "pc_id": "someUniqueIdBasedOnPcMetrics",
        "timestamp": "2024-04-28T11:06:19.134843",
        "data": {
            "cpu": {
                "usage": 21.3
            },
            "ram": {
                "total": 16975147,
                "used": 13172281
            },
            "disk": {
                "kilobytes_read": 0,
                "kilobytes_sent": 73
            },
            "network": {
                "kilobytes_recieved": 1,
                "kilobytes_sent": 0
            }
        }
    }

  
#### Users:
    - user_id
    - username
    - password
    - email


#### Computers:
    - pc_id
    - pc_name
    - user_id

Those are mvp tables, we can add more tables later on, i.e for raporting.

### API Endpoints:
    CPU, RAM, DISK, NETWORK all with filtering based on timestamp, pc_id, user_id. 
    We should be able to fetch data for multiple computers at once.

    Additionaly: 
    - User registration
    - User login
    - Something if we want to expose specific pc data in form of table


###  How to run not **synthetic** data:
    docker compose up
    run producer.py in one terminal 
    run consumer.py in another terminal -> save data from consumer to database.py

But for now we can just save synthetic data from:
    generate_data_recieved_by_server method.
    
