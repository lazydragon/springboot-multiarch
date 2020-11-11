#!/usr/bin/env python3

from aws_cdk import core

from pipeline.pipeline_stack import PipelineStack

env = core.Environment(region="us-east-1")

app = core.App()
PipelineStack(app, "pipeline", env=env)

app.synth()
