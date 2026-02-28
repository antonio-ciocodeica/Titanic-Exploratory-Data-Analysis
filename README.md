# Titanic Exploratory Data Analysis

This project performs an **exploratory data analysis (EDA)** on the `train.csv` dataset (Titanic passengers) using **Python** and the following libraries:

- [Pandas](https://pandas.pydata.org) – data manipulation and analysis  
- [NumPy](https://numpy.org) – numerical operations  
- [Matplotlib](https://matplotlib.org) – data visualization  
- [Seaborn](https://seaborn.pydata.org) – statistical visualizations  

---

## Objectives

1. Inspect the dataset structure and identify missing values or duplicate rows.  
2. Determine the survival rate and distribution of passengers by class and gender.  
3. Generate histograms for numeric columns.  
4. Analyze missing values based on survival status.  
5. Create an `AgeCategory` column and visualize passenger distribution by age group.  
6. Analyze male survival rates by age category.  
7. Compare survival rates between children and adults.  
8. Fill missing values using the mean or most frequent value depending on survival.  
9. Analyze passenger titles (e.g., Mr, Mrs) and their distribution by gender.  
10. Examine survival rates for passengers traveling alone vs. with family and analyze the relationship between class, fare, and survival.

---

## Project Structure

```plaintext
/
├── input/
│   └── train.csv           # Original dataset
├── output/
│   ├── task2/              # Task 2: survival, class, and gender plots
│   ├── task3/              # Task 3: histograms of numeric columns
│   ├── task5/              # Task 5: age category plot
│   ├── task6/              # Task 6: male survivors by age category
│   ├── task7/              # Task 7: survival rates for children vs. adults
│   ├── task9/              # Task 9: title distribution plots
│   └── task10/             # Task 10: survivors alone vs. with family
├── data/
│   ├── AgeCategory_train.csv
│   └── mean_train.csv
├── src/
│   └── main.py             # Main analysis script
└── README.md               # Project documentation
```

---

## Installation and Usage

1. **Clone the repository:**

```bash
git clone https://github.com/antonio-ciocodeica/Titanic-Exploratory-Data-Analysis
cd Titanic-Exploratory-Data-Analysis
```

2. **Create and activate a virtual environment** (recommended)

- On Linux
```bash
python3 -m venv venv
source venv/bin/activate
```

- On Windows
```bash
python3 -m venv venv
venv\Scripts\activate
```

3. **Install the dependencies**
```bash
pip install -r requirements.txt
```

4. **Run the analysis**
```bash
cd src/
python3 analysis.py
```

To run a specific task, provide the task number as an argument. E.g.: To run Task 2 only:

```bash
python3 src/analysis.py 2
```
 