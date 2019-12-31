# -*- coding: utf-8 -*-
# MLToolkit (mltoolkit)

__name__="mltk"

"""
MLToolkit - a verstile helping library for machine learning
===========================================================
'MLToolkit' is a Python package providing a set of user-friendly functions to 
help building machine learning models in data science research or production 
focused projects. It is compatible with and interoperate with popular data 
analysis, manipulation and machine learning libraries Pandas, Sci-kit Learn, 
Tensorflow, Statmodels, Catboost, XGboost, etc.

Main Features
-------------
- Data Extraction (SQL, Flatfiles, etc.)
- Exploratory data analysis (statistical summary, univariate analysis, etc.)
- Feature Extraction and Engineering
- Model performance analysis and comparison between models
- Hyper parameter tuning
- Auto ML (automated machine learning)
- Serving models via RESTful  API

Author
------
- Sumudu Tennakoon

Links
-----
Website: http://sumudu.tennakoon.net/projects/MLToolkit
Github: https://github.com/sptennak/MLToolkit

License
-------
Apache License, Version 2.0 (http://www.apache.org/licenses/LICENSE-2.0)
"""

from datetime import datetime
import gc
import traceback
import gc
import os
import copy
from timeit import default_timer as timer
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import re
import warnings
warnings.filterwarnings("ignore")

from mltk.matrics import *
from mltk.deploy import *

