import findspark
findspark.init()
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
from pyspark.ml.evaluation import BinaryClassificationEvaluator
from pyspark.ml.classification import LogisticRegression
from pyspark.ml.feature import VectorAssembler
from pyspark.ml.linalg import Vectors
from pyspark.sql import SQLContext
from pyspark import SparkContext, SparkConf
from pyspark.sql.types import DoubleType
from sklearn.metrics import accuracy_score, classification_report, confusion_matrix, roc_auc_score, roc_curve
import time

conf = SparkConf().setAppName(
    "LogisticRegressionModel").setMaster("local")
sc = SparkContext(conf=conf).getOrCreate()


def quiet_logs(sc):
    logger = sc._jvm.org.apache.log4j
    logger.LogManager.getLogger("org"). setLevel(logger.Level.ERROR)
    logger.LogManager.getLogger("akka").setLevel(logger.Level.ERROR)


quiet_logs(sc)

df = pd.read_csv("../in/totalData.csv")
df = df.astype(float)
df = df.dropna()
assembler_inputs = [x for x in df.columns if x != "swing"]
SQLContext = SQLContext(sc)

df = SQLContext.createDataFrame(df)

assembler = VectorAssembler(inputCols=assembler_inputs, outputCol="features")
vecOutput = assembler.transform(df)

# print(vecOutput.select("features"))

train, test = vecOutput.randomSplit([0.8, 0.2], seed=3000)


train_time_start = time.time()
lrModel = LogisticRegression(featuresCol='features',
                        labelCol='swing', maxIter=10).fit(train)
train_time_end = time.time() - train_time_start
print("Training Time (Sec) : ", str(train_time_end))

test_time_start = time.time()
predictions = lrModel.transform(test)
test_time_end = time.time() - test_time_start
print("Testing Time (Sec) : ", str(test_time_end))

label = [int(row.swing) for row in predictions.select("swing").collect()]
pred = [int(row.prediction)
        for row in predictions.select("prediction").collect()]



# pred_proba = np.array([np.array(row.probability)
#             for row in predictions.select("probability").collect()])

# pred_proba = pred_proba[:, 1]

# r_probs = [0 for _ in range(len(label))]

# r_auc = roc_auc_score(label,r_probs)
# lg_auc = roc_auc_score(label, pred_proba)

# r_fpr, r_tpr, _ = roc_curve(label, r_probs)
# lg_fpr, lg_tpr, _ = roc_curve(label, pred_proba)



# #PLOT ROC

# plt.plot(r_fpr, r_tpr, linestyle='--',
#         label='Random Prediction (AUROC = %0.3f)' % r_auc)

# plt.plot(lg_fpr, lg_tpr, linestyle='dotted',
#         label='Logistic Regression  (AUROC = %0.3f)' % lg_auc)

# plt.title("ROC Plot")
# plt.ylabel('False Positive Rate')
# plt.xlabel('True Positive Rate')
# plt.legend()

# print("+++++++++++++++++++++++++++++++++++++++++++++")
# #print Traning Dataset Count
# print("Training Dataset Count: " + str(train.count()))

# #print Test Dataset Count
# print("Test Dataset Count: " + str(test.count()))

# # print accuracy
# print("Accuracy: ", accuracy_score(label, pred))

# # print precision, recall, F1-score per each class
# print(classification_report(label, pred))

# # print confusion matrix
# print("Confusion Matrix: ", confusion_matrix(label, pred))

# #print Random (Chance) Prediction AUROC
# print("Random (Chance) Prediction AUROC : ", r_auc)

# #print Logistic Regression AUROC
# print("Logistic Regression AUROC : ", lg_auc)

# #Show Plot
# plt.show()
# print("+++++++++++++++++++++++++++++++++++++++++++++")
