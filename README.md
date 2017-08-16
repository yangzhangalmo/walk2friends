# walk2friends
This repository provides a reference implementation of *walk2friends* as described in the paper:<br>
> walk2friends: Inferring Social Links from Mobility Profiles. <br>
> Michael Backes, Mathias Humbert, Jun Pang, and Yang Zhang. <br>
> The 24th ACM Conference on Computer and Communications Security (CCS). <br>
> <Insert paper link>

## Basic Usage

### Example
To run inference attack on the New York data with each user having at least 20 check-ins, exucte the following command: <br/>``python src/main_attack.py ny 20``

## Requirements

* pandas
* numpy
* scipy
* scikit-learn

It is recommended to install Anaconda, a python data science distribution, which includes all the above packages.

* gensim
* joblib

## Citing
If you find walk2friends useful in your research, please cite the following paper:
<br>
@inproceedings{BHPZ17,
  author = {Michael Backes and Mathias Humbert and Jun Pang and Yang Zhang},
  title = {node2vec: Scalable Feature Learning for Networks},
  booktitle = {Proc.\ 24th ACM SIGSAC Conference on Computer and Communications Security (CCS)},
  year = {2016},
  publisher = {ACM}
  }
</br>