class MLModel():
    def __init__(self, model_attributes, model_parameters, sample_attributes, model_variables, target_variable, score_parameters, model_interpretation, model_evaluation, model_object=None):
        self.model_attributes = model_attributes
        self.model_parameters = model_parameters
        self.sample_attributes=sample_attributes
        self.model_variables = model_variables
        self.target_variable = target_variable
        self.score_parameters = score_parameters
        self.model_interpretation=model_interpretation
        self.model_evaluation = model_evaluation
        self.model_object = model_object
    
    def set_model_object(self, model_object):
        self.model_object = model_object     
        
    def get_identifier_variables(self):
        return self.sample_attributes['RecordIdentifiers']
        
    def get_target_variable(self):
        return self.target_variable
    
    def get_model_variables(self):
        return self.model_variables
    
    def get_model_name(self):
        return self.model_attributes['ModelName']

    def get_model_id(self):
        return self.model_attributes['ModelID']
        
    def get_score_parameter(self, variable):
        return self.score_parameters[variable]

    def get_score_variable(self):
        return self.score_parameters['ScoreVariable']
		
    def get_score_label(self):
        return self.score_parameters['ScoreLabel']
        
    def get_robustness_table(self):
        return self.model_evaluation['RobustnessTable']

    def get_roc_curve(self):
        return self.model_evaluation['ROCCurve']

    def get_precision_recall_curve(self):
        return self.model_evaluation['PrecisionRecallCurve']
    
    def get_auc(self):
        return self.model_evaluation['AUC']
    
    def set_score_edges(self, edges):
        self.score_parameters['Edges']=edges
 
    def get_model_manifest(self, save=False, save_path=''):       
        import json
        model_manifest= {'model_attributes':self.model_attributes,
                        'model_parameters':self.model_parameters,
                        'sample_attributes':self.sample_attributes,            
                        }        
        if save==True:
            json_object = json.dumps(model_manifest)          
            f = open(os.path.join(SavePath, '{}_ModelManifest.json'.format(self.get_model_id())),'w')
            f.write(json_object)
            f.close() 

        return model_manifest
    
    def plot_eval_matrics(self, figure=0, comparison=False):
        import matplotlib.pyplot as plt
        from matplotlib import colors #For custom color maps
        
        description = self.get_model_id()
        
        auc = self.get_auc()
        
        plt.figure(figure, figsize=(8, 6), dpi=80)
        
        ax0 = plt.subplot(231) 
        ROCCurve = self.get_roc_curve()
        plt.plot(ROCCurve.FPR.values, ROCCurve.TPR.values, linestyle='-', label='{} (area = {:.2f}) '.format(description, auc))
        plt.plot([0, 1], [0, 1], color='black', linestyle='--')
        plt.xlim([0.0, 1.0])
        plt.ylim([0.0, 1.05])
        plt.xlabel('False Positive Rate')
        plt.ylabel('True Positive Rate')
        plt.title('ROC')
        plt.legend(loc="lower right")
        plt.show()
        
        ax1 = plt.subplot(234) 
        PrecisionRecallCurve = self.get_precision_recall_curve()
        plt.plot(PrecisionRecallCurve['Recall'].values, PrecisionRecallCurve['Precision'].values, linestyle='-', label='{}'.format(description))
        plt.legend()
        plt.xlabel('Recall')
        plt.ylabel('Precision')
        plt.title('Precision-Recall Curve')
        plt.ylim([0.0, 1.05])
        plt.xlim([0.0, 1.0])
        
        ax2 = plt.subplot(232, sharey=ax1)
        plt.plot(PrecisionRecallCurve['Threshold'].values, PrecisionRecallCurve['Precision'].values, linestyle='-', label='{}'.format(description))
        #plt.plot(thresholds, recall[:-1], 'o-', label='{} recall'.format(description))
        plt.legend()
        plt.xlabel('Threshold')
        plt.ylabel('Precision')
        plt.title('Precision vs. Threshold Curve')
        plt.ylim([0.0, 1.05])
        plt.xlim([0.0, 1.0])
    
        ax3 = plt.subplot(233, sharex=ax2)
        RobustnessTable = self.get_robustness_table().copy()[:-1]
        #plt.plot(thresholds, precision[:-1], 'o-', label='{} precision'.format(description))
        plt.plot(RobustnessTable['max{}'.format(self.get_score_parameter('ScoreVariable'))], RobustnessTable['CumulativeBucketFraction'], linestyle='-', label='{}'.format(description)) #, marker='o'
        plt.legend()
        plt.xlabel('Threshold')
        plt.ylabel('Bucket Fraction')
        plt.title('Bucket Fraction vs. Threshold Curve')
        plt.ylim([0.0, 1.05])
        plt.xlim([0.0, 1.0])
        
        ax4 = plt.subplot(235, sharex=ax2)
        #plt.plot(thresholds, precision[:-1], 'o-', label='{} precision'.format(description))
        plt.plot(PrecisionRecallCurve['Threshold'].values, PrecisionRecallCurve['Recall'].values, linestyle='-', label='{}'.format(description))
        plt.legend()
        plt.xlabel('Threshold')
        plt.ylabel('Recall')
        plt.title('Recall vs. Threshold Curve')
        plt.ylim([0.0, 1.05])
        plt.xlim([0.0, 1.0])
 
        ax5 = plt.subplot(236)
        x_column = 'mean{}'.format(self.get_score_parameter('ScoreVariable'))
        y_column = 'BucketPrecision'
        size_column = 'ResponseFraction' 
        
        plt.plot([0, 1], [0, 1], color='black', linestyle='--')
        plt.xlabel(x_column)
        plt.ylabel(y_column)
        plt.title('Model Charateristics \n ResponseFraction ~ Marker size')
        plt.ylim([0.0, 1.05])
        plt.xlim([0.0, 1.0])
        size_scale=2000 
        size_offset=1      		
        if comparison:
            plt.scatter(RobustnessTable[x_column], RobustnessTable[y_column], s=size_offset+RobustnessTable[size_column].values*size_scale, label='{}'.format(description))
            plt.legend()
        else:
            color_column = 'BucketFraction'
            color_scale=100
            #plt.plot(thresholds, precision[:-1], 'o-', label='{} precision'.format(description))
            bounds = np.array([0.0, 0.3, 0.5, 1.0, 2.0, 5.0, 10.0, 20.0, 25.0, 50.0])
            norm = colors.BoundaryNorm(boundaries=bounds, ncolors=256)
            RobustnessTable.sort_values(by=size_column, ascending=False, inplace=True)
            plt.scatter(RobustnessTable[x_column], RobustnessTable[y_column], c=RobustnessTable[color_column].values*color_scale, s=size_offset+RobustnessTable[size_column].values*size_scale, cmap='nipy_spectral', norm=norm, marker='s')
            cbar = plt.colorbar()
            cbar.set_label(color_column)  

        plt.subplots_adjust(hspace=0.4)
        #plt.show()

