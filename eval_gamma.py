import numpy as np
import itk
import gatetools as gt
import SimpleITK as sitk
import os
import platipy
import pandas as pd
from platipy.imaging.dose.dvh import calculate_dvh_for_labels, calculate_d_cc_x, calculate_d_x, calculate_v_x

translations = [-5, -4, -3, -2, -1, 0, 1, 2, 3, 4, 5]
structure_names =["roi_CTVHR", "roi_CTVRI", "roi_Vessie", "roi_Rectum", "roi_Intestins", "roi_Sigmoide"]
d = {str(t): [] for t in translations}
for translation in translations:
  trans = np.array([-translation, 0, 0])
  trans = trans.astype(float)
  dose = itk.imread("dose.mhd")
  dose_trans = gt.applyTransformation(input=dose, force_resample=True, translation=trans, pad=0, interpolation_mode="linear") 
  itk.imwrite(dose_trans, "dose_translate.mhd")
  itk.imwrite(dose_trans, "dose_translate" + str(translation) + ".mhd")

  dose = sitk.ReadImage("dose_translate.mhd")
  structures = {
      s: sitk.ReadImage(os.path.join("struct", s + ".mhd")) for s in structure_names
  }
  dvh = calculate_dvh_for_labels(dose, structures)
  df_metrics_d = calculate_d_x(dvh, [90, 98])
  df_metrics_d_cc = calculate_d_cc_x(dvh, [2, 0.1])

  d[str(translation)] = [df_metrics_d["D90"][0]*100.0, df_metrics_d["D98"][0]*100.0, df_metrics_d["D90"][1]*100.0, df_metrics_d["D98"][1]*100.0, df_metrics_d_cc["D2cc"][2]*100.0, df_metrics_d_cc["D2cc"][3]*100.0, df_metrics_d_cc["D0.1cc"][3]*100.0, df_metrics_d_cc["D2cc"][4]*100.0, df_metrics_d_cc["D0.1cc"][4]*100.0, df_metrics_d_cc["D2cc"][5]*100.0, df_metrics_d_cc["D0.1cc"][5]*100.0]

df = pd.DataFrame(data=d, index=["roi_CTVHR 90%", "roi_CTVHR 98%", "roi_CTVRI 90%", "roi_CTVRI 98%", "roi_Vessie 2cc", "roi_Rectum 2cc", "roi_Rectum 0.1cc", "roi_Intestins 2cc", "roi_Intestins 0.1cc", "roi_Sigmoide 2cc", "roi_Sigmoide 0.1cc"])
print("translation X (mm)")
print(df)

d = {str(t): [] for t in translations}
for translation in translations:
  trans = np.array([0, -translation, 0])
  trans = trans.astype(float)
  dose = itk.imread("dose.mhd")
  dose_trans = gt.applyTransformation(input=dose, force_resample=True, translation=trans, pad=0, interpolation_mode="linear")
  itk.imwrite(dose_trans, "dose_translate.mhd")
  itk.imwrite(dose_trans, "dose_translate" + str(translation) + ".mhd")

  dose = sitk.ReadImage("dose_translate.mhd")
  structures = {
      s: sitk.ReadImage(os.path.join("struct", s + ".mhd")) for s in structure_names
  }
  dvh = calculate_dvh_for_labels(dose, structures)
  df_metrics_d = calculate_d_x(dvh, [90, 98])
  df_metrics_d_cc = calculate_d_cc_x(dvh, [2, 0.1])

  d[str(translation)] = [df_metrics_d["D90"][0]*100.0, df_metrics_d["D98"][0]*100.0, df_metrics_d["D90"][1]*100.0, df_metrics_d["D98"][1]*100.0, df_metrics_d_cc["D2cc"][2]*100.0, df_metrics_d_cc["D2cc"][3]*100.0, df_metrics_d_cc["D0.1cc"][3]*100.0, df_metrics_d_cc["D2cc"][4]*100.0, df_metrics_d_cc["D0.1cc"][4]*100.0, df_metrics_d_cc["D2cc"][5]*100.0, df_metrics_d_cc["D0.1cc"][5]*100.0]

df = pd.DataFrame(data=d, index=["roi_CTVHR 90%", "roi_CTVHR 98%", "roi_CTVRI 90%", "roi_CTVRI 98%", "roi_Vessie 2cc", "roi_Rectum 2cc", "roi_Rectum 0.1cc", "roi_Intestins 2cc", "roi_Intestins 0.1cc", "roi_Sigmoide 2cc", "roi_Sigmoide 0.1cc"])
print("translation Y (mm)")
print(df)

d = {str(t): [] for t in translations}
for translation in translations:
  trans = np.array([0, 0, -translation])
  trans = trans.astype(float)
  dose = itk.imread("dose.mhd")
  dose_trans = gt.applyTransformation(input=dose, force_resample=True, translation=trans, pad=0, interpolation_mode="linear")
  itk.imwrite(dose_trans, "dose_translate.mhd")
  itk.imwrite(dose_trans, "dose_translate" + str(translation) + ".mhd")

  dose = sitk.ReadImage("dose_translate.mhd")
  structures = {
      s: sitk.ReadImage(os.path.join("struct", s + ".mhd")) for s in structure_names
  }
  dvh = calculate_dvh_for_labels(dose, structures)
  df_metrics_d = calculate_d_x(dvh, [90, 98])
  df_metrics_d_cc = calculate_d_cc_x(dvh, [2, 0.1])

  d[str(translation)] = [df_metrics_d["D90"][0]*100.0, df_metrics_d["D98"][0]*100.0, df_metrics_d["D90"][1]*100.0, df_metrics_d["D98"][1]*100.0, df_metrics_d_cc["D2cc"][2]*100.0, df_metrics_d_cc["D2cc"][3]*100.0, df_metrics_d_cc["D0.1cc"][3]*100.0, df_metrics_d_cc["D2cc"][4]*100.0, df_metrics_d_cc["D0.1cc"][4]*100.0, df_metrics_d_cc["D2cc"][5]*100.0, df_metrics_d_cc["D0.1cc"][5]*100.0]

df = pd.DataFrame(data=d, index=["roi_CTVHR 90%", "roi_CTVHR 98%", "roi_CTVRI 90%", "roi_CTVRI 98%", "roi_Vessie 2cc", "roi_Rectum 2cc", "roi_Rectum 0.1cc", "roi_Intestins 2cc", "roi_Intestins 0.1cc", "roi_Sigmoide 2cc", "roi_Sigmoide 0.1cc"])
print("translation Z (mm)")
print(df)




