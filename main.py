from collab import *
from svd import *
from cur import *
import time
import math

start_time = time.time()
#  temporaries: line,s,z,c,x,y
i, a, b = 0, 6040, 3952
#  b = number of rows
#  a = number of columns
z = 0
movie = [0] * b
ratings = [[0 for p in range(a)]for q in range(b)]
# MAIN MATRIX IS MOVIE
f = open("movies.dat", "r")
for line in f.readlines():
    temp = []
    z = 0
    c = 0
    while line[c] != ':':
        z = z * 10
        z = z + int(line[c])
        c += 1
    tempM = z - 1  # movie id
    while line[c] == ':':
        c += 1
    s = ""
    while not (line[c] == ':' and line[c + 1] == ':'):
        s = s + line[c]
        c += 1
    temp.append(s)  # movie name = 0
    while line[c] == ':':
        c += 1
    genre = []
    s = ""
    while line[c] != '\n':
        if line[c] == '|':
            genre.append(s)
            s = ""
            c += 1
        else:
            s = s + line[c]
            c += 1
    genre.append(s)
    temp.append(genre)  # list of genres = 1
    movie[tempM] = temp  # Store (movie name,genre list,ratings list) in movie


f = open("ratings.dat", "r")
count = 1

for line in f.readlines():
    c = 0
    z = 0
    while line[c] != ':':
        z = z * 10
        z = z + int(line[c])
        c += 1
    tempUserId = z - 1  # set uid
    while line[c] == ':':
        c += 1
    z = 0
    while line[c] != ':':
        z = z * 10
        z = z + int(line[c])
        c += 1
    tempMovieId = z - 1  # set mid
    while line[c] == ':':
        c += 1
    z = 0
    while line[c] != ':':
        z = z * 10
        z = z + int(line[c])
        c += 1
    tempRating = z  # set rating
    ratings[tempMovieId][tempUserId] = tempRating

#  sampling out the data to evaluate...
#  setting up base row and base column...
baser = 1252
basec = 3340

#  initialise matrix with direct absolute values from input matrix
ab = [[0 for y in range(2700)]for x in range(2700)]
for x in range(2700):
    for y in range(2700):
        ab[x][y] = ratings[baser + x][basec + y]
        ratings[baser + x][basec + y] = 0

    #
    #
    #
    #
    #
    #  COLLAB FITTING...
    #  start time
print "**COLLABORATIVE"
start_time = time.time()
rmse = 0
count = 0
for x in range(2700):
    for y in range(2700):
        ratings[baser + x][basec + y] = fitting(ratings, baser + x, basec + y, b, a)
        rmse += math.pow(ab[x][y] - ratings[baser + x][basec + y], 2)
        count += 1
    #  rmse
rmse = rmse/count
rmse = math.pow(rmse, 0.5)
print "root mean square error... " + rmse

    #  top k precision

values = []
flag = 0
k = 0
for x in range(2700):
    for y in range(2700):
        if flag == 0:
            #  set rating threshold of 3.5
            if ratings[x][y] > 3.5 and k < 10:
                values.append(ratings[baser + x][basec + y])
                k += 1
            if k == 10:
                flag = 1

        if flag > 0:
            values.sort()
            if values[0] < ratings[baser + x][basec + y]:
                values[0] = ratings[baser + x][basec + y]
            if values[-1] < ratings[baser + x][basec + y]:
                values[-1] = ratings[baser + x][basec + y]

values.sort()
precision = 0
count = 0
for x in range(2700):
    for y in range(2700):
        if (ratings[baser + x][basec + y] > values[0]) and (ratings[baser + x][basec + y] < values[-1]):
            precision += ratings[baser + x][basec + y]/ab[x][y]
            count += 1
precision = precision/count
print "precision at top k... " + precision
    #  spearman correlation
temp3 = 0  #  sum(d**2)
temp4 = 0  #  n
for x in range(2700):
    for y in range(2700):
        if ratings[baser + x][basec + y] > 0:
            temp3 += (ratings[baser + x][basec + y])**2
            temp4 += 1
temp3 = temp3 * 6
temp3 = temp3/(temp4*(temp4**2 - 1))
temp3 = 1 - temp3
print "spearman correlation... " + temp3

print "time elapsed... " + time.time() - start_time


    #
    #
    #  BASELINE COLLAB FITTING...
    #  start time
print "**COLLABORATIVE WITH BASELINE"
start_time = time.time()
    # rmse
rmse = 0
count = 0
for x in range(2700):
    for y in range(2700):
        ratings[baser + x][basec + y] = bfitting(ratings, baser + x, basec + y, b, a)
        rmse += math.pow(ab[x][y] - ratings[baser + x][basec + y], 2)
        count += 1
rmse = rmse / count
rmse = math.pow(rmse, 0.5)
print "root mean square error... " + rmse

    #  top k precision

values = []
flag = 0
k = 0
for x in range(2700):
    for y in range(2700):
        if flag == 0:
                #  set rating threshold of 3.5
            if ratings[x][y] > 3.5 and k < 10:
                values.append(ratings[baser + x][basec + y])
                k += 1
            if k == 10:
                flag = 1

        if flag > 0:
            values.sort()
            if values[0] < ratings[baser + x][basec + y]:
                values[0] = ratings[baser + x][basec + y]
            if values[-1] < ratings[baser + x][basec + y]:
                values[-1] = ratings[baser + x][basec + y]

values.sort()
precision = 0
count = 0
for x in range(2700):
    for y in range(2700):
        if (ratings[baser + x][basec + y] > values[0]) and (ratings[baser + x][basec + y] < values[-1]):
            precision += ratings[baser + x][basec + y] / ab[x][y]
            count += 1
precision = precision / count
print "precision at top k... " + precision
    #  spearman correlation
temp3 = 0  # sum(d**2)
temp4 = 0  # n
for x in range(2700):
    for y in range(2700):
        if ratings[baser + x][basec + y] > 0:
            temp3 += (ratings[baser + x][basec + y]) ** 2
            temp4 += 1
temp3 = temp3 * 6
temp3 = temp3 / (temp4 * (temp4 ** 2 - 1))
temp3 = 1 - temp3
print "spearman correlation... " + temp3

print "time elapsed... " + time.time() - start_time

    


















































