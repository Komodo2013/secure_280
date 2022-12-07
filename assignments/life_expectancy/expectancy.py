# Uses life-expectancy.csv to
import math


class CountryData:
    """
        This Class is used to store data based on country. It contains functions to aide in saving and accessing data
        add_data: Used to add information to the stored data.
        is_same_country: Used to assure that the country is precisely the same

    """
    def __init__(self, name: str, code: str):
        self.name = name
        self.code = code
        self.data = []

    def add_data(self, year: int, age: float):
        """
            Adds the year:age data point ot this country's data. If this year already exists, it will replace the data
            :param year: Int the year for this life expectancy
            :param age: Int the life expectancy for this year
            :returns self:This object for chaining
        """
        if len(self.data) > 0:
            for i in range(len(self.data)):
                if self.data[i]["year"] == year:
                    self.data[i]["age"] = age
                    return self
        self.data.append({
            "year": year,
            "age": age
        })
        return self

    def is_same_country(self, raw_data: list):
        """
            This function tests if the data from the csv file is a matching country to this one.
            :param raw_data: This is a list of at least two parts: [country_name, country_code]
            :returns: Boolean if the provided list matches this country's name and code
        """
        if self.name in raw_data[0] and self.code in raw_data[1]:
            return True
        return False

    def get_analysis_year(self, year: int):
        """
            This function gets the data from year-10 to year and performs an analysis of the data. It returns a
            dictionary containing min, max, avg, avg_change, and 50_prediction (50 year prediction) values. Both min
            and max are {'year', 'age'} dictionaries
            :param year: int the end year to run the tests on
            :returns: dictionary {'min': {'year', 'age'}, 'max': {'year', 'age'},
                    'avg': float, 'avg_change': float, 50_prediction: float}
        """
        # list to store data we will work with
        analysis_data = []
        # for each stored data point
        for entry in self.data:
            # test if we want this point
            if entry['year'] > year - 10:
                # add it to used data list
                analysis_data.append(entry)

        # checksum if less than 2 data points found do nothing
        if len(analysis_data) < 2:
            return "Insufficient Data"

        # sort list based on year - in theory shouldn't be needed
        sorted(analysis_data, key= lambda x: x['year'])

        # used to store change in expectancy
        differences = []
        # for each data point, find d(age)/dt
        for i in range(len(analysis_data) - 1):
            differences.append((analysis_data[i+1]["age"] - analysis_data[i]["age"]) /
                               (analysis_data[i+1]["year"] - analysis_data[i]["year"]))

        # used to take second derivative of data - in theory more accurate predictions
        accelerations = []
        # for each data point, find d(change of age)/dt
        for i in range(len(differences) - 1):
            accelerations.append((differences[i+1] - differences[i]) /
                                 (analysis_data[i+1]["year"] - analysis_data[i]["year"]))

        # calculate average acceleration of the data
        a_t = sum(accelerations) / len(accelerations)
        # amount of time to predict in the future
        t = 25

        # average change of expectancy
        change_avg = (analysis_data[-1]["age"] - analysis_data[0]["age"]) / \
                     (analysis_data[-1]["year"] - analysis_data[0]["year"])

        # put all ages in list to sum
        ages = []
        for e in analysis_data:
            ages.append(e['age'])

        # data to return
        analysis = {
            "min": analysis_data[0],
            "max": analysis_data[-1],
            "avg": sum(ages)/len(analysis_data),
            "avg_change": change_avg,
            # take the integral as c + v(t) + a(t^2)
            # I use max here as some countries are averaging decline, and result in a negative expected life expectancy
            # max is used to clamp it to the worst point in the last 10 yrs - issue could also have been solved
            # by taking another derivative to get change of a(t), but... I didn't feel like doing that as well...
            "50_prediction": max(analysis_data[-1]["age"] + change_avg * t + a_t * (t ** 2), analysis_data[0]["age"])
        }
        # debug print(a_t, change_avg, analysis_data[-1]["age"])
        return analysis


# Dictionary holding useful format variables. They get changed as you play
# Stored in format int;int;int except when all are 0, which reduces to 0
form = {
    "g": "\x1b[0;92;48m",
    "w": "\x1b[0;97;48m",
    "y": "\x1b[0;93;48m",
    "r": "\x1b[0;91;48m",
    "grey": "\x1b[0;37;48m",
}


