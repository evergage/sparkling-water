# Sparkling Water 3.36.1.5 Evergage Fork

## Overview

Sparkling Water 3.38 dropped all support for joining the H2O cluster as a "client" member and accessing H2O API's directly. Instead, the H2O REST API must be used for all interactions with the H2O cluster. We are not ready at this time to refactor Everlearn to use the REST API, as it will be a significant amount of work. However, we do need to upgrade to Spark 3.5 in order to run on JDK21, and Sparkling Water 3.36 only supports Spark 3.3, so we decided to fork Sparkling Water 3.36.1 amd backport Spark 3.5 support. Specifically, we cherry-picked the following commits:

* Spark 3.4 support: https://github.com/h2oai/sparkling-water/pull/5620 (deb484a)
* Spark 3.5 support: https://github.com/h2oai/sparkling-water/pull/5664 (9713dfd)

## Build Steps

* build project
```
# build will fail with JDK21, so use JDK11
export JAVA_HOME=/Library/Java/JavaVirtualMachines/amazon-corretto-11.jdk/Contents/Home
# skip tests and building docs, and publish artifacts to local Maven repo
./gradlew publishMavenAllPublicationToMavenLocal -x check -x docJar
```
* update this README file
* tag the release, e.g. RELEASE-3.36.1.5-1-evg3 
* manually publish the following artifacts from ~/.m2/repository/ai/h2o/ to Nexus (publish pom, jar, and sources)
  * sparkling-water-core_2.12
  * sparkling-water-utils_2.12
  * sparkling-water-extensions_2.12
  * sparkling-water-repl_2.12
  * sparkling-water-scoring_2.12

