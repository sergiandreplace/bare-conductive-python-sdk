"""
.. module:: bareconductive
   :synopsis: BareConductive API

*Created on June 18th, 2015*
"""

import serial, time

TOUCH="TOUCH";
TTHS="TTHS";
RTHS="RTHS";
FDAT="FDAT";
BVAL="BVAL";
DIFF="DIFF";

class BareConductive():


	def __init__(self, port=6):
		self.port=port;
	

	def open(self):
		self.ser=serial.Serial(self.port, 57600);
		return self.ser;

	def read(self):
		self.ser.flush();
		touchLine=[];
		tthsLine=[];
		rthsLine=[];
		fdatLine=[];
		bvalLine=[];
		diffLine=[];
		ok=0;
		output={};

		while ok==0:
			ok=1;
			try:
				touchLine=self.readType(TOUCH);
				tthsLine=self.readType(TTHS);
				rthsLine=self.readType(RTHS);			
				fdatLine=self.readType(FDAT);
				bvalLine=self.readType(BVAL);
				diffLine=self.readType(DIFF);
				for i in range(13) :
					sensor={};
					sensor[TOUCH]=touchLine[i];
					sensor[TTHS]=tthsLine[i];
					sensor[RTHS]=rthsLine[i];
					sensor[FDAT]=fdatLine[i];
					sensor[BVAL]=bvalLine[i];
					sensor[DIFF]=diffLine[i];
					output[i]=sensor;
			except Exception as e:
				print e;
				ok=0;

		return output;

	def readType(self, type=TOUCH):
		output=self.readLine();
		ok=0;
		while (not(output.startswith(type))):
			output=self.readLine();
		outputArray= output[len(type)+1:].strip().split(' ');
		if (len(outputArray)!=13):
				raise Exception();
		return outputArray;

	def readLine(self):
		return self.ser.readline();

	def close(self):
		self.ser.close();

if __name__ == '__main__':
	bare=BareConductive
	while 1:
		output=bare.read();
		#if (output.startswith("TOUCH")
	bare.close();
	