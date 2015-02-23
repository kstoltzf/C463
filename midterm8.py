from pybrain.tools.shortcuts import buildNetwork
from pybrain.datasets import SupervisedDataSet
from pybrain.supervised.trainers import BackpropTrainer
from math import fabs

traindata = {}
testdata = {}

net = buildNetwork(4, 5, 1)
ds = SupervisedDataSet(4, 1)
trainer = BackpropTrainer(net, ds, verbose = True)

f = open('data_banknote_authentication.txt', 'r')

file = f.readlines()
f.close()

x = 0
for line in file:
    file[x] = file[x].strip()
    x += 1
             
number = 0
key = 0                           
while number < 1372:
    traindata[key] = file[number]
    testdata[key] = file[number + 1]
    number += 2
    key += 1           


for s in range(0,686):
    sample = traindata[s]
    sample = sample.split(',')

    for x in range(0,5):
        sample[x] = float(sample[x])

    ds.addSample((sample[0], sample[1], sample[2], sample[3]),
                 (sample[4]))
                
correct = 0
while trainer.train() > .001:
    trainer.train()

for z in range(0,686):
    test = testdata[z]
    test = test.split(',')

    for y in range(0,5):
        test[y] =  float(test[y])

    print "{} = {}" .format(z, test[4])
    result = net.activate((test[0], test[1], test[2], test[3]))
    print result
    difference = fabs(test[4]) - fabs(result)
    
    if fabs(difference) < .1:
        correct += 1

print "{} of 686 are correct." .format(correct)
percent = (float(correct) / 686) * 100 
print "{}% are correct." .format(percent)
        
