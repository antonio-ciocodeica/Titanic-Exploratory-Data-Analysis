import sys
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sb
import re

def task_1():
    print("-------------- TASK 1 --------------\n")

    print(f"Number of columns: {nr_columns}\n")
    print(f"Columns data types:\n{train_df.dtypes}\n")
    print(f"Number of missing values for each column:\n{train_df.isnull().sum()}\n")

    print(f"Number of rows: {nr_rows}")
    print(f"Number of duplicate rows: {train_df.duplicated().sum()}\n")


def task_2():
    print("\n-------------- TASK 2 --------------\n")

    # Percentage of survivors
    nr_survived = train_df['Survived'].sum()
    survived_percentage = nr_survived / nr_rows
    print(f"Percentage of people that survived: {survived_percentage : %}")
    print(f"Percentage of people that didn't survive: {1 - survived_percentage : %}\n")

    # Percentage of passengers in each class
    classes = train_df['Pclass']
    unique_classes = np.sort(classes.unique())
    class_count = np.zeros(len(unique_classes) + 1, dtype=int)

    for x in classes:
        class_count[x] += 1

    class_percentage = class_count[1:] / nr_rows
    for x in unique_classes:
        print(f"Class {x}: {class_percentage[x - 1] : %}")

    # Percentage of males and females
    genders = train_df['Sex']
    unique_genders = np.sort(genders.unique())
    genders_count = np.zeros(len(unique_genders), dtype=int)

    for x in genders:
        if x == 'female':
            genders_count[0] += 1
        else:
            genders_count[1] += 1

    genders_percentage = genders_count / nr_rows
    print(f"\nMale percentage: {genders_percentage[1] : %}")
    print(f"Female percentage: {genders_percentage[0] : %}\n")

    # Create plots
    survived_array = [1 - survived_percentage, survived_percentage]
    plt.figure()
    plt.bar(["False", "True"], survived_array)
    plt.xticks(["False", "True"])
    plt.title("Survivors plot")
    plt.ylabel("Percentage")
    plt.xlabel("Survived")
    plt.savefig("../output/task2/Survivors.png")

    plt.figure()
    plt.bar(unique_classes, class_percentage)
    plt.xticks(unique_classes)
    plt.title("Classes plot")
    plt.ylabel("Percentage")
    plt.xlabel("Classes")
    plt.savefig("../output/task2/Classes.png")

    plt.figure()
    plt.bar(unique_genders, genders_percentage)
    plt.title("Genders plot")
    plt.ylabel("Percentage")
    plt.xlabel("Gender")
    plt.savefig('../output/task2/Male-Female.png')


def task_3():
    print("\n-------------- TASK 3 --------------\n")
    print("Histograms added to output/task3 directory.\n")

    # Create histograms for numeric columns
    for column in train_df:
        if column == 'PassengerId':
            continue

        x = train_df[column]
        if x.dtype == int or x.dtype == float:
            plt.figure()
            plt.hist(x, bins=20, edgecolor='black')
            plt.title(f"{column} histogram")
            plt.ylabel("Number of passengers")
            plt.xlabel(column)
            plt.savefig(f"../output/task3/{column}.png")


def task_4():
    print("\n-------------- TASK 4 --------------\n")

    # Identify missing values and show proportion for each column
    for column in train_df:
        x = train_df[column]
        missing_values = x.isnull().sum()

        if missing_values != 0:
            survived_array = [0, 0]
            for i in range(len(x)):
                if pd.isna(x[i]):
                    survived_array[train_df.at[i, 'Survived']] += 1

            print(f"{column}:\nMissing values: {missing_values} out of {nr_rows} => Proportion = {missing_values / nr_rows : .5f}")
            print(f"Did not survive = {survived_array[0]}, Survived = {survived_array[1]}\n")


def task_5():
    if task == 5 or task == 0:
        print("\n-------------- TASK 5 --------------\n")
        print("Added 'AgeCategory' column to the dataframe and created 'AgeCategories' plot in output/task5 directory\n")

    # Add 'AgeCategory' column to classify passengers into age groups
    category = [0, 0, 0, 0, 0]
    ages = train_df['Age']
    train_df.insert(6, 'AgeCategory', 0)

    for i in range(len(ages)):
        if pd.isna(ages[i]):
            category[0] += 1
        elif ages[i] <= 20:
            category[1] += 1
            train_df.at[i, 'AgeCategory'] = 1
        elif ages[i] <= 40:
            category[2] += 1
            train_df.at[i, 'AgeCategory'] = 2
        elif ages[i] <= 60:
            category[3] += 1
            train_df.at[i, 'AgeCategory'] = 3
        else:
            category[4] += 1
            train_df.at[i, 'AgeCategory'] = 4

    # Save new dataframe
    train_df.to_csv("../data/AgeCategory_train.csv", index=False)

    # Plot age categories
    plt.figure()
    plt.title("Age categories")
    plt.ylabel("Number of passengers")
    plt.xlabel("Age category")
    plt.xticks([0, 1, 2, 3, 4])
    plt.bar([0, 1, 2, 3, 4], category)
    plt.savefig("../output/task5/AgeCategories.png")


