# Opens hr_system.txt and then prints data as a pretty list

with open("hr_system.txt") as file:
    for line in file:
        data = line.strip().split()
        for i in range(len(data)):
            if i == 0 or i == 2:
                data[i] = data[i].ljust(10)
        data[3] = float(data[3])/(12 * 2)
        if "Engineer" in data[2]:
            data[3] += 1000
        print(f"{data[0]} (ID: {data[1]}), {data[2]} - ${data[3]:.2f}")
