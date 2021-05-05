import streamlit as st
import numpy as np
from scorer import calculate_score
from pre_treatment import treat_input
from probability import calc_proba
from normalizer import normalize
import time as tm
import pandas as pd
import plotly.express as px
from plotly.subplots import make_subplots
import plotly.graph_objects as go
import matplotlib.pyplot as plt
import base64


st.set_page_config(
page_title="ISP",
page_icon="logo.PNG",
layout="centered",
)

st.title('Intelligent Salary Predictor')
st.write("")
st.write("")
st.write("Welcome User! This intelligent salary predictor(ISP) helps you assess yourself in the field of data science. How? It's easy! Just fill in the survey form.")
st.write("After submitting your response to the form, you will receive three values:")
st.markdown("*  A score: the maximum score that can be obtained is 1000. The closer your score is to this value, the more likely you are to receive a salary of $100,000*")
st.markdown("* Probability percentage: the probability (out of 100) that you will receive $100,000*")
st.markdown("* The anticipated salary range: your current valuation in this industry")
st.markdown("*: This value represents the salary of a data scientist with the relevant skill set, qualifications, experience and knowledge, keeping in mind the current market trend, that makes him/her greatly appreciated in the field.")
st.write("")
st.markdown("So Let's get predicting! :chart_with_upwards_trend:")
st.write("")
st.write("")
st.write("")
st.write("")
st.write("")

name = st.text_input(label='Enter your name:')
gender = st.radio("1. What is your gender?", ('Male', 'Female'))
q1_male = q1_female=0
if gender == 'Male':
	q1_male=1
else:
	q1_female=1

age = st.slider("2. Choose your age: ",18, 55,)
q2_one=q2_two=q2_three=q2_four=q2_five=q2_six=0
if age>= 18 and age<22:
	q2_one=1
elif age>=22 and age<25:
	q2_two=1
elif age>=25 and age<30:
	q2_three=1
elif age>=30 and age<35:
	q2_four=1
elif age>=35 and age<40:
	q2_five=1
else:
	q2_six=1


country = st.selectbox("3. In which Country do you currently reside?", ('United States of America','India','China'))
q3_usa=q3_ind=q3_ch=0
if country == 'United States of America':
	q3_usa=1
elif country == 'India':
	q3_ind=1
else:
	q3_ch=1	


degree = st.selectbox("4. What is your level of education?", ("Bachelor's degree","Master's degree","Doctoral's degree"))
q4_b=q4_m=q4_d=0
if degree == "Bachelor's degree":
	q4_b=1
elif degree == "Master's degree":
	q4_m=1
else:
	q4_d=1


title = st.selectbox("5. What is your current title?", ('Student','Data Scientist','Data Analyst','Research Scientist','Software Engineer','Other'))
q5_s=q5_ds=q5_da=q5_rs=q5_se=q5_o=0
if title == 'Student':
	q5_s=1
elif title == 'Data Scientist':
	q5_ds=1
elif title == 'Data Analyst':
	q5_da=1
elif title == 'Research Scientist':
	q5_rs=1
elif title == 'Software Engineer':
	q5_se=1
else:
	q5_o=1


ind = st.selectbox("6. In what industry is your current employer/contract?", ('Accounting/Finance', 'Computers/Technology', 'Academics/Education', 'Other', 'I am a student'))
q6_af=q6_c=q6_ae=q6_o=q6_s=0
if ind == 'Accounting/Finance':
	q6_af=1
elif ind == 'Computers/Technology':
	q6_c=1
elif ind == 'Academics/Education':
	q6_ae=1
elif ind == 'Other':
	q6_o=1
else:
	q6_s=1
	

exp = st.selectbox("7. How many years of experience do you have in your current role?", ('0-1','1-2','2-3','3-4','4-5','5-10','10-15'))
q7_first=q7_second=q7_third=q7_fourth=q7_fifth=q7_sixth=q7_seventh=0
if exp == '0-1':
	q7_first=1
elif exp == '1-2':
	q7_second=1
elif exp == '2-3':
	q7_third=1
elif exp == '3-4':
	q7_fourth=1
elif exp == '4-5':
	q7_fifth=1
elif exp == '5-10':
	q7_sixth=1
else:
	q7_seventh=1


models = st.selectbox("8. Does your current employer incorporate machine learning methods into their business?", ('We have well established ML methods', 'We recently started using ML methods', 'We only use ML methods for generating insights', 'We are exploring ML methods', 'No', 'I dont know'))
q8_wehave=q8_werec=q8_weonly=q8_weare=q8_no=q8_idk=0
if models == 'We have well established ML methods':
	q8_wehave=1
elif models == 'We recently started using ML methods':
	q8_werec=1
