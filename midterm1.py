from pybrain.tools.shortcuts import buildNetwork
from pybrain.datasets import SupervisedDataSet
from pybrain.supervised.trainers import BackpropTrainer
from math import fabs


type = {'Irissetosa': -1, 'Irisversicolor': 0, 'Irisvirginica': 1}
traindata = {}
testdata = {}

net = buildNetwork(4, 10, 1)
ds = SupervisedDataSet(4, 1)
trainer = BackpropTrainer(net, ds, verbose = True)

f = open('bezdekIris.data.txt', 'r')

file = f.readlines()
f.close()

x = 0
for line in file:
    file[x] = file[x].strip()
    x += 1

number = 0
key = 0                           
while number < 150:
    traindata[key] = file[number]
    testdata[key] = file[number + 1]
    number += 2
    key += 1
    
for s in range(0,75):
    sample = traindata[s]
    sample = sample.split(',')
    sample[4] = sample[4].replace('-', '')
    sample[4] = type[sample[4]]

    for x in range(0,4):
        sample[x] = float(sample[x])
        sample[x] = sample[x] / 4
        sample[x] = sample[x] - 1

    ds.addSample((sample[0], sample[1], sample[2], sample[3]),
                 (sample[4]))
                
correct = 0
while trainer.train() > .01:
    trainer.train()

for z in range(0,75):
    test = testdata[z]
    test = test.split(',')
    test[4] = test[4].replace('-', '')
    test[4] = type[test[4]]

    for y in range(0,4):
        test[y] =  float(test[y])
        test[y] = test[y] / 4
        test[y] = test[y] - 1

    print "{} = {}" .format(z, test[4])
    result = net.activate((test[0], test[1], test[2], test[3]))
    print result
    difference = fabs(test[4]) - fabs(result)
    
    if fabs(difference) < .5:
        correct += 1

print "{} of 75 are correct." .format(correct)
percent = (float(correct) / 75) * 100 
print "{}% are correct." .format(percent)
        
