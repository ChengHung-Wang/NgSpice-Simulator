
AC_TYPE = 0
TRANS_TYPE = 1
DC_TYPE = 2

import sys
import os
import json
from decimal import Decimal

class DataExtraction:
    def __init__(self,analysisInfo,plotFile):
        self.data = []
        self.analysisInfo = analysisInfo.split() #['.dc', 'v1', '-1e-00', '5e-00', '0.02e-00', 'i1', '-1e-03', '5e-03', '1e-03']
        self.plotFile = plotFile
        self.val_dict = {}
        self.voltList = []

    def openFile(self):
        try:
            with open(self.plotFile) as plotFile_reader:
                self.allv = plotFile_reader.read()
            self.allv = self.allv.split("\n")

        except Exception as e:
            print "Exception Message : ",str(e)

        for line in self.allv[3].split(" "):
            if len(line):
                self.voltList.append(line)
        self.voltList = self.voltList[2:]
        
        numberList = self.calculateNumbers()
        plotType = self.createDataList(numberList)

        return plotType


    def calculateNumbers(self):

        lines_number = partition_number = volt_number = 0

        for line in self.allv[3:]:
            if "Index" in line:
                volt_number += 1

        self.dec = 0

        if self.analysisInfo[0][-3:]==".ac":
            self.analysisType = AC_TYPE
            if "dec" in self.analysisInfo:
                self.dec = 1

            for line in self.allv[3:]:
                lines_number += 1
                if "Index" in line:
                    partition_number += 1
                if "AC" in line:
                    break

        elif ".tran" in self.analysisInfo:
            self.analysisType = TRANS_TYPE
            for line in self.allv[3:]:
                lines_number += 1
                if "Index" in line:
                    partition_number += 1
                if "Transient" in line:
                    break

        else:
            self.analysisType = DC_TYPE
            for line in self.allv[3:]:
                lines_number += 1
                if "Index" in line:
                    partition_number += 1
                if "DC" in line:
                    break

        
        volt_number //= partition_number

        return [lines_number, volt_number]


    def createDataList(self, numberList):
        lines_number = numberList[0] + 1
        volt_number = numberList[1]
        dec = [self.analysisType, self.dec]

        vnum = len(self.allv[5].split("\t"))
        
        len_volt = len(self.voltList)
        
        full_data = []

        #creating data
        for i in xrange(1, volt_number):
            for line in self.allv[3+i*lines_number].split(" "):
                if len(line) > 0:
                    self.voltList.append(line)
            self.voltList.pop(len_volt)
            self.voltList.pop(len_volt)
            len_volt = len(self.voltList)

        
        p = k = m = 0


        for line in self.allv[5:lines_number-1]:
            if len(line.split("\t")) == vnum:
                j = line.split("\t")
                j.pop()
                if self.analysisType == 0:
                    j.pop()
                for i in xrange(1, volt_number):
                    j1 = self.allv[5+i*lines_number+p].split("\t")
                    j1.pop(0)
                    j1.pop(0)
                    if self.analysisType == 0:
                        j1.pop()
                    if self.voltList[len(self.voltList)-1] == 'v-sweep':
                        self.voltList.pop()
                        j1.pop()

                    j1.pop()
                    j = j + j1
                # j = j + full_data[m] ## Not required as we are not adding alli
                m += 1
                j = "\t".join(j[1:])
                j = j.replace(",", "")
                self.data.append(j)

            p += 1

        self.volts_length = len(self.voltList)
        self.voltList = self.voltList #+ self.currentList

        #print dec
        return dec


    def computeAxes(self):
        nums = len(self.data[0].split("\t"))
        #print "i'm nums:",nums
        x_cordinates = []
        y_cordinates = []
        var = self.data[0].split("\t")
        for i in range(1,nums):
            y_cordinates.append([float(var[i])])
        for i in self.data[1:]:
            temp = i.split("\t")
            for j in range(1,nums):
                y_cordinates[j-1].append(float(temp[j]))
        for i in self.data:
            temp = i.split("\t")
            x_cordinates.append(float(temp[0]))

        for i in xrange(0, nums-1):
            self.val_dict[self.voltList[i]] = y_cordinates[i]
        self.val_dict['x-axis'] = x_cordinates


def main():
    analysisInfo = sys.argv[1]
    plotFile = sys.argv[2]
    app = DataExtraction(analysisInfo,plotFile)
    app.openFile()
    app.computeAxes()
    
    print json.dumps(app.val_dict)

# Call main function
if __name__ == '__main__':
    # Create and display the splash screen
    main()