elif models == 'We only use ML methods for generating insights':
	q8_weonly=1
elif models == 'We are exploring ML methods':
	q8_weare=1
elif models == 'No':
	q8_no=1
else:
	q8_idk=1


def get_activity():
	q9_proto=q9_ml=q9_an=q9_nota=q9_do=q9_data=0
	activity = st.multiselect('9. Select any activities that make up an important part of your role at work:', ['Building prototypes to explore applying machine learning to new areas', 
	'Build and/or run a machine learning service that operationally improves my product or workflows',
	'Analyze and understand data to influence product or business decisions', 
	'None of these activities are an important part of my role at work',
	'Do research that advances the state of the art of machine learning',
	'Build and/or run the data infrasturcture that my business uses for storing, analyzing and operationalizing the data'])
	if 'Building prototypes to explore applying machine learning to new areas' in activity:
		q9_proto=1
	if 'Build and/or run a machine learning service that operationally improves my product or workflows' in activity:
		q9_ml=1
	if 'Analyze and understand data to influence product or business decisions' in activity:
		q9_an=1
	if 'None of these activities are an important part of my role at work' in activity:
		q9_nota=1
	if 'Do research that advances the state of the art of machine learning' in activity:
		q9_do=1
	if 'Build and/or run the data infrasturcture that my business uses for storing, analyzing and operationalizing the data' in activity:
		q9_data=1
	return q9_proto,q9_ml,q9_an,q9_nota,q9_do,q9_data
q9_proto,q9_ml,q9_an,q9_nota,q9_do,q9_data = get_activity()


note = st.selectbox('10. Which of the following hosted notebooks have you used at work or school in the last 5 years?',('Amazon web services','Microsoft azure', 'Google cloud platform','IBM cloud','I have not used any cloud providers'))
q10_aws=q10_ms=q10_gcp=q10_ibm=q10_idk=0
if note =='Amazon web services':
	q10_aws=1
elif note =='Microsoft azure':
	q10_ms=1
elif note =='Google cloud platform':
	q10_gcp=1
elif note == 'IBM cloud':
	q10_ibm=1
else:
	q10_idk=1


def get_languages():
	q11_r=q11_php=q11_java=q11_bash=q11_js=q11_chash=q11_matlab=q11_sql=q11_python=q11_cpp=q11_vb=q11_sas=0
	languages=st.multiselect('11. What programming language do you use on a regular basis?',['R', 'PHP', 'Java','Bash','JavaScript','C#','MATLAB','SQL','Python','C++','VB','SAS'])
	if 'R' in languages:
		q11_r=1
	if 'PHP' in languages:
		q11_php=1
	if 'Java' in languages:
		q11_java=1
	if 'Bash' in languages:
		q11_bash=1
	if 'JavaScript' in languages:
		q11_js=1
	if 'C#' in languages:
		q11_chash=1
	if 'MATLAB' in languages:
		q11_matlab=1
	if 'SQL' in languages:
		q11_sql=1
	if 'Python' in languages:
		q11_python=1
	if 'C++' in languages:
		q11_cpp=1
	if 'VB' in languages:
		q11_vb=1
	if 'SAS' in languages:
		q11_sas=1
	return q11_r,q11_php,q11_java,q11_bash,q11_js,q11_chash,q11_matlab,q11_sql,q11_python,q11_cpp,q11_vb,q11_sas
q11_r,q11_php,q11_java,q11_bash,q11_js,q11_chash,q11_matlab,q11_sql,q11_python,q11_cpp,q11_vb,q11_sas= get_languages()
	

time = st.selectbox('12. What percent of your time at work or school is spent actively coding?', ('1 to 25', '26 to 49', '50 to 74','75 to 99'))
q12_first=q12_second=q12_third=q12_fourth=0
if time =='1 to 25':
	q12_first=1
elif time =='26 to 49':
	q12_second=1
elif time=='50 to 74':
	q12_third=1
else:
	q12_fourth=1


def get_datatype():
	q13_genetic=q13_video=q13_geo=q13_time=q13_tabular=q13_categorical=q13_image=q13_text=q13_sensor=q13_numerical=0
	datatype=st.multiselect('13. Which type of data do you currently interact with most often at work or school?',['Genetic', 'Video', 'Geospatial','TimeSeries','Tabular','Categorical','Image','Text','Sensor','Numerical'])
	if 'Genetic' in datatype:
		q13_genetic=1
	if 'Video' in datatype:
		q13_video=1
	if 'Geospatial' in datatype:
		q13_geo=1
	if 'TimeSeries' in datatype:
		q13_time=1
	if 'Tabular' in datatype:
		q13_tabular=1
	if 'Categorical' in datatype:
		q13_categorical=1
	if 'Image' in datatype:
		q13_image=1
	if 'Text' in datatype:
		q13_text=1
	if 'Sensor' in datatype:
		q13_sensor=1
	if 'Numerical' in datatype:
		q13_numerical=1
	return q13_genetic,q13_video,q13_geo,q13_time,q13_tabular,q13_categorical,q13_image,q13_text,q13_sensor,q13_numerical
