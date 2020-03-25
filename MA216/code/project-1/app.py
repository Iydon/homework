# built-in module
from hashlib import md5
from os import path
# flask-like module
from flask import Flask, Response, redirect, url_for, session, render_template
from flask_script import Manager
from flask_bootstrap import Bootstrap
from flask_wtf import FlaskForm
from wtforms import IntegerField, StringField, FloatField, SubmitField
from wtforms.validators import AnyOf, NumberRange
# scientific module
from pandas_datareader.data import get_data_yahoo
from tushare import get_hist_data
# own module
from lppl import Model


app = Flask(__name__)
app.config["SECRET_KEY"] = 'Svégio'
manager = Manager(app)
bootstrap = Bootstrap(app)


class URLForm(FlaskForm):
	source = IntegerField(
		'`0` 为使用`pandas_datareader`数据, ' \
		'`1`为使用`tushare`数据 (例如`0`).',
		validators=[AnyOf((0, 1))],)
	code = StringField('股票或指数代码 (例如`000001.SS`).')
	start = StringField('开始时间, 格式为`年-月-日` (例如为`2017-4-1`).')
	end = StringField('结束时间, 格式为`年-月-日` (例如`2018-4-1`).')
	tt_ratio = FloatField('训练集占测试集的比例 (例如`0.5`).',
		validators=[NumberRange(0., 1.)])
	et_ratio = FloatField('向后预测时间占所有数据时间的比例 (例如`1.0`).',
		validators=[NumberRange(1.)])
	submit = SubmitField("Submit")


@app.route('/')
def index():
	demo = url_for('demo')
	return f'Please check @ <a href="{demo}">demo</a>.'

@app.route('/demo')
def demo():
	source = '0'
	code = '000001.SS'
	start = '2017-4-1'
	end = '2018-4-1'
	tt_ratio = '0.5'
	et_ratio = '1.2'
	return redirect(url_for('lppl', **locals()))

@app.route('/lppl', methods=["GET", "POST"])
def lppl_index():
	source = session.get('SOURCE')
	code = session.get('CODE')
	start = session.get('START')
	end = session.get('END')
	tt_ratio = session.get('TT_RATIO')
	et_ratio = session.get('ET_RATIO')
	kwargs = locals()
	form = URLForm(**kwargs)
	if form.validate_on_submit():
		return redirect(url_for('lppl',
			**{k:getattr(form, k).data for k in kwargs}))
	return render_template('lppl.html', form=form)

@app.route('/lppl/<source>:<code>:<start>:<end>:<tt_ratio>:<et_ratio>')
def lppl(source, code, start, end, tt_ratio, et_ratio):
	'''
	Argument
	=======
		source: int, 0 or 1

	Example
	=======
		0:000001.SS:2017-4-1:2018-4-1:0.5:1.2
	'''
	def read_binary_file(file):
		with open(file, 'rb') as f:
			return f.read()
	# file exists?
	params = source + code + start + end + tt_ratio + et_ratio
	figure = md5(params.encode()).hexdigest() + '.png'
	if not path.exists(figure):
		# pre-process arguments
		source = {'0':get_data_yahoo, '1':get_hist_data}[source]
		tt_ratio = float(tt_ratio)
		et_ratio = float(et_ratio)
		# construct model
		m = Model(source, code, start, end, tt_ratio, et_ratio)
		m.plot_predict(figure)
	return Response(read_binary_file(figure), mimetype="image/jpeg")



if __name__ == '__main__':
	manager.run()
