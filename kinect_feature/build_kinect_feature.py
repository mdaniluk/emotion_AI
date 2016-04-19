import matplotlib
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

def convert_to_seconds(s):
    a = s.split(':')
    return (float(a[0])*60+float(a[1]))

def name_to_idx(c):
    if(c=='m'):
        return 0
    if(c=='t'):
        return 1
    return -1
    
def build_feature(df):
    
    #spine
    smin = df.spine_ty.min()
    #head
    hmin = df.head_ty.min()
    hmax = df.head_ty.max()
    hrx = df.head_rx.abs().max()
    hry = df.head_ry.abs().max()    
    #left hand
    lmin = df.hand_L_ty.min()
    lmax = df.hand_L_ty.max()
    lvel = (lmax-lmin)/len(df)
    #right hand
    rmin = df.hand_R_ty.min()
    rmax = df.hand_R_ty.max()
    rvel = (rmax-rmin)/len(df)
    #x-distance between shoudler
    sdistmin = (df.upperArm_L_tx - df.upperArm_R_tx).min()
    sdistmax = (df.upperArm_L_tx - df.upperArm_R_tx).max()
    return [hmin,hmax,hrx,hry,sdistmin,sdistmax,smin,lmin,lmax,lvel,rmin,rmax,rvel]

m=0
t=1
first_line ='winner,head_ty_max,head_ty_min,head_rx_max,head_ry_max,'+\
            'upperArm_dist_min,upperArm_dist_max,'+\
            'spine_ty_min,'+\
            'hand_L_ty_min,hand_L_ty_max,hand_L_y_vel,'+\
            'hand_R_ty_min,hand_R_ty_max,hand_R_y_vel'

#total number of feature
n_feature = 13+1

#frame rate kinect
frame_rate = 30

#time window before the point
time_wb = 2

#time window after the point
time_wf = 2

for match in range(1,8):
    #load body file
    body_m = pd.read_csv('Wii_matches/match'+str(match)+'/test1_body_m.csv')
    body_t = pd.read_csv('Wii_matches/match'+str(match)+'/test1_body_t.csv')
    #normalise values
    body_t = (body_t - body_t.mean()) / body_t.std()
    body_m = (body_m - body_m.mean()) / body_m.std()
    
    time_point = pd.read_csv('Wii_matches/match'+str(match)+'/time_point'+str(match)+'.txt',sep=' ')
    time_point.timepoint = time_point.timepoint.map(convert_to_seconds)

    #outptu matrix
    feature_m = np.zeros((len(time_point),n_feature))
    feature_t = np.zeros((len(time_point),n_feature))

    count = 0
    for i in range(len(time_point)):
      winner = name_to_idx(time_point.winner[i])
      #looser = (winner+1)%2
      tm = time_point.timepoint[i]
      start = int((tm-time_wb)*frame_rate)
      end = min(int((tm+time_wf)*frame_rate),len(body_m))
      if(end-start > 0) :
        count = count +1
        #build the feature
        bf_m = build_feature(body_m[start:end])
        bf_t = build_feature(body_m[start:end])
        #add the winning/loosing info
        bf_m = [ 1 if m==winner else 0] + bf_m
        bf_t = [ 1 if t==winner else 0] + bf_t
        feature_m[i,:] = bf_m
        feature_t[i,:] = bf_t
    np.savetxt('match'+str(match)+'_player_m.csv', feature_m[:count,:], delimiter=',',header=first_line,comments='')
    np.savetxt('match'+str(match)+'_player_t.csv', feature_t[:count,:], delimiter=',',header=first_line,comments='')
