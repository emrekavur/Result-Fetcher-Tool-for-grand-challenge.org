
# Result Fetcher Tool for grand-challenge.org

This script collects and saves evaluation scores/values of any challenge hosted on [grand-challenge.org](grand-challenge.org) website. Results are exported as csv files. The tool can be highly modified for specific challenges. Multiple submissions coming from same teams are renamed as "Team Name2", "Team Name3", ... "Team NameN", 

## Usage
The flowing parameters of the challenge should be defined at the beginning of the script. 
 - **url**: Results page of the challenge.
 - **main_key**: The main key under specified task(s). 
 -   **sub_key**: The sub key under specified main key. In general, it defines the metric result or score 
  -  **multitask**: *True* if the challenge has multiple tasks. Otherwise *False*.
  -  **include_empty_tasks**: If it is *False*, the script does not include scores of a task if all cases in the task have *zero* or *None* value. If it is *True*, the script collects everything regardless of the values.
  -  **exclude_key**: (optional) You may define some keys to exclude their values.
  -  **csv_name**: The name of the output file.

Since each challenge has unique result exporting structure, the parameters above are highly specific for the challenges. It is advised to examine JSON tree of the challenge's result by clicking on an arbitrary result. For example, JSON tree structure of CHAOS challenge can be examined via [this link](https://chaos.grand-challenge.org/evaluation/results/9c1281b8-a6e2-44bf-b3b3-ed1167fcfb20/).


## Examples
 There are three example usages of the tool inside the code for [CHAOS](https://chaos.grand-challenge.org/), [SLiver07](https://sliver07.grand-challenge.org/) and [ACDC@LUNGHP](https://acdc-lunghp.grand-challenge.org/) challenges.

1. Parameters for CHAOS challenge to get 'DICE' values for all tasks
```python
url = "https://chaos.grand-challenge.org/evaluation/results/" 
main_key = 'case'
sub_key = 'DICE'
multitask = True
include_empty_tasks = False
exclude_key = 'All_Tasks_Aggregate'
csv_name = 'CHAOS_DICE_values.csv'
```
2. Parameters for SLiver07 challenge to get 'Total_score'
```python
url = "https://sliver07.grand-challenge.org/evaluation/results/"
main_key = 'case'
sub_key = 'Total_score'
multitask = False
include_empty_tasks = False
exclude_key = ''
csv_name = 'SLiver07_scores.csv'
```

3. Parameters for ACDC@LUNGHP challenge to get 'DiceCoefficient' values
```python
url = "https://acdc-lunghp.grand-challenge.org/evaluation/results/"
main_key = 'case'
sub_key = 'DiceCoefficient'
multitask = False
include_empty_tasks = False
exclude_key = ''
csv_name = 'acdc-lunghp_scores.csv'
```

# Required packages: 
The scripts works with Python 3. Also the following packages are needed:
- bs4
- urllib
- re
- pandas
- simplejson

The script was tested on:
```
Python==3.7.4, bs4==0.0.1, urllib3==1.25.3, pandas==0.24.2, simplejson==3.16.0 
```
