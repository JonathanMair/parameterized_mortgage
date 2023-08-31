# Parameterized Mortgage

A package to provide an easily vizualizable mortgage class, built on the Holoviz Param and Panel packages.


## Installation 

Install the package using pip:

`pip install parameterized_mortgage`

Import the Mortgage class:

`from parameterized_mortgage import Mortgage`

## Demo

The package includes a demo dashboard application to show how the Mortgage class can be embedded in visualizations using holoviz panel. See the code in `parameterized_mortgage.dashboard` to see how this is achieved. 

To run the demo on your own machine, install the package using [pipx](https://pypa.github.io/pipx/installation/) (install pipx if necessary):

`pipx install git+https://github.com/JonathanMair/parameterized_mortgage.git`

The run the following command:

`dashboard`

The panel app will launch and should open automatically in a browser. It will look like this:


![](https://raw.githubusercontent.com/JonathanMair/parameterized_mortgage/main/parameterized_mortgage_demo.png)


## Usage


### Mortgage class constructor and user-set parameters

The Mortgage constructor takes 3 named parameters:

- principal (float): amount initially borrowed
- rate (float): annual interest rate expressed as a %
- term (int): mortgage term in years

e.g.:

`mortgage = Mortgage(principal=300000, rate=4.5, term=20)`

These three parameters can be re-set at any time and all other members will be recalculated automatically as a result. 

e.g.: 

`mortgage.rate = 3.8`

### Other class members

`Mortgage.monthly_payment`: A float representing the value of monthly repayments without rounding

`Mortgage.get_monthly_payment()`: Returns the monthly repayment as a string, formatted to 2 decimal places

`Mortgage.repayment_schedule()`: Returns a pandas DataFrame containing the full repayment schedule or amortization table

`Mortgage.annual_summary()`: Returns a pandas DataFrame containing the repayment schedule summarized by year

`Mortgage.lifetime_summary()`: Returns a pandas DataFrame containing the repayment schedule summarized over the whole lifetime of the mortgage

`Mortgage.custom_widgets()`: Returns dictionary detailing customised widgets for a panel.Param object that will allow the user-set parameters to be incorporated easily in a dashboard

`Mortgage.amortization_chart()`: Returns a plot of the outstanding loan over time

`Mortgage.chart_interest_vs_capital()`: Returns a plot of the interest and capital components of monthly payments over time


## Contributing

Contributions are welcome!

## License

This project is licensed under the GNU GENERAL PUBLIC LICENSE Version 3.


## Disclaimer

This software makes calculations that could be relevant to investment decisions, but it is provided without warranty. Users' attention is drawn to the relevant paragraphs of the licence.

## Change log

- 0.1.5: updated README.md
- 0.1.4: added script entrypoint
- 0.1.3: moved __main__.py with demo cli to module `dashboard`
- 0.1.2: fixed error in param.depends declarations in Mortgage
