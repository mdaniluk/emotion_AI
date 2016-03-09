import numpy as np
import csv
import matplotlib.pyplot as plt

class watch_reader:
    def __init__(self, match_id, player):
        self.match_id = match_id
        self.player = player
        self.data = {'ACCx': [], 'ACCy': [], 'ACCz': [], 'EDA': [], 'BVP': [], 'HR': []}
        self.sample_rate = {'ACCx': [], 'ACCy': [], 'ACCz': [], 'EDA': [], 'BVP': [], 'HR': []}
        self.start_time = self.read_start_time()
        self.timepoints = []
        self.winner = []
        self.get_timepoints_and_winners()

    def read_start_time(self):
        start_time = 0.0
        with open("Wii_matches/match%d/watch%d%s/tags.csv"%(self.match_id, self.match_id, self.player), "rb") as file1:
            file_reader = csv.reader(file1, delimiter=' ')
            for row_id, row in enumerate(file_reader):
                start_time = float(row[0])
        print start_time
        return start_time
       

    def get_timepoints_and_winners(self):
        with open("Wii_matches/match%d/timepoints.csv"%(self.match_id), "rb") as file1:
            file_reader = csv.reader(file1, delimiter=' ')
            for row_id, row in enumerate(file_reader):
                row = row[0].split(',')
                self.winner.append(int(row[0]))
                
                time = row[1].split(':')
                
                self.timepoints.append(60*float(time[0]) + float(time[1]) )
                
    def read_ACC(self):
        with open("Wii_matches/match%d/watch%d%s/ACC.csv"%(self.match_id, self.match_id, self.player), "rb") as file1:
            file_reader = csv.reader(file1, delimiter=' ')
            
            for row_id, row in enumerate(file_reader):
                if row_id == 0 or row_id == 1:
                    continue
                row = row[0].split(',')
                self.data['ACCx'].append(float(row[0]))
                self.data['ACCy'].append(float(row[1]))
                self.data['ACCz'].append(float(row[2]))
        
    def read_EDA(self):
        with open("Wii_matches/match%d/watch%d%s/EDA.csv"%(self.match_id, self.match_id, self.player), "rb") as file1:
            file_reader = csv.reader(file1, delimiter=' ')
            for row_id, row in enumerate(file_reader):
                if row_id == 0 :
                    watch_on = float(row[0])
                elif row_id == 1:
                    self.sample_rate['EDA'] = float(row[0])
                    
                if row_id == 0 or row_id == 1:
                    continue
            
                difference = self.start_time - watch_on
                num_rows_to_remove = difference * self.sample_rate['EDA']
                if (row_id > num_rows_to_remove):
                    self.data['EDA'].append(float(row[0]))
                
    def read_BVP(self):
        with open("Wii_matches/match%d/watch%d%s/BVP.csv"%(self.match_id, self.match_id, self.player), "rb") as file1:
            file_reader = csv.reader(file1, delimiter=' ')
            for row_id, row in enumerate(file_reader):
                if row_id == 0 :
                    watch_on = float(row[0])
                elif row_id == 1:
                    self.sample_rate['BVP'] = float(row[0])
                    
                if row_id == 0 or row_id == 1:
                    continue
            
                difference = self.start_time - watch_on
                num_rows_to_remove = difference * self.sample_rate['BVP']
                if (row_id > num_rows_to_remove):
                    self.data['BVP'].append(float(row[0]))
            
    def read_HR(self):
        with open("Wii_matches/match%d/watch%d%s/HR.csv"%(self.match_id, self.match_id, self.player), "rb") as file1:
            file_reader = csv.reader(file1, delimiter=' ')
            for row_id, row in enumerate(file_reader):
                if row_id == 0 :
                    watch_on = float(row[0])
                elif row_id == 1:
                    self.sample_rate['HR'] = float(row[0])
                    
                if row_id == 0 or row_id == 1:
                    continue
            
                difference = self.start_time - watch_on
                num_rows_to_remove = difference * self.sample_rate['HR']
                if (row_id > num_rows_to_remove):
                    self.data['HR'].append(float(row[0]))
    
                           
    def plot_data(self):
        plt.plot(np.linspace(0, len(self.data['EDA']) / self.sample_rate['EDA'], num = len(self.data['EDA'])), self.data['EDA'],'r-')
        for timepoint in self.timepoints:
            plt.axvline(x = timepoint)           
        plt.show()
        plt.plot(np.linspace(0, len(self.data['BVP']) / self.sample_rate['BVP'], num = len(self.data['BVP'])), self.data['BVP'],'r-')
        for timepoint in self.timepoints:
            plt.axvline(x = timepoint)          
        plt.show()
        plt.plot(np.linspace(0, len(self.data['HR']) / self.sample_rate['HR'], num = len(self.data['HR'])), self.data['HR'],'g-')
        for timepoint in self.timepoints:
            plt.axvline(x = timepoint)          
        plt.show()
        
if __name__ == "__main__":
    w_reader = watch_reader(7,'michal')
    w_reader.read_EDA()
    w_reader.read_BVP()
#    w_reader.read_ACC()
    w_reader.read_HR()
    w_reader.plot_data()