def load_tensorflow_model(file_path):
    from tensorflow import keras 
    model = keras.models.load_model(file_path)
    return model
        
def load_object(file_name):
    import pickle
    pickle_in = open(file_name,'rb')
    print('Loading model from file {}'.format(file_name))
    object = pickle.load(pickle_in)
    pickle_in.close()
    return object

def save_object(object_to_save, file_name):
    import pickle
    pickle_out = open(file_name,'wb')
    print('Saving model to file {}'.format(file_name))
    pickle.dump(object_to_save, pickle_out)
    pickle_out.close()

def save_model(Model, file_path):
    """
    Parameters
    ----------
    Model : mltk.MLModel
        MLModel Object
    file_path : str, dafault ''
        Path to file including the file name.    
    
    Returns
    -------
    None
    """
    if Model.model_parameters['MLAlgorithm']=='NN':
        Model.model_object.save(os.path.splitext(file_path)[0]+'.tfh5')
        Model.set_model_object(None)       
    save_object(Model, file_path)

def load_model(file_path):
    """
    Parameters
    ----------
    file_path : str, dafault ''
        Path to file including the file name.    
    
    Returns
    -------
    Model : mltk.MLModel
        MLModel Object
    """
    Model = load_object(file_path)
    if Model.model_parameters['MLAlgorithm']=='NN':
        model = load_tensorflow_model(os.path.splitext(file_path)[0]+'.tfh5')
        Model.set_model_object(model)
    return Model
	
def build_logit_model(x_train, y_train, model_variables, target_variable, model_parameters):
    import statsmodels as sm
    import statsmodels.discrete.discrete_model as sm
    import statsmodels.api as smapi
    
    maxiter=model_parameters['MaxIterations']    
    model=smapi.Logit(y_train, x_train)
    
    startTime = timer()  
    model=model.fit(maxiter=maxiter)
    model_fit_time = timer() - startTime
    
    output = model.summary(xname=list(model_variables))
        
    return model, output, model_fit_time

def stack_tf_layers_sequential(architecture, print_summary=False):
    """
    Parameters
    ----------
    architecture : dict
        list of layers
    print_summary : bool, default False
        prints model summary if True
        
    Returns
    -------
    model : keras.engine.sequential.Sequential
        Keras Sequential model object
    """
    
    from tensorflow.keras.models import Sequential
    from tensorflow.keras.layers import Dense, Dropout, Conv2D, MaxPooling2D, MaxPooling1D, Flatten
    
    model = Sequential()
    
    for key, layer in architecture.items():
        if layer['type']=='Dense':
            if layer['position']=='input':
                model.add(Dense(units=layer['units'], activation=layer['activation'], input_shape=layer['input_shape']))
            elif layer['position']=='hidden':
                model.add(Dense(units=layer['units'], activation=layer['activation']))
            elif layer['position']=='output':
                model.add(Dense(units=layer['units'], activation=layer['activation'])) #, output_shape=layer['output_shape']
        elif layer['type']=='Dropout': 
             model.add(Dropout(rate=layer['rate']))   
        elif layer['type']=='Conv2D':
            if layer['position']=='input':
                model.add(Conv2D(filters=layer['filters'], kernel_size=layer['kernel_size'], strides=layer['strides'], padding=layer['padding'], data_format='channels_last', activation=layer['activation'], input_shape=layer['input_shape'])) #, strides=(2, 2)
            elif layer['position']=='hidden':
                model.add(Conv2D(filters=layer['filters'], kernel_size=layer['kernel_size'], strides=layer['strides'], padding=layer['padding'], data_format='channels_last', activation=layer['activation'])) #, strides=(2, 2)
        elif layer['type']=='MaxPooling2D':
                model.add(MaxPooling2D(pool_size=layer['pool_size'], strides=None, padding=layer['padding'], data_format='channels_last'))
        elif layer['type']=='MaxPooling1D':
                model.add(MaxPooling1D(pool_size=layer['pool_size'], strides=None, padding=layer['padding'], data_format='channels_last'))
        elif layer['type']=='Flatten':
                model.add(Flatten())
    
    if print_summary:
        model.summary()
                
    return model
    