def search_year():
    """
        This function gets the average, min, and max from a user prompted year
        :returns: Boolean True to signal to continue the menu loop
    """
    # Loop until we get a valid year, interest is year we are interested in.
    getting = True
    interest = 0
    while getting:
        try:
            interest = int(get_input("What year would you like to learn about?"))
            # Ensure year lies in the interval of provided data
            if yr_min < interest <= yr_max:
                getting = False
            else:
                # Tell them year is not valid and repeat loop
                print(f"{form['y']}Please enter a number between {form['g']}{yr_min}{form['y']} "
                      f"and {form['g']}{yr_max}{form['y']}")
        except ValueError:
            # don't do anything but continue the loop
            pass

    # Min and max life expectancies and their countries go here.
    # Averages is just list of all expectancies - averaged later
    min_ = {"age": math.inf, "country": ""}
    max_ = {"age": -math.inf, "country": ""}
    averages = []

    # Iterate over each entry in each country's data
    for country in d:
        for entry in country.data:
            if entry["year"] == interest:
                if entry["age"] < min_["age"]:
                    min_ = {"age": entry["age"], "country": country.name}
                if entry["age"] > max_["age"]:
                    max_ = {"age": entry["age"], "country": country.name}
                averages.append(entry["age"])

    # Checksum to ensure we don't divide by 0. if len is 0 then that year has no data
    if len(averages) == 0:
        print(f"{form['r']}Error: no data found for year: {form['g']}{interest}{form['w']}")
        return search_year()
    average = sum(averages)/len(averages)

    # Output data to console
    print(f"\nData for the year {form['g']}{interest}{form['w']}:")
    print(f"Minimum life expectancy was {form['g']}{min_['age']:.1f}{form['w']} years in "
          f"{form['g']}{min_['country']}{form['w']}")
    print(f"Maximum life expectancy was {form['g']}{max_['age']:.1f}{form['w']} years in "
          f"{form['g']}{max_['country']}{form['w']}")
    print(f"The average life expectancy was {form['g']}{average:.1f}{form['w']} years.\n")
    return True


def search_country():
    """
        This function gets the average, min, and max from a user prompted country
        :returns: Boolean True to signal to continue the menu loop
    """
    # Loop until we get a valid year, interest is year we are interested in.
    getting = True
    interest = ""
    while getting:
        interest = get_input("What country would you like to learn about?")
        # test if country of interest is in the dataset
        for country in d:
            if country.name in interest:
                getting = False
                break
        if getting:
            # since it isn't, tell user and repeat loop
            print(f"{form['y']}Please enter a valid country")

    # Min and max life expectancies and their countries go here.
    # Averages is just list of all expectancies - averaged later
    min_ = {"age": math.inf, "year": 0}
    max_ = {"age": -math.inf, "year": 0}
    averages = []

    # Iterate over each entry in each country's data
    for country in d:
        if country.name in interest:
            for entry in country.data:
                if entry["age"] < min_["age"]:
                    min_ = {"age": entry["age"], "year": entry["year"]}
                if entry["age"] > max_["age"]:
                    max_ = {"age": entry["age"], "year": entry["year"]}
                if entry["year"] >= 2010:
                    averages.append(entry["age"])

    # Checksum to ensure we don't divide by 0. if len is 0 then that year has no data
    if len(averages) == 0:
        print(f"{form['r']}Error: no data found for country: {form['g']}{interest}{form['w']}")
        return search_country()

    average = sum(averages)/len(averages)

    # Output data to console
    print(f"\nData for the country {form['g']}{interest}{form['w']}:")
    print(f"Minimum life expectancy was {form['g']}{min_['age']:.1f}{form['w']} years in "
          f"{form['g']}{min_['year']}{form['w']}")
    print(f"Maximum life expectancy was {form['g']}{max_['age']:.1f}{form['w']} years in "
          f"{form['g']}{max_['year']}{form['w']}")
    print(f"The average life expectancy of the last 10 years is: {form['g']}{average:.1f}{form['w']} years.\n")
    return True


