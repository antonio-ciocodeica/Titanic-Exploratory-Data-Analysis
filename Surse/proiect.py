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

    # Procentul de supravietuitori
    nr_survived = (train_df['Survived']).sum()
    survived_percentage = (nr_survived / nr_rows)
    print(f"Percentage of people that survived: {survived_percentage : %}")
    print(f"Percentage of people that didn't survive: {1 - survived_percentage : %}\n")

    # Procentul pasagerilor din fiecare clasa
    classes = train_df['Pclass']
    unique_classes = classes.unique()
    unique_classes.sort()
    class_count = np.zeros(len(unique_classes) + 1, dtype=int)

    for x in classes:
        class_count[x] += 1

    class_percentage = class_count[1:] / nr_rows

    for x in unique_classes:
        print(f"Class {x}: {class_percentage[x - 1] : %}")

    # Procentul de barbati si de femei
    genders = train_df['Sex']
    unique_genders = genders.unique()
    unique_genders.sort()
    genders_count = np.zeros(len(unique_genders), dtype=int)

    for x in genders:
        if x == 'female':
            genders_count[0] += 1
        else:
            genders_count[1] += 1

    genders_percentage = genders_count / nr_rows

    print(f"\nMale percentage: {genders_percentage[1] : %}")
    print(f"Female percentage: {genders_percentage[0] : %}\n")

    # Realizam graficele pentru reprezentarea rezultatelor
    survived_array = [1 - survived_percentage, survived_percentage]
    plt.figure()
    plt.bar(["False", "True"], survived_array)
    plt.xticks(["False", "True"])
    plt.title("Survivors plot")
    plt.ylabel("Percentage")
    plt.xlabel("Survived")
    plt.savefig("../output/task2/Survivors.png")
    plt.show()

    plt.figure()
    plt.bar(unique_classes, class_percentage)
    plt.xticks(unique_classes)
    plt.title("Classes plot")
    plt.ylabel("Percentage")
    plt.xlabel("Classes")
    plt.savefig("../output/task2/Classes.png")
    plt.show()

    plt.figure()
    plt.bar(unique_genders, genders_percentage)
    plt.title("Genders plot")
    plt.ylabel("Percentage")
    plt.xlabel("Gender")
    plt.savefig('../output/task2/Male-Female.png')
    plt.show()

def task_3():
    print("\n-------------- TASK 3 --------------\n")
    print("Histograms added to output/task3 directory.\n")
    # Pentru fiecare coloana din dataframe, verificam daca aceasta contine
    # valori numerice (int sau float) si construim histogramele.
    for column in train_df:
        x = train_df[column]
        if x.dtype == int or x.dtype == float:
            plt.figure()
            plt.hist(x, bins = 20, edgecolor = 'black')
            plt.title(f"{column} histogram")
            plt.ylabel("Nr. People")
            plt.xlabel(column)
            plt.savefig(f"../output/task3/{column}")
            plt.show()

def task_4():
    print("\n-------------- TASK 4 --------------\n")

    for column in train_df:
        x = train_df[column]
        missing_values = x.isnull().sum()

        if missing_values != 0:
            survived_array = [0, 0]
            for i in range(len(x)):
                if x[i] != x[i]:
                    survived_array[train_df.at[i, 'Survived']] += 1

            print(f"{column}:\nMissing values: {missing_values} out of {nr_rows} => Proportion = {missing_values / nr_rows : .5f}")
            print(f"Did not survive = {survived_array[0]}, Survived = {survived_array[1]}\n")

def task_5():
    if task == 5 or task == 0:
        print("\n-------------- TASK 5 --------------\n")
        print("Added 'AgeCategory' column to the dataframe and created 'AgeCategories' plot in output/task5 directory\n")

    # Initializam o lista care va contine numarul de persoane din fiecare
    # categorie de varsta si adaugam coloana AgeCategory imediat dupa coloana Age.
    # Vom incadra persoanele a caror varsta este necunoscuta in categoria 0.
    category = [0, 0, 0, 0, 0]
    ages = train_df['Age']
    train_df.insert(6, 'AgeCategory', 0)

    # Parcurgem coloana cu varstele, incrementam valoarea corespunzatoare din lista
    # de categorii si actualizam categoria de varsta a persoanei din tabel.
    for i in range(len(ages)):
        if ages[i] != ages[i]:
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

    # Salvam noul dataframe
    train_df.to_csv("../Date/AgeCategory_train.csv", index=False)

    # Realizam graficul pentru a evidentia rezultatele
    plt.figure()
    plt.title("Age categories")
    plt.ylabel("Number of passangers")
    plt.xlabel("Age category")
    plt.xticks([0, 1, 2, 3, 4])
    plt.bar([0, 1, 2, 3, 4], category)
    plt.savefig("../output/task5/AgeCategories.png")
    plt.show()

