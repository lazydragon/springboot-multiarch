from aws_cdk import (core, aws_codebuild as codebuild,
                     aws_codecommit as codecommit,
                     aws_codepipeline as codepipeline,
                     aws_codepipeline_actions as codepipeline_actions,
                     aws_lambda as lambda_, aws_s3 as s3,
                     aws_iam as iam, aws_ecr as ecr)

class PipelineStack(core.Stack):

    def __init__(self, scope: core.Construct, id: str, **kwargs) -> None:
        
        super().__init__(scope, id, **kwargs)

        # create ECR
        ecr_repo = ecr.Repository(self, "ECRRep", repository_name="springboot-multiarch")
        
        # create code repo
        code = codecommit.Repository(self, "CodeRep", repository_name="springboot-multiarch")

        # create code builds
        arm_build = codebuild.PipelineProject(self, "ARMBuild",
                        build_spec=codebuild.BuildSpec.from_source_filename("pipeline/armbuild.yml"),
                        environment=codebuild.BuildEnvironment(
                            build_image=codebuild.LinuxBuildImage.AMAZON_LINUX_2_ARM,
                            privileged=True),
                        environment_variables=self.get_build_env_vars(ecr_repo))
        self.add_role_access_to_build(arm_build)
            
        amd_build = codebuild.PipelineProject(self, "AMDBuild",
                        build_spec=codebuild.BuildSpec.from_source_filename("pipeline/amdbuild.yml"),
                        environment=codebuild.BuildEnvironment(
                            build_image=codebuild.LinuxBuildImage.AMAZON_LINUX_2_3,
                            privileged=True),
                        environment_variables=self.get_build_env_vars(ecr_repo))
        self.add_role_access_to_build(amd_build)
        
        post_build = codebuild.PipelineProject(self, "PostBuild",
                        build_spec=codebuild.BuildSpec.from_source_filename("pipeline/post_build.yml"),
                        environment=codebuild.BuildEnvironment(
                            build_image=codebuild.LinuxBuildImage.AMAZON_LINUX_2_3,
                            privileged=True),
                        environment_variables=self.get_build_env_vars(ecr_repo))
        self.add_role_access_to_build(post_build)


        # create pipeline
        source_output = codepipeline.Artifact()
        arm_build_output = codepipeline.Artifact("ARMBuildOutput")
        amd_build_output = codepipeline.Artifact("AMDBuildOutput")
        post_build_output = codepipeline.Artifact("PostBuildOutput")

        codepipeline.Pipeline(self, "Pipeline",
            stages=[
                codepipeline.StageProps(stage_name="Source",
                    actions=[
                        codepipeline_actions.CodeCommitSourceAction(
                            action_name="CodeCommit_Source",
                            repository=code,
                            output=source_output)]),
                codepipeline.StageProps(stage_name="Build",
                    actions=[
                        codepipeline_actions.CodeBuildAction(
                            action_name="ARM_Build",
                            project=arm_build,
                            input=source_output,
                            outputs=[arm_build_output]),
                        codepipeline_actions.CodeBuildAction(
                            action_name="AMD_Build",
                            project=amd_build,
                            input=source_output,
                            outputs=[amd_build_output]),
                            ]),
                codepipeline.StageProps(stage_name="PostBuild",
                    actions=[
                        codepipeline_actions.CodeBuildAction(
                            action_name="Post_Build",
                            project=post_build,
                            input=source_output,
                            outputs=[post_build_output])
                            ]),
                #codepipeline.StageProps(stage_name="Deploy", actions=[]),
            ])
    
    def add_role_access_to_build(self, build):
        build.role.add_managed_policy(
            iam.ManagedPolicy.from_aws_managed_policy_name("AmazonEC2ContainerRegistryFullAccess"))
        build.role.add_managed_policy(
            iam.ManagedPolicy.from_aws_managed_policy_name("AmazonSSMReadOnlyAccess"))
        build.add_to_role_policy(iam.PolicyStatement(
            actions=["kms:Decrypt", "kms:GenerateDataKey*"], resources=["*"]))
            
    def get_build_env_vars(self, ecr_repo):
        return {
                    "REPOSITORY_URI": codebuild.BuildEnvironmentVariable(value=ecr_repo.repository_uri),
                    "DOCKERHUB_USERNAME": codebuild.BuildEnvironmentVariable(
                                value="/springboot-multiarch/dockerhub/username", 
                                type=codebuild.BuildEnvironmentVariableType.PARAMETER_STORE),
                    "DOCKERHUB_PASSWORD": codebuild.BuildEnvironmentVariable(
                                value="/springboot-multiarch/dockerhub/password ", 
                                type=codebuild.BuildEnvironmentVariableType.PARAMETER_STORE)
                }