from PIL import Image

path = "../encrypted.txt"
my_bytes = bytearray()
byte_packets = []

with open(path, "rb") as file:
    for line in file:
        my_bytes.extend(line[:])

        if len(my_bytes) >= 64:
            byte_packets.append(my_bytes[0:64])
            my_bytes = my_bytes[65:]

reduced = []
for array in byte_packets:
    byte = 0
    for b in array:
        byte = byte << 8 | b

    reduced.append(byte)


all_time_longest = 0
for value in reduced:
    ones = 0
    tested = 0
    run = 0
    longest_run = 0
    for i in range(512):
        if value >> i & 0x01 == 0x01:
            ones += 1
            run += 1
        else:
            if run > longest_run:
                longest_run = run
                if longest_run > all_time_longest:
                    all_time_longest = longest_run
            run = 0
        tested += 1
    print(ones, longest_run)

print(all_time_longest)


out_image = Image.new("RGB", (512, len(byte_packets) - 1))
out_pixels = out_image.load()

for x in range(512):
    for y in range(len(byte_packets) - 1):
        if reduced[y] >> x & 0x01 == 0x01:
            out_pixels[x, y] = (0, 0, 0)
        else:
            out_pixels[x, y] = (255, 255, 255)

out_image.save('bitmap_encrypted.png')

