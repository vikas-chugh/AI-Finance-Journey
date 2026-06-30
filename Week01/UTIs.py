utis = [
    "UTI001",
    "UTI002",
    "UTI003",
    "UTI002",
    "UTI005",
    "UTI003",
    "UTI007",
    "UTI008",
    "UTI001"
]

# print(set(utis))

# Seen = set(utis)

# for i in Seen:
#     if utis.count(i)>1:
#         print(i)
# seen = set()
# duplicates = set()

for uti in utis:
    if uti in seen:
        duplicates.add(uti)
    else:
        seen.add(uti)

print(duplicates)