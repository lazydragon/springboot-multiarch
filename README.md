prerequesite

1. create Systems Manager Parameter on the console
/springboot-multiarch/dockerhub/username
/springboot-multiarch/dockerhub/password

2. 
```
git clone ......

python3 -m venv .env

cd cdk
./bootstrap.sh {account id}
```

commit code to codecommit
```
git clone https://git-codecommit.us-east-1.amazonaws.com/v1/repos/springboot-multiarch test
cd test
cp -r ../springboot-multiarch/* .
git add *
git commit -m "commit test"
git push
```

aws eks update-kubeconfig --name EKSE2753513-bae9b318b5754fa1adc14474a5322c5c --region us-east-1 --role-arn arn:aws:iam::053173851555:role/backend-EKSMastersRole2941C445-A0OD4MWB37FG
kubectl describe ingress | grep Address 

./cleanup.sh