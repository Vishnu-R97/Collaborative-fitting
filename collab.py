
def fitting(clb, i, j, r, c):  # run collaborative fitting
    #  temporaries: a,b,k,l,x,y
    lis = []
    #  copy onto ctemp
    ctemp = [[0 for y in range(c)] for x in range(r)]
    for x in range(r):
        for y in range(c):
            ctemp[x][y] = clb[x][y]

    # take out items that have been rated by user j
    for k in range(r):
        if ctemp[k][j] > 0 and k != i:
            lis.append(k)

    #  normalise each row in question with respective av,to calc centered cosine sim
    for k in lis:
        av = 0
        count = 0
        for l in ctemp[k]:
            if l > 0:
                av += l
                count += 1
        av = av/count  #  average of given row
        for b in ctemp[k]:
            if b > 0:
                b -= av  #  normalise

    av = 0
    count = 0
    #  doing the same for target row
    for l in ctemp[i]:
        if l > 0:
            av += l
            count += 1
    av = av/count  #  average of row i
    for b in ctemp[i]:
        if b > 0:
            b -= av  #  normalise only those terms which have been rated,unrated already at av

    sim = []  #  stores similarities b/w items and target item
    for k in lis:
        temp = 0
        for l in range(c):
            temp += ctemp[k][l] * ctemp[i][l]  #  adding product of concurrent values of target row and lis set
        temp1 = 0
        temp2 = 0
        for l in range(c):
            temp1 += ctemp[k][l]**2
            temp2 += ctemp[i][l]**2
        final = temp/(temp1**(1/2)*temp2**(1/2))
        sim.append(final)
    #  sim has corresponding to lis
    #  prediction of rating,using abs ratings from clb
    temp3 = 0
    for k in range(len(lis)):
        temp3 += sim[k] * clb[lis[k]][j]
    temp4 = 0
    for l in sim:
        temp4 += l
    #  divide by sum of similarity values
    temp3 = temp3/temp4
    return temp3+av


def bfitting(clb, i, j, r, c):  # run collaborative fitting
    #  temporaries: a,b,k,l,x,y
    lis = []
    u = 0  # universal average
    #  copy onto ctemp
    ctemp = [[0 for y in range(c)] for x in range(r)]
    for x in range(r):
        for y in range(c):
            u += clb[x][y]
            ctemp[x][y] = clb[x][y]

    u = u/(r*c)
    # take out items that have been rated by user j
    for k in range(r):
        if ctemp[k][j] > 0 and k != i:
            lis.append(k)

    jav = 0  #  average over col j
    for x in range(r):
        jav += clb[x][j]
    jav = jav/r
    rav = []
    #  normalise each row in question with respective av,to calc centered cosine sim
    for k in lis:
        av = 0
        count = 0
        for l in ctemp[k]:
            if l > 0:
                av += l
                count += 1
        av = av/count
        rav.append(av)
        #  list of averages of rows

        for b in ctemp[k]:
            if b > 0:
                b -= av  #  normalise

    av = 0
    #  doing the same for target row
    for l in ctemp[i]:
        av += l
    av = av/c
    iav = av
    for b in ctemp[i]:
        b -= av

    sim = []  #  stores similarities b/w items and target item
    for k in lis:
        temp = 0
        for l in range(c):
            temp += ctemp[k][l] * ctemp[i][l]  #  adding product of concurrent values of target row and lis set
        temp1 = 0
        temp2 = 0
        for l in range(c):
            temp1 += ctemp[k][l]**2
            temp2 += ctemp[i][l]**2
        final = temp/(temp1**(1/2)*temp2**(1/2))
        sim.append(final)
    #  sim has corresponding to lis
    #  prediction of rating,using abs ratings from clb
    temp3 = 0
    for k in range(len(lis)):
        temp3 += sim[k] * (clb[lis[k]][j] - (u + rav[k] - u + jav - u))
    temp4 = 0
    for l in sim:
        temp4 += l
    #  divide sum of similarity values by temp4
    temp3 = temp3/temp4
    #  adding changes in iav and jav
    temp3 += u + iav - u + jav - u
    return temp3





