def task_6():
    print("\n-------------- TASK 6 --------------\n")
    if task == 6:
        task_5()

    # Calculate male survivors by age category
    male_survivors = [0, 0, 0, 0, 0]
    total_males = [0, 0, 0, 0, 0]
    age_categories = train_df['AgeCategory']
    genders = train_df['Sex']
    survivors = train_df['Survived']

    for i in range(nr_rows):
        if genders[i] == 'male':
            total_males[age_categories[i]] += 1
            if survivors[i] == 1:
                male_survivors[age_categories[i]] += 1

    for i in range(len(male_survivors)):
        print(f"Category {i}: {male_survivors[i]} survivors")

    survivors_percentage = [x / y if y != 0 else 0 for x, y in zip(male_survivors, total_males)]

    # Plot male survivors by age category
    plt.figure()
    plt.title("Male survivors by age category")
    plt.ylabel("Percentage of survivors")
    plt.xlabel("Age category")
    plt.xticks([0, 1, 2, 3, 4])
    plt.bar([0, 1, 2, 3, 4], survivors_percentage)
    plt.savefig("../output/task6/MaleSurvivors.png")

    print("'MaleSurvivors' graph added to output/task6 directory\n")

def task_7():
    print("\n-------------- TASK 7 --------------\n")

    # Calculate total children/adults and survivors
    children_count = 0
    children_survivors = 0
    adults_count = 0
    adults_survivors = 0
    known_age_count = 0
    ages = train_df['Age']
    survivors = train_df['Survived']

    for i in range(nr_rows):
        # Ignore unkown ages
        if ages[i] != ages[i]:
            continue
        
        known_age_count += 1
        if ages[i] < 18:
            children_count += 1
            if survivors[i] == 1:
                children_survivors += 1
        else:
            adults_count += 1
            if survivors[i] == 1:
                adults_survivors += 1

    # Compute children/adults surviving percentages
    children_percentage = children_count / known_age_count
    print(f"Percentage of children aboard: {children_percentage : %}\n")

    children_surviving_rate = children_survivors / children_count
    adults_surviving_rate = adults_survivors / adults_count
    print(f"Children survival rate: {children_surviving_rate : 0.4f}")
    print(f"Adult survival rate: {adults_surviving_rate : 0.4f}\n")

    # Plot the results
    plt.figure()
    plt.title("Survival rates")
    plt.ylabel("Survival rate")
    plt.bar(['Children', 'Adults'], [children_surviving_rate, adults_surviving_rate])
    plt.savefig("../output/task7/SurvivalRates.png")

    print("Added 'SurvivalRates' graph to output/task7 directory.\n")

def task_8():
    print("\n-------------- TASK 8 --------------\n")

    # Fill missing values using mean or most frequent value based on 'Survived'
    for column in train_df:
        values = train_df[column]

        if values.isnull().sum() != 0:

            # Group all people based on the 'Survived' column
            survived = [[], []]
            for i in range(nr_rows):
                if values[i] == values[i]:
                    if train_df.at[i, 'Survived'] == 0:
                        survived[0].append(values[i])
                    else:
                        survived[1].append(values[i])


            # Compute the mean for numeric columns, otherwise, take the most frequent value
            if values.dtype == int or values.dtype == float:
                mean_value_0 = round(np.average(survived[0]))
                mean_value_1 = round(np.average(survived[1]))
            else:
                unique_0, count_0 = np.unique(survived[0], return_counts=True)
                mean_value_0 = unique_0[np.argmax(count_0)]
                unique_1, count_1 = np.unique(survived[1], return_counts=True)
                mean_value_1 = unique_1[np.argmax(count_1)]

            # Replace NaN values with the mean value 
            for i in range(nr_rows):
                if train_df.at[i, column] != train_df.at[i, column]:
                    if train_df.at[i, 'Survived'] == 0:
                        train_df.at[i, column] = mean_value_0
                    else:
                        train_df.at[i, column] = mean_value_1
                        
    train_df.to_csv("../data/mean_train.csv", index=False)
    print("Added 'mean_train.csv' to 'data' directory\n")

