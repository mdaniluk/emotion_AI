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
        self.features = {'EDA_mean': [], 'BVP_mean': [], 'HR_mean': [], 
                         'EDA_std': [], 'BVP_std': [], 'HR_std': [],
                         'label': []}

    def reset(self):
        self.data = {'ACCx': [], 'ACCy': [], 'ACCz': [], 'EDA': [], 'BVP': [], 'HR': []}
        self.sample_rate = {'ACCx': [], 'ACCy': [], 'ACCz': [], 'EDA': [], 'BVP': [], 'HR': []}
        self.features = {'EDA_mean': [], 'BVP_mean': [], 'HR_mean': [], 
                         'EDA_std': [], 'BVP_std': [], 'HR_std': [],
                         'label': []}
                         
    def read_start_time(self):
        start_time = 0.0
        with open("Wii_matches/match%d/watch%d%s/tags.csv"%(self.match_id, self.match_id, self.player), "rb") as file1:
            file_reader = csv.reader(file1, delimiter=' ')
            for row_id, row in enumerate(file_reader):
                start_time = float(row[0])
#        print start_time
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
    
    def get_window_at_timepoint(self, data, sample_rate, timepoint, size = 4):
        centre = sample_rate * timepoint
        begin = int(centre - sample_rate * size/2)
        end = int(centre + sample_rate * size/2)
        return data[begin:end]
        
    def get_mean(self, data):
        return float(sum(data) / len(data))
    
    def stddev(self, data):
        return np.std(data)

    def compute_features(self):
        mean_EDA = self.get_mean(self.data['EDA'])
        mean_BVP = self.get_mean(self.data['BVP'])
        mean_HR = self.get_mean(self.data['HR'])
        
        #normalize data
        self.data['EDA'] = [x - mean_EDA for x in self.data['EDA']]
        self.data['BVP'] = [x - mean_BVP for x in self.data['BVP']]
        self.data['HR'] = [x - mean_HR for x in self.data['HR']]
        
        
        for idx, timepoint in enumerate(self.timepoints):
#                plt.plot(np.linspace(0, len(self.data['EDA']) / self.sample_rate['EDA'], num = len(self.data['EDA'])), self.data['EDA'],'r-')
#                plt.axvline(x = timepoint)
#                plt.show()
            sample_EDA = self.get_window_at_timepoint(self.data['EDA'], self.sample_rate['EDA'], timepoint)
#                plt.plot(np.linspace(0, len(sample) / self.sample_rate['EDA'], num = len(sample)), sample,'g-')
#                plt.show()
            sample_BVP = self.get_window_at_timepoint(self.data['BVP'], self.sample_rate['BVP'], timepoint)
            sample_HR = self.get_window_at_timepoint(self.data['HR'], self.sample_rate['HR'], timepoint)                
            self.features['EDA_mean'].append(self.get_mean(sample_EDA))
            self.features['BVP_mean'].append(self.get_mean(sample_BVP))
            self.features['HR_mean'].append(self.get_mean(sample_HR))
            self.features['EDA_std'].append(self.stddev(sample_EDA))
            self.features['BVP_std'].append(self.stddev(sample_BVP))
            self.features['HR_std'].append(self.stddev(sample_HR))
            
            self.features['label'].append(self.winner[idx])

                
                    
    def plot_data(self):
        plt.plot(np.linspace(0, len(self.data['EDA']) / self.sample_rate['EDA'], num = len(self.data['EDA'])), self.data['EDA'],'r-')
        for idx, timepoint in enumerate(self.timepoints):
            if (self.winner[idx] == 1):
                plt.axvline(x = timepoint,  color='g')
            elif(self.winner[idx] == 2):
                plt.axvline(x = timepoint,  color='b')
            else:
                print "SOMETHING WRONG"
        plt.show()
        plt.plot(np.linspace(0, len(self.data['BVP']) / self.sample_rate['BVP'], num = len(self.data['BVP'])), self.data['BVP'],'r-')
        for idx, timepoint in enumerate(self.timepoints):
            if (self.winner[idx] == 1):
                plt.axvline(x = timepoint,  color='g')
            elif(self.winner[idx] == 2):
                plt.axvline(x = timepoint,  color='b')
            else:
                print "SOMETHING WRONG"         
        plt.show()
        plt.plot(np.linspace(0, len(self.data['HR']) / self.sample_rate['HR'], num = len(self.data['HR'])), self.data['HR'],'g-')
        for idx, timepoint in enumerate(self.timepoints):
            if (self.winner[idx] == 1):
                plt.axvline(x = timepoint,  color='g')
            elif(self.winner[idx] == 2):
                plt.axvline(x = timepoint,  color='b')
            else:
                print "SOMETHING WRONG"         
        plt.show()
   
   
   
def write_data():
    names = ['michal', 'thomas']
    matches = [1, 2, 3, 4, 5, 6, 7]
    with open('features_watches.csv', 'wb') as feature_file:
        f_writer = csv.writer(feature_file, delimiter=',', quotechar='|', quoting=csv.QUOTE_MINIMAL)
        f_writer.writerow(('id', 'EDA_mean', 'BVP_mean', 'HR_mean', 
                               'EDA_std', 'BVP_std', 'HR_std', 'player', 'win(1) lose(0)'))
        idd = 1
        for match in matches:            
            for name in names:
                try:
                    print(name)
                    print(match)
                    w_reader = watch_reader(match, name)
                    w_reader.read_EDA()
                    w_reader.read_BVP()
                    w_reader.read_HR()
                    w_reader.compute_features()
                    for idx, timepoint in enumerate(w_reader.timepoints):
                        win = -999                    
                        if name == 'michal':
                            if w_reader.winner[idx] == 1:
                                win = 1
                            else:
                                win = 0
                        elif name == 'thomas':
                            if w_reader.winner[idx] == 1:
                                win = 0
                            else:
                                win = 1
                                
                        f_writer.writerow((idd,w_reader.features['EDA_mean'][idx],
                                      w_reader.features['BVP_mean'][idx],
                                      w_reader.features['HR_mean'][idx],
                                      w_reader.features['EDA_std'][idx],
                                      w_reader.features['BVP_std'][idx],
                                      w_reader.features['HR_std'][idx],
                                      name, win))
                        idd = idd + 1
                    w_reader.reset()
                except:
                    print('no data')
                    print (match)
                    print(name)
                    print('no data')
#           for idx, timepoint in enumerate(self.timepoints):
#               f_writer = csv.writer(feature_file, delimiter=',', quotechar='|', quoting=csv.QUOTE_MINIMAL)
#               f_writer.writerow((self.features['EDA_mean'][idx],
#                                  self.features['BVP_mean'][idx],
#                                  self.features['HR_mean'][idx],
#                                  self.features['EDA_std'][idx],
#                                  self.features['BVP_std'][idx],
#                                  self.features['HR_std'][idx]))
if __name__ == "__main__":
#    w_reader = watch_reader(1,'thomas')
#    w_reader.read_EDA()
#    w_reader.read_BVP()
##    w_reader.read_ACC()
#    w_reader.read_HR()
#    w_reader.plot_data()
#    
#    w_reader.compute_features()
    write_data()