def build_nn_model(x_train, y_train, x_validate, y_validate, model_variables, target_variable, model_parameters):
    import tensorflow as tf
    import tensorflow.keras as keras
    #from tensorflow.keras.models import Sequential
    #from tensorflow.keras.layers import Dense, Dropout

    #tf.enable_eager_execution()
    
    batch_size = model_parameters['BatchSize']
    #input_shape = model_parameters['InputShape']
    epochs = model_parameters['Epochs']   
    metrics = model_parameters['metrics']    
    num_classes = model_parameters['num_classes']      
    architecture = model_parameters['architecture']
    
    y_train = keras.utils.to_categorical(y_train, num_classes)
    y_validate = keras.utils.to_categorical(y_validate, num_classes)
    
    ###########################################################################    
    model = stack_tf_layers_sequential(architecture)
    model.summary()  
    ###########################################################################
    
    model.compile(loss=keras.losses.categorical_crossentropy,
                  optimizer=keras.optimizers.Adadelta(), #keras.optimizers.RMSprop(),
                  metrics=metrics) #['accuracy']

    # Create Tensorflow Session
    sess = tf.Session(config=tf.ConfigProto(intra_op_parallelism_threads=0, inter_op_parallelism_threads=0, log_device_placement=True)) #device_count={'GPU': 0}, 
    keras.backend.set_session(sess)
    
    startTime = timer()
    hist = model.fit(x_train, y_train,
                        batch_size=batch_size,
                        epochs=epochs,
                        verbose=1,
                        validation_data=(x_validate, y_validate))
    model_fit_time = timer() - startTime
    
    output = pd.DataFrame(data = hist.history)
    
    score = model.evaluate(x_validate, y_validate, verbose=1)
    print('Test loss:', score[0])
    print('Test accuracy:', score[1])
       
    return model, output, model_fit_time
    
    
def build_rf_model(x_train, y_train, model_variables, target_variable, model_parameters):
    from sklearn.ensemble import RandomForestClassifier
    
    NTrees = model_parameters['NTrees']
    MaxDepth = model_parameters['MaxDepth']
    Processors = model_parameters['Processors']
    MinSamplesToSplit = model_parameters['MinSamplesToSplit']
    model = RandomForestClassifier(n_estimators=NTrees, max_depth=MaxDepth, n_jobs=Processors, verbose=1, min_samples_split=MinSamplesToSplit)

    startTime = timer()      
    model.fit(x_train, y_train)  
    model_fit_time = timer() - startTime
    
    Importances = model.feature_importances_
    stdev = np.std([tree.feature_importances_ for tree in model.estimators_], axis=0)    
    output = pd.DataFrame({'Features':model_variables, 'Importances':Importances, 'stdev':stdev}).sort_values(by='Importances', ascending=False)       
        
    return model, output, model_fit_time