def analyze_year():
    # Loop until we get a valid year, interest is year we are interested in.
    getting = True
    interest = 0
    while getting:
        try:
            interest = int(get_input("What year would you like to learn about?"))
            # Ensure year lies in the interval of provided data
            if yr_min < interest <= yr_max:
                getting = False
            else:
                # Tell them year is not valid and repeat loop
                print(f"{form['y']}Please enter a number between {form['g']}{yr_min}{form['y']} "
                      f"and {form['g']}{yr_max}{form['y']}")
        except ValueError:
            # don't do anything but continue the loop
            pass

    # world analysis, used to compare and add to
    t_analysis = {
        "min": {"year": 0, "age": math.inf, "name": ""},
        "max": {"year": 0, "age": -math.inf, "name": ""},
        "avg": 0.0,
        "avg_change": 0.0,
        "50_prediction": 0.0
    }

    # because i is deleted after the for loop, and I'm only counting countries I get data from
    j = 0
    for i in range(len(d)):
        a = d[i].get_analysis_year(interest)
        # If insufficient data, skip this country
        if a == "Insufficient Data":
            continue

        j += 1
        # Ignore soft warnings here.... The ide doesn't realize that a['min'] will always be a dictionary
        if a["min"]["age"] < t_analysis["min"]["age"]:
            t_analysis["min"] = {"year": a["min"]["year"], "age": a["min"]["age"], "name": d[i].name}
        if a["max"]["age"] > t_analysis["max"]["age"]:
            t_analysis["max"] = {"year": a["max"]["year"], "age": a["max"]["age"], "name": d[i].name}
        t_analysis["avg"] += a["avg"]
        t_analysis["avg_change"] += a["avg_change"]
        t_analysis["50_prediction"] += a["50_prediction"]

    # take average of the sum by dividing by total number of countries tested - j
    t_analysis["avg"] = t_analysis["avg"] / j
    t_analysis["avg_change"] = t_analysis["avg_change"] / j
    t_analysis["50_prediction"] = t_analysis["50_prediction"] / j

    # output findings
    print(f"\nData for the country {form['g']}The World{form['w']} in: {form['g']}{interest}{form['w']}")
    print(f"Minimum life expectancy of last 10 yrs was {form['g']}{t_analysis['min']['age']:.1f}{form['w']} years in "
          f"{form['g']}{t_analysis['min']['year']}{form['w']} in {form['g']}{t_analysis['min']['name']}{form['w']}")
    print(f"Maximum life expectancy of last 10 yrs was {form['g']}{t_analysis['max']['age']:.1f}{form['w']} years in "
          f"{form['g']}{t_analysis['max']['year']}{form['w']} in {form['g']}{t_analysis['max']['name']}{form['w']}")
    print(f"The average life expectancy of the last 10 years is: {form['g']}{t_analysis['avg']:.1f}{form['w']} years.")
    print(f"The average life expectancy is changing by: {form['g']}{t_analysis['avg_change']:.1f}{form['w']} per year.")
    print(f"According to growth trends, in {form['g']}{interest + 50}{form['w']} the life expectancy will be about: "
          f"{form['g']}{t_analysis['50_prediction']:.1f}{form['w']} years.")
    return True


def analyze_country():
    # Loop until we get a valid year, interest is year we are interested in.
    getting = True
    interest_country = ""
    interest_yr = 0
    analysis = ""
    while getting:
        interest_country = get_input("What country would you like to learn about?")
        # test if country of interest is in the dataset
        for country in d:
            if country.name in interest_country:
                try:
                    interest_yr = int(get_input("What year would you like to learn about?"))
                    # Ensure year lies in the interval of provided data
                    if yr_min < interest_yr <= yr_max:
                        analysis = country.get_analysis_year(interest_yr)
                        if analysis != "Insufficient Data":
                            getting = False
                        else:
                            print(f"{form['r']}Error: Insufficient data{form['w']}")
                    else:
                        # Tell them year is not valid and repeat loop
                        print(f"{form['y']}Please enter a number between {form['g']}{yr_min}{form['y']} "
                              f"and {form['g']}{yr_max}{form['y']}")
                except ValueError:
                    # don't do anything but continue the loop
                    pass
        if getting:
            # since no data found, tell user and repeat loop
            print(f"{form['y']}Please enter a valid country and year")

    # Output data to console
    print(f"\nData for the country {form['g']}{interest_country}{form['w']} in :{form['g']}{interest_yr}{form['w']}")
    # Ignore soft warnings here.... The ide doesn't realize that a['min'] will always be a dictionary
    print(f"Minimum life expectancy of last 10 yrs was {form['g']}{analysis['min']['age']:.1f}{form['w']} years in "
          f"{form['g']}{analysis['min']['year']}{form['w']}")
    print(f"Maximum life expectancy of last 10 yrs was {form['g']}{analysis['max']['age']:.1f}{form['w']} years in "
          f"{form['g']}{analysis['max']['year']}{form['w']}")
    print(f"The average life expectancy of the last 10 years is: {form['g']}{analysis['avg']:.1f}{form['w']} years.")
    print(f"The average life expectancy is changing by: {form['g']}{analysis['avg_change']:.1f}{form['w']} per year.")
    print(f"According to growth trends, in {form['g']}{interest_yr + 50}{form['w']} the life expectancy will be about: "
          f"{form['g']}{analysis['50_prediction']:.1f}{form['w']} years.")
    return True


