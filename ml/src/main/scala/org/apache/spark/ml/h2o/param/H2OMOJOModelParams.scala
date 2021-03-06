/*
* Licensed to the Apache Software Foundation (ASF) under one or more
* contributor license agreements.  See the NOTICE file distributed with
* this work for additional information regarding copyright ownership.
* The ASF licenses this file to You under the Apache License, Version 2.0
* (the "License"); you may not use this file except in compliance with
* the License.  You may obtain a copy of the License at
*
*    http://www.apache.org/licenses/LICENSE-2.0
*
* Unless required by applicable law or agreed to in writing, software
* distributed under the License is distributed on an "AS IS" BASIS,
* WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
* See the License for the specific language governing permissions and
* limitations under the License.
*/
package org.apache.spark.ml.h2o.param

import org.apache.spark.ml.param._

/**
  * Parameters available on the MOJO Model
  */
trait H2OMOJOModelParams extends Params {

  //
  // Param definitions
  //
  protected final val predictionCol: Param[String] = new Param[String](this, "predictionCol", "Prediction column name")
  protected final val featuresCols: StringArrayParam = new StringArrayParam(this, "featuresCols", "Name of feature columns")

  protected final val convertUnknownCategoricalLevelsToNa = new BooleanParam(this,
    "convertUnknownCategoricalLevelsToNa",
    "If set to 'true', the model converts unknown categorical levels to NA during making predictions.")

  protected final val namedMojoOutputColumns: Param[Boolean] = new BooleanParam(this, "namedMojoOutputColumns", "Mojo Output is not stored" +
    " in the array but in the properly named columns")

  //
  //
  // Default values
  //
  setDefault(
    featuresCols -> Array.empty[String],
    predictionCol -> "prediction",
    convertUnknownCategoricalLevelsToNa -> false,
    namedMojoOutputColumns -> true)

  //
  // Getters
  //
  def getPredictionCol(): String = $(predictionCol)

  def getFeaturesCols(): Array[String] = $(featuresCols)

  def getConvertUnknownCategoricalLevelsToNa(): Boolean = $(convertUnknownCategoricalLevelsToNa)

  def getNamedMojoOutputColumns(): Boolean = $(namedMojoOutputColumns)

  //
  // Setters
  //
  def setConvertUnknownCategoricalLevelsToNa(value: Boolean): this.type = set(convertUnknownCategoricalLevelsToNa, value)

  def setNamedMojoOutputColumns(value: Boolean): this.type = set(namedMojoOutputColumns, value)
}
