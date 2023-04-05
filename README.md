# Autodiff Using Computational Graphs 

Code for the project
<br/>
[[This is a makeshift README file. Please treat it as a placeholder and a way to track changes, updates, and todos for the project]]

## Setting up the Environment 
### Conda
1. Clone the repo.
```bash 
conda env create -f environment.yaml
``` 
2. Activate the environment using `conda activate ENVNAME` (which is taenv by default).


### pip / virtualenv
- Use `scripts/create_env_files.py` with the flag `--manager` set to 'pip' to generate a requirements.txt file. The following code will install all the dependencies in your `virtualenv` (**Note:** you will have to create it first).
```bash
python scripts/create_env_files.py --manager pip
pip install -r requirements.txt
```

## Contributing

Pull requests are welcome. For major changes, please open an issue first
to discuss what you would like to change.

Please make sure to update tests as appropriate.

## License

[GNU-GPL v3,0](https://license.md/wp-content/uploads/2022/06/gpl-3.0.txt) <br/>
OR 
See LICENSE.md