def task_6():
    print("\n-------------- TASK 6 --------------\n")
    if task == 6:
        task_5()

    # Calculam numarul total de barbati si numarul de supravietuitori
    # in functie de categoria de varsta.
    male_survivors = [0, 0, 0, 0, 0]
    total_males = [0, 0, 0, 0, 0]
    age_categories = train_df['AgeCategory']
    genders = train_df['Sex']
    survivors = train_df['Survived']

    for i in range(nr_rows):
        if genders[i] == 'male':
            total_males[age_categories[i]] += 1
            if survivors[i] == True:
                male_survivors[age_categories[i]] += 1

    # Afisam numarul de supravietuitori din fiecare categorie de varsta
    for i in range(len(male_survivors)):
        print(f"Category {i}: {male_survivors[i]} survivors")

    # Determinam procentul de barbati supravietuitori din fiecare categorie de varsta.
    survivors_percentage = [x/y for x, y in zip(male_survivors, total_males)]

    # Realizam graficul pentru a pune in evidenta modul in care varsta influenteaza
    # procentul de supravietuire al barbatilor
    plt.figure()
    plt.title("Male survivors by age category")
    plt.ylabel("Percentage of survivors")
    plt.xlabel("Age category")
    plt.xticks([0, 1, 2, 3, 4])
    plt.bar([0, 1, 2, 3, 4], survivors_percentage)
    plt.savefig("../output/task6/MaleSurvivors.png")
    plt.show()
    print("'MaleSurvivors' graph added to output/task6 directory\n")

def task_7():
    print("\n-------------- TASK 7 --------------\n")

    # Calculam numarul total de copii si numarul de copii care au supravietuit.
    # Facem acelasi lucru si pentru adulti.
    children_count = 0
    children_survivors = 0
    adults_count = 0
    adults_survivors = 0
    known_age_count = 0
    ages = train_df['Age']
    survivors = train_df['Survived']

    for i in range(nr_rows):
        # Daca ages[i] != ages[i], inseamna ca varsta persoanei
        # este necunoscuta, deci nu o luam in considerare
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

    # Calculam procentul de copii aflati la bord.
    children_percentage = children_count / known_age_count
    print(f"Percentage of children aboard: {children_percentage : %}\n")

    # Calculam rata de supravietuire pentru copii si adulti.
    children_surviving_rate = children_survivors / children_count
    adults_surviving_rate = adults_survivors / adults_count
    print(f"Children survival rate: {children_surviving_rate : 0.4f}")
    print(f"Adult survival rate: {adults_surviving_rate : 0.4f}\n")

    # Realizam graficul care pune in evidenta ratele de supravietuire.
    plt.figure()
    plt.title("Survival rates")
    plt.ylabel("Survival rate")
    plt.bar(['Children', 'Adults'], [children_surviving_rate, adults_surviving_rate])
    plt.savefig("../output/task7/SurvivalRates.png")
    plt.show()
    print("Added 'SurvivalRates' graph to output/task7 directory.\n")

def task_8():
    print("\n-------------- TASK 8 --------------\n")

    # Cautam coloanele care au valori lipsa
    for column in train_df:
        values = train_df[column]

        # Daca am gasit o coloana cu valori lipsa, le vom inlocui cu media
        # valorilor din coloana curenta
        if values.isnull().sum() != 0:

            # Impartim toate persoanele in 2 categorii, in functie de coloana 'Survived'
            survived = [[], []]
            for i in range(nr_rows):
                if values[i] == values[i]:
                    if train_df.at[i, 'Survived'] == 0:
                        survived[0].append(values[i])
                    else:
                        survived[1].append(values[i])


            # Daca valorile sunt numerice, calculam media acestora.
            # Daca valorile nu sunt numerice, o cautam pe cea mai frecventa.
            if values.dtype == int or values.dtype == float:
                mean_value_0 = round(np.average(survived[0]))
                mean_value_1 = round(np.average(survived[1]))
            else:
                unique_0, count_0 = np.unique(survived[0], return_counts=True)
                mean_value_0 = unique_0[np.argmax(count_0)]
                unique_1, count_1 = np.unique(survived[1], return_counts=True)
                mean_value_1 = unique_1[np.argmax(count_1)]

            # Inlocuim toate inregistrarile NaN cu valoarea gasita anterior
            for i in range(nr_rows):
                if train_df.at[i, column] != train_df.at[i, column]:
                    if train_df.at[i, 'Survived'] == 0:
                        train_df.at[i, column] = mean_value_0
                    else:
                        train_df.at[i, column] = mean_value_1
                        
    train_df.to_csv("../Date/mean_train.csv", index=False)
    print("Added 'mean_train.csv' to Date directory\n")

