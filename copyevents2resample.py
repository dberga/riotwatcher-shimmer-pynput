import pandas as pd
import os

pre_files = [
	"data_8feb_2023/gsr_events5sec_4K Poppy_session6127260054_samplingrate(Hz)20.768850930477626_TOP_110_True.txt",
	"data_8feb_2023/gsr_events5sec_EnojaDitto_session6097099909_samplingrate(Hz)12.159531477232065_JUNGLE_402_False.txt",
	"data_8feb_2023/gsr_events5sec_Frank DeWitt_session6127260054_samplingrate(Hz)16.91714804332114_BOTTOM_354_True.txt",
	"data_8feb_2023/gsr_events5sec_ivegotflow_session6097099909_samplingrate(Hz)13.732818588588293_MIDDLE_115_False.txt",
	"data_8feb_2023/gsr_events5sec_ivegotflow_session6127260054_samplingrate(Hz)17.810246564156888_UTILITY_116_True.txt",
	"data_8feb_2023/gsr_events5sec_Loxart_session6097099909_samplingrate(Hz)13.823916590341312_BOTTOM_82_False.txt",
	"data_8feb_2023/gsr_events5sec_PELO AVIONETA_session6127260054_samplingrate(Hz)18.835758147541256_JUNGLE_298_True.txt",
	"data_8feb_2023/gsr_events5sec_Rogihrim6_session6097099909_samplingrate(Hz)13.22152079496548_TOP_365_False.txt",
	"data_8feb_2023/gsr_events5sec_Taketagamer_session6097099909_samplingrate(Hz)13.727894372277317_UTILITY_13_False.txt"
]
res_files = [
	"resampled/gsr_4KPoppy_TOP_110_True_GSC_shimmer_resampled.txt",
	"resampled/gsr_EnojaDitto_JUNGLE_402_False_GSC_shimmer_resampled.txt",
	"resampled/gsr_FrankDeWitt_BOTTOM_354_True_GSC_shimmer_resampled.txt",
	"resampled/gsr_ivegotflow_MIDDLE_115_False_GSC_shimmer_resampled.txt",
	"resampled/gsr_ivegotflow_UTILITY_116_True_GSC_shimmer_resampled.txt",
	"resampled/gsr_Loxart_BOTTOM_82_False_GSC_shimmer_resampled.txt",
	"resampled/gsr_PELOAVIONETA_JUNGLE_298_True_GSC_shimmer_resampled.txt",
	"resampled/gsr_Rogihrim6_TOP_365_False_GSC_shimmer_resampled.txt",
	"resampled/gsr_Taketagamer_UTILITY_13_False_GSC_shimmer_resampled.txt"
]

out_folder = "results/"
os.makedirs(out_folder,exist_ok=True)

for i,f in enumerate(pre_files):
	df_pre = pd.read_csv(pre_files[i],sep=' ',header=None)
	df_res = pd.read_csv(res_files[i],sep=",",header=None)

	# add empty column
	df_res[2] = ""
	# add events to df_res
	df_events = df_pre[df_pre[2]>0]
	for index, row in df_events.iterrows():
		timestamp = row[0]
		event = int(row[2]) 
		res_idx = df_res[0].sub(timestamp).abs().idxmin()
		df_res[2][res_idx] = event
	df_res = df_res.set_index(0)
	df_res.to_csv(out_folder+res_files[i].split("/")[1],sep=" ",header=False)


