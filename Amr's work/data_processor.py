import pandas as pd
import numpy as np
from sklearn.preprocessing import LabelEncoder
from sklearn.model_selection import train_test_split

class DataProcessor():

	def __init__(self): 
		self.file = "../data/Train.csv"
		self.time_attributes = ['Placement - Time', 'Confirmation - Time', 'Arrival at Pickup - Time', 'Pickup - Time', 'Arrival at Destination - Time']	
		self.categorical_attributes = ['User Id' , 'Vehicle Type', 'Platform Type', 'Rider Id', 'Personal or Business']
		self.label_col = 'Time from Pickup to Arrival'
		self.encoder = LabelEncoder
		self.one_hot = None
		self.user_col = ['User Id']
		self.cols_to_drop = ['Order No', 'Precipitation in millimeters']

	def _load_file(self, file): 
		train_df = pd.read_csv(file)
		return train_df

	def _drop_col(self, df, col_to_drop):
		df = df.drop(col_to_drop, axis = 1)
		return df 

	def _fill_null(self, df): 
		df = df.fillna(df.mean())
		return df 

	def _process_time(self, df, dt_attributes):

		for time in dt_attributes: 
			df[time] = pd.to_datetime(df[time]).dt.strftime('%H:%M:%S')

		for time in dt_attributes:
			df[time+'_H'] = pd.DatetimeIndex(df[time]).hour
			df[time+'_M'] = pd.DatetimeIndex(df[time]).minute
			df[time+'_S'] = pd.DatetimeIndex(df[time]).second

			df = self._drop_col(df, time)

		return df 

	def _encode_categorical(self, df, encoding, attribues): 
		
		encoder = encoding()
		encoded = df[attribues].apply(encoder.fit_transform)
		df[attribues] = encoded[attribues]

		return df 

	def _extract_features_labels(self, df, label_col):

		feature_cols = df.columns.drop([label_col])

		X = df[feature_cols]
		Y = df[[label_col]]

		return X, Y

	def _get_numpy_train_valid_data(self, data):
		X, Y = data
		x_train, x_valid, y_train, y_valid = train_test_split(X.values, Y.values, test_size=0.33)

		return x_train, x_valid, y_train, y_valid

	def get_numpy_data(self, fillna = True, encode = True, np_split = True, enocde_user = False): 

		df = self._load_file(self.file)

		for col in self.cols_to_drop: 
			df = self._drop_col(df, col)

		if fillna is True:
			df = self._fill_null(df)

		df = self._process_time(df, self.time_attributes)
		
		if encode is True: 
			df = self._encode_categorical(df, self.encoder, self.categorical_attributes)
		
		if enocde_user is False: 
			df = self._drop_col(df, self.user_col)
		
		if np_split is True:
			return self._get_numpy_train_valid_data(self._extract_features_labels(df, self.label_col))
		else:
			return self._extract_features_labels(df, self.label_col)


	#def get_nomralized_numpy_data(self, data): 


def main():
    pass

if __name__ == "__main__":
	main()