
# Result Fetcher Tool for grand-challenge.org

This script collects and saves evaluation scores/values of any challenge that publish results via [grand-challenge.org](grand-challenge.org)'s evaluation system. Every evaluated submission at grand-challenge.org is published in JSON format that contains all results for each case in the challenge data. This tool collects this data from the selected challenge for all submissions. Some specifications of this tool are: 

- Results are exported as csv files. 
- Multiple submissions from same teams are automatically renamed as "Team Name2", "Team Name3", ... "Team NameN".
- It is possible to exclude some keys in JSON tree.
- The tool can be highly modified for specific challenges.

Please remember that this is the first version of this tool. There might be some bugs.

## Usage
The following parameters of the challenge should be defined at the beginning of the script. 
 - **url**: Results page of the challenge.
 - **main_key**: The main key under the specified task(s). 
 -   **sub_key**: The subkey under the specified main key. In general, it defines the metric result or score 
  -  **multitask**: *True* if the challenge has multiple tasks. Otherwise *False*.
  -  **include_empty_tasks**: If it is *False*, the script does not include scores of a task if all cases in the task have *zero* or *None* value. If it is *True*, the script collects everything regardless of the values.
  -  **exclude_key**: (optional) You may define some keys to exclude their values.
  -  **csv_name**: The name of the output file.

Since each challenge has a unique result exporting structure, the parameters above are highly specific for the challenges. It is advised to examine the JSON structure of the challenge's result by clicking on an arbitrary result. For example, the JSON tree structure of CHAOS challenge can be examined via [this link](https://chaos.grand-challenge.org/evaluation/results/9c1281b8-a6e2-44bf-b3b3-ed1167fcfb20/).


## Examples
 There are three example usages of the tool for [CHAOS](https://chaos.grand-challenge.org/), [SLiver07](https://sliver07.grand-challenge.org/) and [ACDC@LUNGHP](https://acdc-lunghp.grand-challenge.org/) challenges. (They are also included in the script.)

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
The script works with Python 3. Also the following packages are needed:
- bs4
- urllib
- re
- pandas
- simplejson

The script was tested on:
```
Python==3.7.4, bs4==0.0.1, urllib3==1.25.3, pandas==0.24.2, simplejson==3.16.0 
```
