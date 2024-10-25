#
# Licensed to the Apache Software Foundation (ASF) under one or more
# contributor license agreements.  See the NOTICE file distributed with
# this work for additional information regarding copyright ownership.
# The ASF licenses this file to You under the Apache License, Version 2.0
# (the "License"); you may not use this file except in compliance with
# the License.  You may obtain a copy of the License at
#
#    http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#

"""
Unit tests for MOJO pipelines functionality in PySparkling. We don't start H2O context for these tests to actually tests
that mojo can run without H2O runtime in PySparkling environment
"""

import os
from pyspark.ml import Pipeline, PipelineModel
from pysparkling.ml import H2OMOJOPipelineModel, H2OMOJOSettings


def test_h2o_mojo_pipeline_predictions(prostateDataset):
    # Try loading the Mojo and prediction on it without starting H2O Context
    path = "file://" + os.path.abspath("../ml/src/test/resources/mojo2data/pipeline.mojo")
    settings = H2OMOJOSettings(namedMojoOutputColumns=False)
    mojo = H2OMOJOPipelineModel.createFromMojo(path, settings)

    preds = mojo.transform(prostateDataset).repartition(1)

    normalSelection = preds.select("prediction.preds").take(5)

    assert normalSelection[0][0][0] == 65.36339431549945
    assert normalSelection[1][0][0] == 64.98931238070139
    assert normalSelection[2][0][0] == 64.95047899851251
    assert normalSelection[3][0][0] == 65.78738866816514
    assert normalSelection[4][0][0] == 66.11292243968764

    udfSelection = preds.select(mojo.selectPredictionUDF("AGE")).take(5)

    assert udfSelection[0][0] == 65.36339431549945
    assert udfSelection[1][0] == 64.98931238070139
    assert udfSelection[2][0] == 64.95047899851251
    assert udfSelection[3][0] == 65.78738866816514
    assert udfSelection[4][0] == 66.11292243968764


def test_h2o_mojo_pipeline_predictions_with_named_cols(prostateDataset):
    # Try loading the Mojo and prediction on it without starting H2O Context
    mojo = H2OMOJOPipelineModel.createFromMojo(
        "file://" + os.path.abspath("../ml/src/test/resources/mojo2data/pipeline.mojo"))

    preds = mojo.transform(prostateDataset).repartition(1).select(mojo.selectPredictionUDF("AGE")).take(5)

    assert preds[0][0] == 65.36339431549945
    assert preds[1][0] == 64.98931238070139
    assert preds[2][0] == 64.95047899851251
    assert preds[3][0] == 65.78738866816514
    assert preds[4][0] == 66.11292243968764


def test_feature_types_on_h2o_mojo_pipeline():
    mojo = H2OMOJOPipelineModel.createFromMojo(
        "file://" + os.path.abspath("../ml/src/test/resources/mojo2data/pipeline.mojo"))
    types = mojo.getFeatureTypes()

    assert types["DPROS"] == "Int32"
    assert types["GLEASON"] == "Int32"
    assert types["VOL"] == "Float64"
    assert types["DCAPS"] == "Int32"
    assert types["PSA"] == "Float64"
    assert types["CAPSULE"] == "Int32"
    assert types["RACE"] == "Int32"
    assert types["ID"] == "Int32"
    assert len(types) == 8


def test_mojo_dai_pipeline_serialize(prostateDataset):
    mojo = H2OMOJOPipelineModel.createFromMojo(
        "file://" + os.path.abspath("../ml/src/test/resources/mojo2data/pipeline.mojo"))

    # Create Spark pipeline of single step - mojo pipeline
    pipeline = Pipeline(stages=[mojo])
    pipeline.write().overwrite().save("file://" + os.path.abspath("build/test_dai_pipeline_as_spark_pipeline"))
    loadedPipeline = Pipeline.load("file://" + os.path.abspath("build/test_dai_pipeline_as_spark_pipeline"))

    # Train the pipeline model
    model = loadedPipeline.fit(prostateDataset)

    model.write().overwrite().save("file://" + os.path.abspath("build/test_dai_pipeline_as_spark_pipeline_model"))
    loadedModel = PipelineModel.load(
        "file://" + os.path.abspath("build/test_dai_pipeline_as_spark_pipeline_model"))

    preds = loadedModel.transform(prostateDataset).repartition(1).select(mojo.selectPredictionUDF("AGE")).take(5)

    assert preds[0][0] == 65.36339431549945
    assert preds[1][0] == 64.98931238070139
    assert preds[2][0] == 64.95047899851251
    assert preds[3][0] == 65.78738866816514
    assert preds[4][0] == 66.11292243968764


def testMojoPipelineProtoBackendWithoutError(spark):
    mojo = H2OMOJOPipelineModel.createFromMojo(
        "file://" + os.path.abspath("../ml/src/test/resources/proto_based_pipeline.mojo"))

    data = [(2.0, 'male', 0.41670000553131104, 111361, 6.449999809265137, 'A19'),
            (1.0, 'female', 0.33329999446868896, 110413, 6.4375, 'A14'),
            (1.0, 'female', 0.16670000553131104, 111320, 6.237500190734863, 'A21'),
            (1.0, 'female', 2.0, 111361, 6.237500190734863, 'A20'),
            (3.0, 'female', 1.0, 110152, 6.75, 'A14'),
            (1.0, 'male', 0.666700005531311, 110489, 6.85830020904541, 'A10'),
            (3.0, 'male', 0.33329999446868896, 111320, 0.0, 'A11'),
            (3.0, 'male', 2.0, 110413, 6.85830020904541, 'A24'),
            (1.0, 'female', 1.0, 110489, 3.170799970626831, 'A21'),
            (1.0, 'female', 0.33329999446868896, 111240, 0.0, 'A14')
            ]
    rdd = spark.sparkContext.parallelize(data)
    df = spark.createDataFrame(rdd, ['pclass', 'sex', 'age', 'ticket', 'fare', 'cabin'])
    prediction = mojo.transform(df)
    prediction.collect()


def test_h2o_mojo_pipeline_contributions(spark):
    test_folder = "daiMojoShapley"
    mojo_path = "file://" + os.path.abspath("../ml/src/test/resources/" + test_folder + "/pipeline.mojo")
    data_path = "file://" + os.path.abspath("../ml/src/test/resources/" + test_folder + "/example.csv")

    # request pipeline to provide contribution (SHAP) values
    settings = H2OMOJOSettings(withContributions=True)
    mojo = H2OMOJOPipelineModel.createFromMojo(mojo_path, settings)

    df = spark.read.csv(data_path, header=True, inferSchema=True)
    contributions = mojo.transform(df).select("contributions.*")

    featureColumns = 4
    classes = 3
    bias = 1
    contribution_columns = classes * (featureColumns + bias)

    assert contribution_columns == len(contributions.columns)
    assert all(c.startswith("contrib_") for c in contributions.columns)