def task_9():
    print("\n-------------- TASK 9 --------------\n")
    
    # Iteram prin setul de antrenament si construim 2 dictionare care vor
    # contine titlurile de noblete ale pasagerilor
    male_dictionary = {}
    female_dictionary = {}

    for i in range(nr_rows):
        name = train_df.at[i, 'Name']
        title = re.findall(", ([^\.]+)\.", name)

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

    # Afisam titlurile impreuna cu numarul de aparitii
    print(f"Male titles: {male_dictionary}")
    print(f"Female titles: {female_dictionary}\n")

    # Reprezentam grafic repartitia titlurilor de noblete
    plt.figure()
    plt.title("Male Titles")
    plt.ylabel("Number of passangers")
    plt.xlabel("Title")
    plt.bar(male_dictionary.keys(), male_dictionary.values(), width=0.5)
    plt.savefig("../output/task9/MaleTitles.png")
    plt.show()

    plt.figure()
    plt.title("Female Titles")
    plt.ylabel("Number of passangers")
    plt.xlabel("Title")
    plt.bar(female_dictionary.keys(), female_dictionary.values(), width=0.5)
    plt.savefig("../output/task9/FemaleTitles.png")
    plt.show()

    print("Added Title repartition graphs to output/task9 directory.")

def task_10():
    print("\n-------------- TASK 10 --------------\n")

    # Construim un dictionar care contine toate numele de familie
    # impreuna cu numarul de aparitii al acestora.
    family_dictionary = {}

    for i in range(nr_rows):
        name = train_df.at[i, 'Name']
        family_name = re.findall(".*,", name)
        family_name = family_name[0][:-1]

        if family_name in family_dictionary:
            family_dictionary[family_name] += 1
        else:
            family_dictionary[family_name] = 1

    # Construim 2 dictionare pentru a calcula numarul de
    # supravietuitori cu rude, respectiv fara rude.
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

    # Calculam procentul de supravietuitori din cele 2 categorii.
    alone_percentage = survived['Alone'][True] / (survived['Alone'][True] + survived['Alone'][False])
    not_alone_percentage = survived['Not_Alone'][True] / (survived['Not_Alone'][True] + survived['Not_Alone'][False])

    print(f"Percentage of people with no relatives that survived:{alone_percentage : .2%}")
    print(f"Percentage of people with relatives that survived:{not_alone_percentage : .2%}\n")

    percentage = [alone_percentage, not_alone_percentage]

    plt.figure()
    plt.title("Percentage of survivors with/without relatives")
    plt.ylabel("Percentage of survivors")
    plt.bar(["Alone", "Not Alone"], percentage, width=0.4)
    plt.savefig("../output/task10/Alone_Survivors.png")
    plt.show()

    # Realizam graficul pentru a pune in evidenta relatia dintre tarif, clasa.
    # si starea de supravietuire a primelor 100 de inregistrari din train.csv.
    plt.figure()
    sb.catplot(data=train_df.head(100), x='Pclass', y='Fare', hue='Survived', kind="swarm", s=20, aspect=2)
    plt.savefig("../output/task10/Pclass-Fare.png")
    plt.show()
    print("Added 'Pclass-Fare' relation graph to output/task10 directory\n")


# Citim dataframe-ul din fisier si determinam numarul de linii si coloane.
train_df = pd.read_csv('../input/train.csv')
nr_columns = len(train_df.axes[1])
nr_rows = len(train_df.axes[0])

# Determinam ce task vrem sa rulam.
# Daca nu se specifica un task, se vor rula toate.
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