q13_genetic,q13_video,q13_geo,q13_time,q13_tabular,q13_categorical,q13_image,q13_text,q13_sensor,q13_numerical = get_datatype()


metrics = st.selectbox('14. What metrics do you or your organization use to determine whether or not your models were successful?', ('Not Applicable', 'Revenue Goals', 'Unfair Bias','Accuracy'))
q14_na=q14_revenue=q14_unfair=q14_accuracy=0
if metrics=='Not Applicable':
	q14_na=1
elif metrics=='Revenue Goals':
	q14_revenue=1
elif metrics=='Unfair Bias':
	q14_unfair=1
else:
	q14_accuracy=1


# Model intercept
INTERCEPT = 0.9131248369325842
# Model coefficients
COEFS = [['q1', 'q1_female', -0.3487355484270125],
         ['q2', 'q2_18_21', -1.96234161804328],
         ['q2', 'q2_22_24', -2.3605128416317713],
         ['q2', 'q2_25_29', -1.7681263915191143],
         ['q2', 'q2_30_34', -1.0765264779722998],
         ['q2', 'q2_35_39', -0.6665749708008458],
         ['q2', 'q2_40_44', -0.31653960542380233],
         ['q3', 'q3_china', -0.4493864978563702],
         ['q3', 'q3_india', -0.09594103439318508],
         ['q3', 'q3_united_', 2.4816988643437266],
         ['q4', 'q4_bachelo', -0.14728755526917045],
         ['q4', 'q4_doctora', 0.3274722766953135],
         ['q6', 'q6_data_an', -0.7596010957738204],
         ['q6', 'q6_data_sc', 0.056568150906102344],
         ['q6', 'q6_other', 0.0020903459322821473],
         ['q6', 'q6_researc', -0.14536493362328776],
         ['q6', 'q6_softwar', 0.08177628665972585],
         ['q6', 'q6_student', -1.2972552074172683],
         ['q7', 'q7_academi', -1.0044159736971054],
         ['q7', 'q7_account', 0.46224990078193257],
         ['q7', 'q7_compute', 0.18616785994960353],
         ['q7', 'q7_other', 0.49675347231980665],
         ['q8', 'q8_0_1', -1.3012204894501347],
         ['q8', 'q8_1_2', -1.1495246761664337],
         ['q8', 'q8_10_15', -0.353939906911341],
         ['q8', 'q8_2_3', -0.8573376032119822],
         ['q8', 'q8_3_4', -0.8898373383852489],
         ['q8', 'q8_4_5', -0.6092232497874794],
         ['q8', 'q8_5_10', -0.6010654365051905],
         ['q10', 'q10_i_do_n', -0.3725363104261915],
         ['q10', 'q10_no_we_', -0.4397044643326389],
         ['q10', 'q10_we_are', 0.14761014636121658],
         ['q10', 'q10_we_hav', 0.9341870620554303],
         ['q10', 'q10_we_rec', 0.4302958909459399],
         ['q10', 'q10_we_use', 0.3325263754576947],
         ['q11', 'q11_analyz', 0.04545328524768237],
         ['q11', 'q11_run_a_', 0.22418811492138116],
         ['q11', 'q11_run_th', -0.07540616948629499],
         ['q11', 'q11_build_', 0.3939979674366195],
         ['q11', 'q11_do_res', -0.06122823732398035],
         ['q11', 'q11_none_o', -0.09443949382473273],
         ['q15', 'q15_google', 0.0930315778686908],
         ['q15', 'q15_amazon', 0.4620929360142492],
         ['q15', 'q15_micros', 0.058766556800380274],
         ['q15', 'q15_ibm_cl', -0.2461194661063596],
         ['q16', 'q16_python', -0.139599938665869],
         ['q16', 'q16_r', -0.002571752026494642],
         ['q16', 'q16_sql', -0.051524904285054636],
         ['q16', 'q16_bash', 0.15613492086131672],
         ['q16', 'q16_java', 0.07666488607408702],
         ['q16', 'q16_javasc', 0.13443301950406103],
         ['q16', 'q16_visual', -0.09473752856781227],
         ['q16', 'q16_c_c_', -0.1469888922508943],
         ['q16', 'q16_matlab', -0.17038441322568842],
         ['q16', 'q16_c_net', -0.06339291807790341],
         ['q16', 'q16_php', 0.023269809082284647],
         ['q16', 'q16_sas_st', -0.1300851926427114],
         ['q23', 'q23_1_to_2', -0.6038743873852727],
         ['q23', 'q23_25_to_', -0.48497736256300555],
         ['q23', 'q23_50_to_', -0.631095859036816],
         ['q23', 'q23_75_to_', -0.6527586235843719],
         ['q31', 'q31_catego', 0.012448920089331806],
         ['q31', 'q31_geneti', 0.46623462900414536],
         ['q31', 'q31_geospa', 0.17738304917730824],
         ['q31', 'q31_image_', -0.0623543665932586],
         ['q31', 'q31_numeri', -0.159038939529615],
         ['q31', 'q31_sensor', 0.028839641018403677],
         ['q31', 'q31_tabula', 0.04376858153442275],
         ['q31', 'q31_text_d', -0.028876893560396064],
         ['q31', 'q31_time_s', 0.18547779152780786],
         ['q31', 'q31_video_', 0.3513026206164099],
         ['q42', 'q42_revenu', 0.38556433196821505],
         ['q42', 'q42_accura', -0.19619994752137193],
         ['q42', 'q42_unfair', 0.025441298917100987],
         ['q42', 'q42_not_ap', 0.163173334930764]]



