
  #@filename esame.py
  #@author(s) Silvia Bartole
  #@brief conteggio invesione trend temperatura (1 ora)

  #@date 19/02/2021
  #@last update 22/02/2021
  #@version 1

  #programma che riceve in input un file .cvs contenente un elenco di orari (formato epoch) con associate le relative misurazioni di temperatura
  #torna in output una lista contenente il numero di inversioni di trend di temperatura che avvengono in un ora

class ExamException(Exception):
	pass

class CSVTimeSerie:
	
	def __init__(self, name):
		self.name = name
	
	def get_data(self):
		try:
			my_file = open(self.name, "r")
		except:
			raise ExamException('Errore, file inesistente o illeggibile')	

		time_series = []
		test_timestamp = []
		
		for line in my_file:
			elements = line.split(',')
			
			if elements[0] != "epoch":
				elements_num = []
				elements_num.append(float(elements[0]))
				try:
					elements_num.append(float(elements[1]))
				except:
					pass
				else:
					if (elements_num[1] != 0 or elements_num[1] != None):
						if type(elements_num[0])!= int:
							elements_num[0] = round(elements_num[0])
						test_timestamp.append(elements_num[0])
						time_series.append(elements_num)
		
		test_timestamp_copy = test_timestamp
		test_timestamp.sort()
		if(test_timestamp_copy != test_timestamp):
			raise ExamException('Errore, timestamp fuori ordine')
		
		test_timestamp = list(set(test_timestamp))
		if (len(test_timestamp_copy) != len(test_timestamp)):
			raise ExamException('Errore, timestamp duplicato')

		return time_series

def hourly_trend_changes(time_series):
	temperatures = []
    list_temperatures = []
	h = time_series[0][0] - (time_series[0][0]%3600)
	for elements in time_series:
		
		if elements[0] - (elements[0]%3600) == h:
			temperatures.append(elements[1])
		else:
		list_temperatures.append(temperatures)
			temperatures = []
			h = elements[0] - (elements[0]%3600)
			temperatures.append(elements[1])
	
	list_counter = []
	
	for temperatures in list_temperatures:
		counter = 0
		delta1 = 0
		delta2 = 0
		
		for i in range(len(temperatures)-1):
			delta2 = temperatures [i] - temperatures[i+1]
			
			#caso in cui ci sia un valore costante dopo il quale avviene un cambio di trend
			if (delta1 == 0 and delta2 != 0):
				j = i
				costant = temperatures[i]
				while (j >= 0 and delta1 == 0):
					if (temperatures[j] != costant):
						delta1 = temperatures[j] - costant
					j = j - 1
			
			if (delta1 > 0 and delta2 < 0) or (delta1 < 0 and delta2 > 0):
				counter = counter + 1
			delta1 = delta2
		
		list_counter.append(counter)
	return list_counter

time_series_file = CSVTimeSeriesFile(name='data.csv')
time_series = time_series_file.get_data()
hourly_trend_changes(time_series)
