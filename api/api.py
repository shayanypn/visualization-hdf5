from flask import Flask, jsonify, make_response
from flask_cors import CORS
import h5py
import numpy as np

def create_app():
	app = Flask(__name__)
	CORS(app)

	@app.route('/')
	def home_route():
		return make_response(jsonify({'status': 'ok'}), 200)

	@app.route('/data/<sample_name>')
	def data_route(sample_name):
		filename = './' + sample_name +'.hdf5'

		with h5py.File(filename, "r") as f:

			interval_item = list(f.keys())[1]
			interal_groups = f[interval_item]
			dataset = [];

			for index, item in enumerate(interal_groups["time"]):
				time = item[0],
				glucose = interal_groups["glucose"][index][0],
				dataset.append({
					"time": int(time[0]),
					"glucose": glucose[0]
				})

		return make_response(jsonify(dataset), 200)

	@app.route('/data/<sample_name>/<ts>')
	def data_detail_route(sample_name, ts):
		filename = './' + sample_name +'.hdf5'

		with h5py.File(filename, "r") as f:

			interval_item = list(f.keys())[1];
			interal_groups = f[interval_item];
			dataset = [];

			for index, time in enumerate(interal_groups["time"]):
				if int(ts) == int(time[0]):
					dataset = np.array(interal_groups["measurement"][index]).tolist()

		return make_response(jsonify(dataset), 200)




	@app.route('/pagingdata/<sample_name>/<limit>/<page>')
	def wholedata_route(sample_name, limit, page):
		filename = './' + sample_name +'.hdf5'

		with h5py.File(filename, "r") as f:

			interval_item = list(f.keys())[1]
			interal_groups = f[interval_item]
			dataset = [];
			start = int(limit) * int(page)
			end = int(limit) * (int(page) + 1)

			for index, item in enumerate(interal_groups["time"]):
				time = item[0],
				glucose = interal_groups["glucose"][index][0],
				if index >= start and index < end:
					dataset.append({
						"time": int(time[0]),
						"glucose": glucose[0],
						"measurement": np.array(interal_groups["measurement"][index]).tolist()
					})

		return make_response(jsonify(dataset), 200)

	return app

if __name__ == "__main__":
	app = create_app()
	app.run(debug=True)
	# serve the application on port 7410
	app.run(host='0.0.0.0', port=7410)