li = [q1_female,q2_one,q2_two,q2_three,q2_four,q2_five,q2_six,
q3_ch,q3_ind,q3_usa,q4_b,q4_d,
q5_da,q5_ds,q5_o,q5_rs,q5_se,q5_s,
q6_ae,q6_af,q6_c,q6_o,q7_first,q7_second,q7_seventh,q7_third,
q7_fourth,q7_fifth,q7_sixth,
q8_idk,q8_no,q8_weare,q8_wehave,q8_werec,q8_weonly,
q9_an,q9_ml,q9_data,q9_proto,q9_do,q9_nota,
q10_gcp,q10_aws,q10_ms,q10_ibm,q11_python,q11_r,q11_sql,
q11_bash,q11_java,q11_js,q11_vb,q11_cpp,q11_matlab,q11_chash,
q11_php,q11_sas,q12_first,q12_second,q12_third,q12_fourth,
q13_categorical,q13_genetic,q13_geo,q13_image,q13_numerical,
q13_sensor,q13_tabular,q13_text,q13_time,q13_video,
q14_revenue,q14_accuracy,q14_unfair,q14_na]


def calculate_score(input_data):
	result = COEFS.copy()
	
	for i in range(len(result)):
		result[i].append(input_data[i])

	for idx, row in enumerate(COEFS):
		result[idx].append(row[2] * row[-1])
	
	score = INTERCEPT
	for row in result:
		score += row[-1]

	return normalize(score)

if st.button('Submit'):
	score = calculate_score(li)
	proba = calc_proba(score)
	li = {'input_data': li,
		'score': score,
		'proba': proba}
	st.success('Form succesfully submitted!')
	
	my_bar = st.progress(0)
	for percent_complete in range(100):
		tm.sleep(0.05)
		my_bar.progress(percent_complete+1)
	my_bar.empty()
	st.balloons()
	score = int(score)
	
	if score<200:
		new_salary='20,000 to 30,000'
	elif score>=300 and score<300:
		new_salary='30,000 to 40,000'
	elif score>=300 and score<400:
		new_salary='40,000 to 50,000'
	elif score>=400 and score<500:
		new_salary='50,000 to 60,000'
	elif score>=500 and score<600:
		new_salary='60,000 to 70,000'
	elif score>=600 and score<700:
		new_salary='70,000 to 80,000'
	elif score>=700 and score<800:
		new_salary='80,000 to 90,000'
	elif score>=800 and score<900:
		new_salary='90,000 to 100,000'
	else:
		new_salary='more than 100,000'
	
	st.markdown('##')
	st.write("Hi", name, ", your predicted score out of 1000 is", score, "and percentage chances of earning $100,000 per year with this score is",proba)
	st.write('Furthermore, upon recruitment your range of salary could be',new_salary,'USD')	
	fig1 = plt.figure()
	new_score = (score*100) + 10000
	st.write('The graph below shows the average salary of a Data Scientist in USD and your predicted salary after running through your profile:')
	st.markdown('#')
	fig = plt.figure()
	avg = 100000
	ax = fig.add_axes([0,0,1,1])
	ax.set_ylabel("Salary in USD")
	people = ['Average salary', 'Your salary']
	sal = [avg,new_score]
	ax.bar(people,sal,color=['#148F77','#D68910'])
	st.write(fig)
	st.write("")
	st.subheader("Thank you for using ISP!")