def build_ml_model(TrainDataset, ValidateDataset, TestDataset, model_variables, target_variable, 
                 model_attributes, sample_attributes, model_parameters, score_parameters,
                   return_model_object=False, show_results=False, show_plot=False):
    """
    Parameters
    ----------
    TrainDataset : pandas.DataFrame
    ValidateDataset : pandas.DataFrame
    TestDataset : pandas.DataFrame
    model_variables : dict
    target_variable : dict 
    model_attributes : dict
    sample_attributes : dict
    model_parameters : dict
    score_parameters : dict
    return_model_object : bool, default False
    show_results : bool, default False
    show_plot : bool, default False
    
    Returns
    -------
    Model : mltk.MLModel
        MLModel Object
    """
    ###############################################################################
    # Create deep copies of each dictionary
    model_variables = copy.deepcopy(model_variables)
    target_variable = copy.deepcopy(target_variable)
    model_attributes = copy.deepcopy(model_attributes)
    sample_attributes = copy.deepcopy(sample_attributes)
    model_parameters = copy.deepcopy(model_parameters)
    score_parameters = copy.deepcopy(score_parameters)
    ###############################################################################
    # TRAIN DATASET
    x_train = TrainDataset[model_variables].values
    print('Train samples: {} loded...'.format(x_train.shape[0]))

    y_train = TrainDataset[target_variable].values
    y_train_act = y_train
    ###############################################################################
    # VALIDATE DATASET
    x_validate = ValidateDataset[model_variables].values
    print('Validate samples: {} loded...'.format(x_validate.shape[0]))

    y_validate = ValidateDataset[target_variable].values
    y_validate_act = y_validate
    ###############################################################################
    # TEST DATASET
    x_test = TestDataset[model_variables].values
    print('Test samples: {} loded...'.format(x_test.shape[0]))

    y_test = TestDataset[target_variable].values
    y_test_act = y_test
    ###############################################################################
    
    model_interpretation={}

    model_evaluation={}
    
    # ModelAttributes 
    model_attributes['BuiltTime'] = datetime.now().strftime('%Y%m%d%H%M%S')
    model_attributes['ModelID'] = model_attributes['ModelName'].replace(' ', '').upper()+model_parameters['MLAlgorithm'].replace(' ', '').upper()+model_attributes['BuiltTime']  
    model_attributes['ModelFitTime']=-1

    # SampleAttribues
    RecordIdentifiers = sample_attributes['RecordIdentifiers']
    sample_attributes['TrainSize'] = len(TrainDataset.index)
    sample_attributes['ValidateSize'] = len(ValidateDataset.index)
    sample_attributes['TestSize'] = len(TestDataset.index)
	#
    sample_attributes['TrainValidateTestRatio'] = '{}'.format(np.round(np.array([sample_attributes['TrainSize'],sample_attributes['ValidateSize'],sample_attributes['TestSize']])/(sample_attributes['TrainSize']+sample_attributes['ValidateSize']+sample_attributes['TestSize']),2))
    sample_attributes['TrainResponseRate'] = len(TrainDataset.loc[TrainDataset[target_variable]==1].index)/sample_attributes['TrainSize'] 
    sample_attributes['ValidateResponseRate'] = len(ValidateDataset.loc[ValidateDataset[target_variable]==1].index)/sample_attributes['ValidateSize']
    sample_attributes['TestResponseRate'] = len(TestDataset.loc[TestDataset[target_variable]==1].index)/sample_attributes['TestSize'] 

    # ScoreParameters
    edges = score_parameters['Edges']
    quantiles = score_parameters['Quantiles']
    quantile_label = score_parameters['QuantileLabel']
    score_variable=score_parameters['ScoreVariable']
    score_label=score_parameters['ScoreLabel']
    
    ###############################################################################
    print(model_attributes)
    print(model_parameters)
    print(sample_attributes)
    print(score_parameters)
    ###############################################################################
    
    ml_algorithm = model_parameters['MLAlgorithm']
    
    if ml_algorithm=='LGR':
        ###############################################################################
        import statsmodels
        model_attributes['MLTool'] = 'statsmodels={}'.format(statsmodels.__version__) 
        # Logit Model
        model, summary, model_fit_time = build_logit_model(x_train, y_train, model_variables, target_variable, model_parameters)
        model_interpretation['ModelSummary'] = summary    

#        y_pred_prob = model.predict(x_validate)
#        ValidateDataset[score_variable]=y_pred_prob
        
        y_pred_prob = model.predict(x_test)
        TestDataset[score_variable]=y_pred_prob
        ###############################################################################
        
    elif ml_algorithm=='RF':
        ###############################################################################
        import sklearn
        model_attributes['MLTool'] = 'sklearn={}'.format(sklearn.__version__) 
        # Random Forest Model
        model, summary, model_fit_time= build_rf_model(x_train, y_train, model_variables, target_variable, model_parameters)
        model_interpretation['ModelSummary'] = summary  
        