def exit_func():
    print("Goodbye!")
    return False


# Dictionary holding all menu options. This is place here as teh functions must be defined before they can be
# indexed in the dictionary
# display index: {text: name of menuItem, func: function to run if chosen}
menuItems = {
    "1": {
        "text": "Search by Year",
        "func": search_year
    },
    "2": {
        "text": "Search by Country",
        "func": search_country
    },
    "3": {
        "text": "Analyze Year",
        "func": analyze_year
    },
    "4": {
        "text": "Explore Country Data",
        "func": analyze_country
    },
    "5": {
        "text": "Exit",
        "func": exit_func
    }
}


def get_input(s=""):
    """
        Wrapper of print and input. The format will be s -> _
        :param s: String the text to display before asking for input:
        :returns: String The user's input stripped of whitespace on both sides
    """
    return input(form["w"] + s + "\t\u2192 ").strip()


def serialize_data(path: str, header_rows=1):
    """
        Opens file at path and loads its contents into an array. File should be a csv.
        Expects Entity,Code,Year,Life expectancy (years)
        :param header_rows: Int the number of rows to skip at beginning of file
        :param path: String the path to the file to be parsed
        :returns data: List the list containing data from parsed file
        :returns year_min: Int the smallest year in the dataset
        :returns year_max: Int the largest year in the dataset
    """
    # Variables to be returned.
    data = []
    year_min = math.inf
    year_max = -math.inf

    # counter to output a '.' every nth line parsed
    k = 0
    with open(path) as file:
        print(f"{form['w']}Loading. Please wait.", end="")
        for line in file:
            k += 1
            if (k % 400) == 0:
                print(".", end="")

            # skip the header rows
            if header_rows > 0:
                header_rows -= 1
                continue

            # assume create new country, and prep raw data
            create_new = True
            raw = line.strip().split(",")

            # turn data into numbers... soft warning here, ide just doesn't know it will always get strings of number
            raw[2] = int(raw[2])
            raw[3] = float(raw[3])

            # test if data has any countries in it
            if len(data) > 0:
                # if so test each one to see if it is the same as what we currently have
                for i in range(len(data)):
                    # If it is, don't create a new country, instead just update it
                    if data[i].is_same_country(raw):
                        # soft warning as ide isn't sure raw[2&3] will be numbers
                        data[i].add_data(raw[2], raw[3])
                        create_new = False

            # if we need new country, make it and give it the first data point
            if create_new:
                data.append(CountryData(raw[0], raw[1]))
                data[-1].add_data(raw[2], raw[3])

            # test if this data point sets new boundaries for our data
            if raw[2] < year_min:
                year_min = raw[2]
            elif raw[2] > year_max:
                year_max = raw[2]

            continue

    # new line and return data, as well as boundaries
    print("")
    return data, year_min, year_max


def menu():
    """
        Function run from menu. Displays menu of actions, gets user input and returns the corresponding function
        :returns: Function the function corresponding to the menuItem selected
    """

    listening = True
    while listening:

        # String to put menu in
        menu_text = ""
        # For each menu item
        for i, j in menuItems.items():
            menu_text += f"{i}. {j['text']} \t\t"

        # display menu
        print(menu_text)

        # get the user input
        choice = get_input()
        # iterate through each menu item and test if the number (as string) and
        for i, j in menuItems.items():
            if choice in i:
                # return the driving function for this ch
                return j['func']
    return


# code that runs it all
d, yr_min, yr_max = serialize_data("life-expectancy.csv")
continuing = True
while continuing:
    action = menu()
    continuing = action()
