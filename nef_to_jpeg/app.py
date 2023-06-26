import rawpy
import imageio
import os

from flask import Flask, render_template, request

# path = '/media/wd/d1/Projects/nef_to_jpeg/data/'
# op_path = '/media/wd/d1/Projects/nef_to_jpeg/output/'

# for filename in os.listdir(path):
# 	name_wo_extension = filename.split('.')[0]
# 	file_path = path + filename
# 	with rawpy.imread(file_path) as raw:
#    		rgb = raw.postprocess(rawpy.Params(use_camera_wb=True))
# 	imageio.imsave( op_path + name_wo_extension + '.jpg', rgb)



app = Flask(__name__)

@app.route("/", methods = ["GET", "POST"])
def home():
	if request.method == "POST":
		# try:
		ip_path = request.form['input']			
		op_path = request.form['output']

		for filename in os.listdir(ip_path):
			name_wo_extension = filename.split('.')[0]
			file_path = ip_path + filename
			with rawpy.imread(file_path) as raw:
				rgb = raw.postprocess(rawpy.Params(use_camera_wb=True))
			imageio.imsave( op_path + name_wo_extension + '.jpg', rgb)

		success_message = "All files are successfully converted."
		return render_template("index.html", success_message=success_message)
		
		# except : return ("There's an error no one knows where.") 

	return render_template("index.html")



if __name__ == "__main__" :
	app.run(debug=True, port=5000)