#        y_pred_prob = model.predict(x_validate)
#        ValidateDataset[score_variable]=y_pred_prob
        
        y_pred_prob = model.predict_proba(x_test)[:,1]
        TestDataset[score_variable]=y_pred_prob
        ###############################################################################
        
    elif ml_algorithm=='NN':
        ###############################################################################
        import tensorflow
        import tensorflow.keras
        model_attributes['MLTool'] = 'tensorflow={}; keras={}'.format(tensorflow.__version__, tensorflow.keras.__version__) 
        # Deep Feed Forward Model using TensorFlow
        model, summary, model_fit_time= build_nn_model(x_train, y_train, x_validate, y_validate, model_variables, target_variable, model_parameters)
        model_interpretation['ModelSummary'] = summary  
        
#        y_pred_prob = model.predict(x_validate)
#        ValidateDataset[score_variable]=y_pred_prob
        
        y_pred_prob = model.predict(x_test, verbose=1, batch_size=model_parameters['BatchSize'])[:,1]
        TestDataset[score_variable]=y_pred_prob
        ###############################################################################     
    else:
        raise Exception('No ML Algorithm is given!')
        
    ############################################################################### 
    model_evaluation['RobustnessTable'], model_evaluation['ROCCurve'], model_evaluation['PrecisionRecallCurve'], model_evaluation['AUC'] = model_performance_matrics(TestDataset, target_variable=target_variable, score_variable=score_variable, quantile_label=quantile_label,  quantiles=quantiles, show_plot=show_plot)        
    if show_results:
        print(model_evaluation['RobustnessTable'])
    ###############################################################################
    
    ###############################################################################
    if return_model_object:
        Model = MLModel(model_attributes, model_parameters, sample_attributes, model_variables, target_variable, 
                        score_parameters, model_interpretation, model_evaluation, model_object=model)
    else:
        Model = MLModel(model_attributes, model_parameters, sample_attributes, model_variables, target_variable, 
                        score_parameters, model_interpretation, model_evaluation, model_object=None)
    ###############################################################################   
    # Cleanup memeory
    gc.collect()
    
    #return copy.deepcopy(Model)
    return Model
	
def confusion_matrix_comparison(DataFrame, Models, thresholds=0.5, score_variable=None, save_prediction=False, show_plot=False):
    """
    Parameters
    ----------
    DataFrame : pandas.DataFrame
        DataFrame
    Models : 
    thresholds : int or list(int), default 0.5    
    score_variable : str, optional, dafault None
        Name of the variable where the score is based on.  If None, score variabel is assigned by the model      
    save_prediction: bool, default False
        Retains prediction in column named by Model ID
    show_plot : bool, default False
        plot results if True

    Returns
    -------
    ConfusionMatrixComparison : pandas.DataFrame
    """
    try:
        if len(thresholds)>0:
            thresholds = thresholds        
    except:
        thresholds = [thresholds]
        
    ConfusionMatrixComparison=pd.DataFrame()
    
    for i in range(len(Models)):
        Model = Models[i]
        DataFrame=score_processed_dataset(DataFrame, Model, edges=None, score_label=score_variable, fill_missing=0)
        for threshold in thresholds:            
            model_id = Model.get_model_id()+'_[TH={}]'.format(threshold)    
            target_variable = Model.get_target_variable()
            predict_column = 'Predict'
            DataFrame[predict_column] = np.where(DataFrame[Model.get_score_variable()]>threshold,1,0)
            ConfusionMatrix=confusion_matrix(DataFrame, actual_variable=target_variable, predcted_variable=predict_column, labels=[0,1], sample_weight=None, totals=True)
            ConfusionMatrixComparison=ConfusionMatrixComparison.append(confusion_matrix_to_row(ConfusionMatrix, ModelID=model_id),ignore_index=True) 
            if save_prediction:
                pass
            else:
                DataFrame.drop(columns=[predict_column], inplace=True)
                
    if show_plot:
        ConfusionMatrixComparison[['PPV', 'TPR', 'ACC', 'F1']].plot(kind='bar', subplots=True, figsize=(5,10), legend=False)
    
    return ConfusionMatrixComparison
