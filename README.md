# gas-model
Tools for modeling gas of filecoin builtin actor methods

## Repo structure

### Prerequisites / Requirements
1. A running lotus node
2. A python3 installation with the following packages: pandas, sklearn
3. jq installed 

### Repo contents

1. Tools for running gas trace gathering and processing
2. A simple tool for multiple linear regression of vectors
3. A high level script putting things together to demonstrate the flow
4. Example data and intermediate forms used for the [proving deadline cron modeling effort](https://github.com/filecoin-project/FIPs/discussions/761)

### How to generalize

All tools in this repo are tailored for miner proving deadline cron processing. These tools can be forked and tweaked or generalized to handle any type of message gas analysis.  Note that you'll need human in the loop analysis of the structure of filecoin messages to come up with a good decomposition of gas costs in terms of individual messages.  The general flow is:
  1. Gather gas trace summaries of the relevant messages
  2. Look for patterns in these gas costs.  How is gas cost distributed? Are there any outliers?  
  3. Gather data about the state of the actor running the message that can explain different costs.  For proving deadline cron this is done with a lotus shed command parsing deadline, partition, vesting table and precommit queue data.  You could also gather this directly from the gas trace by looking at subcalls.
  4. Iterate between 2 and 3 until you think you can explain most messages gas traces that you inspect in terms of particular variables.
  5. Transform gas traces into a vector, write traces to a csv file.  Spot check that your vectorization is correct by checking csv output against the outputs of gas summaries.  It is important to keep chain epoch and actor address references in vectors for ease of reference.
  6. Run a multilinear regression over your vectors to get gas cost of each variable.  Its possible other models are worth looking into but unlikely.  Gas costs are inherently linear if you keep granularity course enough.  One place you *might* want to explore is taking quadratic terms, for example gas == (HAMT size)*(number of jobs over HAMT).  I suspect this would have explained almost all the variance in the precommit expiry queue for example.
  7. Look at the outliers of your model and iterate from 2 to 6 until you have good enough statistics to be satisfied you're model is explaining reality.  For example in the cron gas model I ended up fitting a model after witholding the 5% of vectors with non zero precommit expiry queues because almost all outliers had big precommit expiry queues.