def task_9():
    print("\n-------------- TASK 9 --------------\n")
    
    # Build dictionaries for male and female titles
    male_dictionary = {}
    female_dictionary = {}

    for i in range(nr_rows):
        name = train_df.at[i, 'Name']
        title = re.findall(r", ([^.]+)\.", name)

        if train_df.at[i, 'Sex'] == 'male':
            if title[0] not in male_dictionary:
                male_dictionary[title[0]] = 1
            else:
                male_dictionary[title[0]] += 1
        else:
            if title[0] not in female_dictionary:
                female_dictionary[title[0]] = 1
            else:
                female_dictionary[title[0]] += 1

    # Print the frequency of each noble title and plot the results
    print(f"Male titles: {male_dictionary}")
    print(f"Female titles: {female_dictionary}\n")
    
    plt.figure()
    plt.title("Male Titles")
    plt.ylabel("Number of passangers")
    plt.xlabel("Title")
    plt.bar(male_dictionary.keys(), male_dictionary.values(), width=0.5)
    plt.savefig("../output/task9/MaleTitles.png")

    plt.figure()
    plt.title("Female Titles")
    plt.ylabel("Number of passangers")
    plt.xlabel("Title")
    plt.bar(female_dictionary.keys(), female_dictionary.values(), width=0.5)
    plt.savefig("../output/task9/FemaleTitles.png")

    print("Added Title repartition graphs to output/task9 directory.")

def task_10():
    print("\n-------------- TASK 10 --------------\n")

    # Create a surname dictionary
    family_dictionary = {}

    for i in range(nr_rows):
        name = train_df.at[i, 'Name']
        family_name = re.findall(".*,", name)
        family_name = family_name[0][:-1]

        if family_name in family_dictionary:
            family_dictionary[family_name] += 1
        else:
            family_dictionary[family_name] = 1

    # Dictionaries for alone/not alone survivors
    survived_not_alone = {True: 0, False: 0}
    survived_alone = {True: 0, False: 0}

    for i in range(nr_rows):
        name = train_df.at[i, 'Name']
        family_name = re.findall(".*,", name)
        family_name = family_name[0][:-1]

        survived = bool(train_df.at[i, 'Survived'])

        if family_dictionary[family_name] == 1:
            survived_alone[survived] += 1
        else:
            survived_not_alone[survived] += 1

    survived = {'Alone': survived_alone, 'Not_Alone': survived_not_alone}

    # Compute and print the surviving percentages for each category
    alone_percentage = survived['Alone'][True] / (survived['Alone'][True] + survived['Alone'][False])
    not_alone_percentage = survived['Not_Alone'][True] / (survived['Not_Alone'][True] + survived['Not_Alone'][False])

    print(f"Percentage of people with no relatives that survived:{alone_percentage : .2%}")
    print(f"Percentage of people with relatives that survived:{not_alone_percentage : .2%}\n")

    percentage = [alone_percentage, not_alone_percentage]

    # Plot the results
    plt.figure()
    plt.title("Percentage of survivors with/without relatives")
    plt.ylabel("Percentage of survivors")
    plt.bar(["Alone", "Not Alone"], percentage, width=0.4)
    plt.savefig("../output/task10/Alone_Survivors.png")

    plt.figure()
    sb.catplot(data=train_df.head(100), x='Pclass', y='Fare', hue='Survived', kind="swarm", s=20, aspect=2)
    plt.savefig("../output/task10/Pclass-Fare.png")

    print("Added 'Pclass-Fare' relation graph to output/task10 directory\n")


if __name__ == "__main__":
    # Read dataframe and determine dimensions
    train_df = pd.read_csv('../input/train.csv')
    nr_columns = len(train_df.columns)
    nr_rows = len(train_df)

    # Determine which task to run (default is all tasks)
    task = 0
    if len(sys.argv) > 1:
        task = int(sys.argv[1])

    if task == 1 or task == 0:
        task_1()
    if task == 2 or task == 0:
        task_2()
    if task == 3 or task == 0:
        task_3()
    if task == 4 or task == 0:
        task_4()
    if task == 5 or task == 0:
        task_5()
    if task == 6 or task == 0:
        task_6()
    if task == 7 or task == 0:
        task_7()
    if task == 8 or task == 0:
        task_8()
    if task == 9 or task == 0:
        task_9()
    if task == 10 or task == 0:
        task_10()