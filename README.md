# Artivest Code Test

## 1. Run pip to get dependencies.
## From the top-level directory, run like so:

python solution.py --filename=data.csv --rollup=True

The filename argument is required and points to the csv input to parse.
The rollup argument, if set to true, will output Format 2. If there is no rollup arg or it is set to false, will output Format 1.


**Format 1: Time Series**

Return the data grouped by identifier and sorted by datetime:


```
[
    {
        "identifier": "TSLA",
        "data": [
            [
                "2011-06-21T03:27:34Z",
                925.6532
            ],
            [
                "2013-02-03T09:46:24Z",
                949.8351
            ]
        ]
    },
    {
        "identifier": "GOOG",
        "data": [
            [
                "2007-09-25T05:06:22Z",
                320.3999
            ],
            [
                "2013-02-03T09:46:24Z",
                357.209
            ],
            [
                "2015-01-15T09:51:59Z",
                638.8338
            ]
        ]
    }
]
```

**Format 2: Rolled up with gaps maintained**

Given the following data from the CSV:

| Datetime | Identifier | Value |
| ---------------- | --- | --- |
| 6/21/2014 3:00PM | GOOG | 1 |
| 6/21/2014 4:00PM | TSLA | 3 |
| 6/21/2014 4:30PM | TSLA | 8 |
| 6/21/2014 4:45PM | GOOG | 6 |
| 6/21/2014 5:45PM | TSLA | 2 |

The data listed below would be produced. So if a data point doesn't appear in the rollup up time period (one hour in this case), it should still appear in the output with a 0 as the value:

```
[
    {
        "datetime": "6/21/2014 3:00PM",
        "identifier": "GOOG",
        "value": 1
    },
    {
        "datetime": "6/21/2014 3:00PM",
        "identifier": "TSLA",
        "value": 0
    },
    {
        "datetime": "6/21/2014 4:00PM",
        "identifier": "GOOG",
        "value": 6
    },
    {
        "datetime": "6/21/2014 4:00PM",
        "identifier": "TSLA",
        "value": 11
    },
    {
        "datetime": "6/21/2014 5:00PM",
        "identifier": "GOOG",
        "value": 0
    },
    {
        "datetime": "6/21/2014 5:00PM",
        "identifier": "TSLA",
        "value": 2
    }
    {
        "datetime": "6/21/2014 6:00PM",
        "identifier": "GOOG",
        "value": 0
    },
    {
        "datetime": "6/21/2014 6:00PM",
        "identifier": "TSLA",
        "value": 0
    }
]
```


