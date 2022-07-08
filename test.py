from datetime import datetime, timedelta


data = [
    {
        "test": {
            "current_track": {
                "id": 100,
                "name": "Current track 1",
                "artist": "Current artist 1"
            },
            "playlist": [
                {
                    "name": "Current track 1",
                    "artist": "Current artist 1",
                    "time": datetime.strftime(datetime.now(), "%Y-%m-%d %H:%M")
                },
                {
                    "name": "Past track 1",
                    "artist": "Past artist 1",
                    "time": datetime.strftime(datetime.now() - timedelta(minutes=3), "%Y-%m-%d %H:%M")
                },
                {
                    "name": "Past track 2",
                    "artist": "Past artist 2",
                    "time": datetime.strftime(datetime.now() - timedelta(minutes=7), "%Y-%m-%d %H:%M")
                },
                {
                    "name": "Past track 3",
                    "artist": "Past artist 3",
                    "time": datetime.strftime(datetime.now() - timedelta(minutes=11), "%Y-%m-%d %H:%M")
                },
            ]
        }
    },
    {
        "test": {
            "current_track": {
                "id": 101,
                "name": "Current track 2",
                "artist": "Current artist 2"
            }
        }
    },
    {
        "test": {
            "current_track": {
                "id": 101,
                "name": "Current track 2",
                "artist": "Current artist 2"
            }
        }
    },
    {
        "test": {
            "current_track": {
                "id": 102,
                "name": "Current track 3",
                "artist": "Current artist 3"
            }
        }
    },
]
